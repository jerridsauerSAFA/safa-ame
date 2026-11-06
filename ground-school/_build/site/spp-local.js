/* SAFA Student Pilot Permit — local engine.
   Lets the ground-school pages run on a plain website (no Google sign-in):
   - progress is saved on this device (localStorage) instead of the Apps Script sheet
   - in-page buttons get real links to the other pages on this site
   - adds the phone-friendly top bar and menu                                        */
(function () {
  'use strict';
  var NAV = window.SPP_NAV || [];           // filled in by build.py (see nav.js)
  var CFG = window.SPP_SITE || {};
  var KEY = 'safa-spp-rows-v1';

  /* ---------- links: every page id -> absolute URL on this site ---------- */
  var base = new URL('.', location.href).href;
  var links = {};
  (function walk(nodes) {
    nodes.forEach(function (n) {
      if (n.file) {
        var url = base + (n.file === 'index.html' ? '' : n.file);
        links[n.id] = url;
        (n.alias || []).forEach(function (a) { links[a] = url; });
      }
      if (n.kids) walk(n.kids);
    });
  })(NAV);
  links.home = links.spp = base;
  links['oral-direct'] = links.oral || '';
  window.SITE_LINKS = links;
  window.SAFA_ME = { email: 'this-device', name: '', teacher: false };
  window.SAFA_CONFIG = Object.assign({}, CFG.config || {});

  /* ---------- progress saved on this device ---------- */
  function rows() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
  function save(r) { try { localStorage.setItem(KEY, JSON.stringify(r.slice(-20000))); } catch (e) {} }
  var API = {
    track: function (page, unit, type, data) { var r = rows(); r.push([Date.now(), page, unit, type, data]); save(r); return true; },
    getSppData: function () { return { me: { name: '', email: '' }, rows: rows() }; },
    getMyData: function () { return { me: { name: '', email: '' }, rows: rows() }; }
  };
  function runner(ok, fail) {
    return new Proxy({}, {
      get: function (_, name) {
        if (name === 'withSuccessHandler') return function (f) { return runner(f, fail); };
        if (name === 'withFailureHandler') return function (f) { return runner(ok, f); };
        if (name === 'withUserObject') return function () { return runner(ok, fail); };
        return function () {
          var args = arguments;
          setTimeout(function () {
            try {
              if (!API[name]) throw new Error('Not available on this site');
              var res = API[name].apply(null, args);
              if (ok) ok(res);
            } catch (e) { if (fail) fail(e); }
          }, 0);
        };
      }
    });
  }
  window.google = window.google || {};
  window.google.script = { run: runner() };
  window.SPP_LOCAL = {
    rows: rows,
    reset: function () { try { localStorage.removeItem(KEY); } catch (e) {} }
  };

  /* ---------- links inside pages open in the same tab ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[target="_blank"]');
    if (!a || !a.href) return;
    if (a.href.indexOf(base) === 0) { e.preventDefault(); location.href = a.href; }
  }, true);

  /* ---------- top bar + menu ---------- */
  var here = (location.pathname.split('/').pop() || 'index.html');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function contains(n) { return n.file === here || (n.kids || []).some(contains); }
  function item(n, depth) {
    var cur = n.file === here ? ' aria-current="page"' : '';
    var soon = n.soon ? ' <small>coming soon</small>' : '';
    var label = esc(n.label) + soon;
    if (n.kids && n.kids.length) {
      var open = contains(n) ? ' open' : '';
      return '<details class="spp-d' + depth + '"' + open + '><summary>' + label + '</summary>' +
        (n.file ? '<a class="spp-hub" href="' + esc(links[n.id]) + '"' + cur + '>' + esc(n.hubLabel || 'Overview') + '</a>' : '') +
        n.kids.map(function (k) { return item(k, depth + 1); }).join('') + '</details>';
    }
    if (n.soon && !n.file) return '<span class="spp-soon">' + label + '</span>';
    return '<a href="' + esc(links[n.id]) + '"' + cur + '>' + label + '</a>';
  }
  function build() {
    if (document.getElementById('spp-bar')) return;
    var bar = document.createElement('header');
    bar.id = 'spp-bar';
    bar.innerHTML =
      '<button id="spp-menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="spp-drawer"><span></span><span></span><span></span></button>' +
      '<a id="spp-brand" href="' + esc(base) + '"><img src="' + esc(base) + 'safa-mark.png" alt=""><span><b>SAFA Ground School</b><i>Student Pilot Permit</i></span></a>';
    var drawer = document.createElement('nav');
    drawer.id = 'spp-drawer';
    drawer.setAttribute('aria-label', 'Site menu');
    drawer.innerHTML = '<div class="spp-dhead"><b>Menu</b><button id="spp-close" aria-label="Close menu">&times;</button></div>' +
      NAV.map(function (n) { return item(n, 0); }).join('') +
      '<p class="spp-note">Your progress saves on this device and browser.</p>';
    var shade = document.createElement('div');
    shade.id = 'spp-shade';
    var fab = document.createElement('button');
    fab.id = 'spp-fab'; fab.setAttribute('aria-label', 'Open menu'); fab.innerHTML = '<span></span><span></span><span></span>';
    document.body.insertBefore(bar, document.body.firstChild);
    document.body.appendChild(shade);
    document.body.appendChild(drawer);
    document.body.appendChild(fab);
    var btn = document.getElementById('spp-menu-btn');
    function set(open) {
      document.documentElement.classList.toggle('spp-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { var c = drawer.querySelector('[aria-current]'); if (c && c.scrollIntoView) c.scrollIntoView({ block: 'center' }); }
    }
    btn.onclick = fab.onclick = function () { set(true); };
    shade.onclick = document.getElementById('spp-close').onclick = function () { set(false); };
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () { ticking = false; fab.classList.toggle('show', window.scrollY > 260); });
    }, { passive: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
