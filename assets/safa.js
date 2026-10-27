/* SAFA · ASYS 245 shared navigation — v1 (Oct 2026)
   Usage on any page:
     <link rel="stylesheet" href="../../assets/safa-nav.css">   (nav chrome only — safe on any page)
     <link rel="stylesheet" href="../../assets/safa.css">       (full SAFA page styling — study pages and hubs only)
     <body data-mod="4" data-page="notes">   data-mod optional; data-page = a key in MODS[n].pages, "hub", "home" or "wordbank";
                                             data-label overrides the breadcrumb label; data-nav-theme="dark" for always-dark pages
     <script src="../../assets/safa.js" defer></script>
   Builds: sticky top bar, module sheet, breadcrumb + chip strip, footer. Nothing else on the page changes. */
(function(){
  var me = document.currentScript || document.querySelector('script[src*="assets/safa.js"]');
  var ROOT = me.src.replace(/assets\/safa\.js.*$/,'');
  if(!document.querySelector('link[href*="safa-nav.css"]')){
    var l=document.createElement('link'); l.rel='stylesheet'; l.href=ROOT+'assets/safa-nav.css'; document.head.appendChild(l);
  }
  var MODS = [
    {n:1,t:'The Atmosphere',dir:'asys245/module-1/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module1.html'],['cards','Cards','03_Flashcards_Module1.html'],['sheet','Sheet','04_Formula_Sheet_Module1.html'],['lab','Atmosphere lab','05_Atmosphere_Column_Lab_Module1.html']]},
    {n:2,t:'Lift & Drag',dir:'asys245/module-2/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module2.html'],['cards','Cards','03_Flashcards_Module2.html'],['sheet','Sheet','04_Formula_Sheet_Module2.html'],['lab','Stall simulator','05_Airfoil_Stall_Lab_Module2.html']]},
    {n:3,t:'Stability & Control',dir:'asys245/module-3/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module3.html'],['cards','Cards','03_Flashcards_Module3.html'],['sheet','Sheet','04_Formula_Sheet_Module3.html'],['map','Map','05_Stability_Control_Map_Module3.html'],['table','Table','06_Stability_Control_Table_Module3.html'],['lab','Controls lab','09_Flight_Controls_Lab_Module3.html'],['yaw','Adverse yaw lab','07_Adverse_Yaw_Lab_Module3.html'],['yawsheet','Yaw sheet','08_Adverse_Yaw_Sheet_Module3.html']]},
    {n:4,t:'Flight Controls',dir:'asys245/module-4/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module4.html'],['cards','Cards','03_Flashcards_Module4.html'],['sheet','Sheet','04_Formula_Sheet_Module4.html'],['poster','C172 poster','05_C172_Secondary_Flight_Controls_Module4.html'],['lab3','Controls lab','../module-3/09_Flight_Controls_Lab_Module3.html']]},
    {n:5,t:'Performance & Phases of Flight',dir:'asys245/module-5/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module5.html'],['cards','Cards','03_Flashcards_Module5.html'],['sheet','Sheet','04_Formula_Sheet_Module5.html'],['lab2','Stall simulator','../module-2/05_Airfoil_Stall_Lab_Module2.html']]},
    {n:6,t:'Weight & Balance',dir:'asys245/module-6/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module6.html'],['cards','Cards','03_Flashcards_Module6.html'],['sheet','Sheet','04_Formula_Sheet_Module6.html']]},
    {n:7,t:'Airfoil Construction & Performance',soon:true},
    {n:8,t:'ATA Chapters',soon:true},
    {n:'H',t:'Hydraulics',soon:true},
    {n:12,t:'Doors',soon:true},
    {n:13,t:'Windows',soon:true},
    {n:'LG',t:'Landing Gear · Tundra Tires & Skis',soon:true}
  ];
  var WB = 'asys245/module-1/02_Word_Bank.html';
  var b = document.body, modN = b.getAttribute('data-mod'), page = b.getAttribute('data-page')||'';
  var mod = null; MODS.forEach(function(m){ if(String(m.n)===String(modN)) mod=m; });
  var isWB = page==='wordbank', isHub = page==='hub'||page==='home';
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  var MENU='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  var X='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  /* top bar */
  var h=document.createElement('header'); h.className='sb';
  h.innerHTML='<div class="in"><a class="brand" href="'+ROOT+'" aria-label="ASYS 245 home"><img src="'+ROOT+'assets/safa-white.png" alt="SAFA" width="37" height="26"><span>ASYS 245<small>Theory of Flight</small></span></a>'+
    '<button class="menu" type="button" aria-haspopup="dialog" aria-controls="safa-sheet"><span>Modules</span>'+MENU+'</button></div>';
  b.insertBefore(h,b.firstChild);

  /* module sheet */
  var d=document.createElement('dialog'); d.className='sheet'; d.id='safa-sheet'; d.setAttribute('aria-label','Modules');
  var items='<div class="grp">Course</div>';
  items+='<a href="'+ROOT+'"'+(page==='home'?' class="on" aria-current="page"':'')+'><span class="n">⌂</span>All modules</a>';
  items+='<a href="'+ROOT+WB+'"'+(isWB?' class="on" aria-current="page"':'')+'><span class="n">WB</span>Word Bank</a>';
  items+='<div class="grp">Modules</div>';
  MODS.forEach(function(m){
    if(m.soon) items+='<a class="soon" aria-disabled="true"><span class="n">'+m.n+'</span>'+esc(m.t)+'<span class="soonpill">soon</span></a>';
    else items+='<a href="'+ROOT+m.dir+'"'+(mod&&mod.n===m.n?' class="on"':'')+'><span class="n">'+m.n+'</span>'+esc(m.t)+'</a>';
  });
  d.innerHTML='<div class="panel"><div class="head"><b>Modules</b><button type="button" class="close" aria-label="Close menu">'+X+'</button></div>'+items+'<div class="foot">Progress and notes save on this device. Works offline once opened.</div></div>';
  b.appendChild(d);
  h.querySelector('.menu').addEventListener('click',function(){ if(d.showModal) d.showModal(); else d.setAttribute('open',''); });
  d.querySelector('.close').addEventListener('click',function(){ d.close ? d.close() : d.removeAttribute('open'); });
  d.addEventListener('click',function(e){ if(e.target===d) d.close(); });

  /* breadcrumb + chip strip, directly under the bar */
  if(mod||isWB){
    var sub=document.createElement('div'); sub.className='s-sub'+(isHub?' narrow':'');
    var parts='<a href="'+ROOT+'">Modules</a>';
    if(mod){
      parts+='<span class="sep" aria-hidden="true">›</span>';
      if(page==='hub') parts+='<span class="here">Mod '+mod.n+' · '+esc(mod.t)+'</span>';
      else{
        var cur=null; mod.pages.forEach(function(p){ if(p[0]===page) cur=p; });
        parts+='<a href="'+ROOT+mod.dir+'">Mod '+mod.n+'</a><span class="sep" aria-hidden="true">›</span><span class="here">'+esc(b.getAttribute('data-label')||(cur?cur[1]:'Study'))+'</span>';
      }
    } else parts+='<span class="sep" aria-hidden="true">›</span><span class="here">Word Bank</span>';
    var html='<div class="in"><nav class="s-crumb" aria-label="Breadcrumb">'+parts+'</nav>';
    if(mod && page!=='hub'){
      html+='<nav class="s-chips" aria-label="Study sets in this module"><a href="'+ROOT+mod.dir+'">Mod '+mod.n+' home</a>';
      mod.pages.forEach(function(p){ html+='<a href="'+ROOT+mod.dir+p[2]+'"'+(p[0]===page?' class="on" aria-current="page"':'')+'>'+esc(p[1])+'</a>'; });
      html+='<a href="'+ROOT+WB+'">Word Bank</a></nav>';
    }
    sub.innerHTML=html+'</div>';
    h.insertAdjacentElement('afterend',sub);
    var ch=sub.querySelector('.s-chips'), on=ch&&ch.querySelector('.on');
    if(on) ch.scrollLeft=Math.max(0,on.offsetLeft-ch.offsetLeft-(ch.clientWidth-on.offsetWidth)/2);
  }

  /* footer */
  var f=document.createElement('footer'); f.className='sf';
  f.innerHTML='<div class="in"><div class="logos"><img src="'+ROOT+'assets/safa-white.png" alt="South Alberta Flight Academy" width="57" height="40"><span class="tile"><img src="'+ROOT+'assets/sait-logo.png" alt="SAIT" width="22" height="30"></span></div>'+
    '<small>ASYS 245 Theory of Flight study sets, built from each class for South Alberta Flight Academy students. Not an official SAIT publication — confirm anything safety-critical against the manual. <a href="'+ROOT+'">All modules</a></small></div>';
  b.appendChild(f);

  /* edge to edge: pages that pad their own <body> (the labs) would otherwise inset the bar, strip and footer */
  function bleed(){
    var cs=getComputedStyle(b), pl=parseFloat(cs.paddingLeft)||0, pr=parseFloat(cs.paddingRight)||0,
        pt=parseFloat(cs.paddingTop)||0, pb=parseFloat(cs.paddingBottom)||0;
    var els=[h,f,document.querySelector('.s-sub')];
    els.forEach(function(el){ if(!el) return;
      el.style.marginLeft=(-pl)+'px'; el.style.marginRight=(-pr)+'px';
      el.style.width='calc(100% + '+(pl+pr)+'px)'; el.style.maxWidth='none'; });
    h.style.marginTop=(-pt)+'px'; f.style.marginBottom=(-pb)+'px';
  }
  bleed(); addEventListener('resize',bleed);
})();
