/* SAFA · ASYS 245 shared navigation — v1 (Oct 2026)
   Usage on any page:
     <link rel="stylesheet" href="../../assets/safa.css">
     <body data-mod="4" data-page="notes">  (data-mod optional; data-page = key in MODS[n].pages, or "hub")
     <script src="../../assets/safa.js" defer></script>
   Builds: sticky top bar, module sheet, breadcrumb, chip row, footer. Nothing else on the page changes. */
(function(){
  var ROOT = document.currentScript.src.replace(/assets\/safa\.js.*$/,'');
  var MODS = [
    {n:1,t:'The Atmosphere',dir:'asys245/module-1/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module1.html'],['cards','Cards','03_Flashcards_Module1.html'],['sheet','Sheet','04_Formula_Sheet_Module1.html'],['lab','Lab','05_Atmosphere_Column_Lab_Module1.html']]},
    {n:2,t:'Lift & Drag',dir:'asys245/module-2/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module2.html'],['cards','Cards','03_Flashcards_Module2.html'],['sheet','Sheet','04_Formula_Sheet_Module2.html'],['lab','Simulator','05_Airfoil_Stall_Lab_Module2.html']]},
    {n:3,t:'Stability & Control',dir:'asys245/module-3/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module3.html'],['cards','Cards','03_Flashcards_Module3.html'],['sheet','Sheet','04_Formula_Sheet_Module3.html'],['map','Map','05_Stability_Control_Map_Module3.html'],['table','Table','06_Stability_Control_Table_Module3.html'],['lab','Controls lab','09_Flight_Controls_Lab_Module3.html'],['yaw','Adverse yaw','07_Adverse_Yaw_Lab_Module3.html']]},
    {n:4,t:'Flight Controls',dir:'asys245/module-4/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module4.html'],['cards','Cards','03_Flashcards_Module4.html'],['sheet','Sheet','04_Formula_Sheet_Module4.html'],['poster','C172 poster','05_C172_Secondary_Flight_Controls_Module4.html'],['lab','Controls lab','../module-3/09_Flight_Controls_Lab_Module3.html']]},
    {n:5,t:'Performance & Phases of Flight',dir:'asys245/module-5/',pages:[
      ['notes','Notes','01_Cornell_Notes_Module5.html'],['cards','Cards','03_Flashcards_Module5.html'],['sheet','Sheet','04_Formula_Sheet_Module5.html'],['lab','Stall sim','../module-2/05_Airfoil_Stall_Lab_Module2.html']]},
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
  var isWB = page==='wordbank';
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  var MENU='<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  var X='<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  /* top bar */
  var h=document.createElement('header'); h.className='sb';
  h.innerHTML='<div class="in"><a class="brand" href="'+ROOT+'" aria-label="SAFA AME home"><img src="'+ROOT+'assets/safa-white.png" alt="SAFA"><span>ASYS 245<small>Theory of Flight</small></span></a>'+
    '<button class="menu" type="button" aria-haspopup="dialog" aria-controls="safa-sheet"><span>Modules</span>'+MENU+'</button></div>';
  b.insertBefore(h,b.firstChild);

  /* sheet */
  var d=document.createElement('dialog'); d.className='sheet'; d.id='safa-sheet';
  var items='';
  items+='<div class="grp">Course</div>';
  items+='<a href="'+ROOT+'"'+(!mod&&!isWB?' class="on"':'')+'><span class="n">⌂</span>All modules</a>';
  items+='<a href="'+ROOT+WB+'"'+(isWB?' class="on"':'')+'><span class="n">WB</span>Word Bank</a>';
  items+='<div class="grp">Modules</div>';
  MODS.forEach(function(m){
    if(m.soon){ items+='<a class="soon" tabindex="-1" aria-disabled="true"><span class="n">'+m.n+'</span>'+esc(m.t)+' <span class="soonpill">soon</span></a>'; }
    else { items+='<a href="'+ROOT+m.dir+'"'+(mod&&mod.n===m.n?' class="on"':'')+'><span class="n">'+m.n+'</span>'+esc(m.t)+'</a>'; }
  });
  d.innerHTML='<div class="panel"><div class="head"><b>Modules</b><button type="button" class="close" aria-label="Close menu">'+X+'</button></div>'+items+'<div class="foot">Progress and notes save on this device. Works offline once opened.</div></div>';
  b.appendChild(d);
  h.querySelector('.menu').addEventListener('click',function(){ d.showModal(); });
  d.querySelector('.close').addEventListener('click',function(){ d.close(); });
  d.addEventListener('click',function(e){ if(e.target===d) d.close(); });

  /* breadcrumb + chips (inside main / .w, before its first child) */
  var main=document.querySelector('main')||document.querySelector('.w');
  if(main && (mod||isWB)){
    var cr=document.createElement('nav'); cr.className='crumb'; cr.setAttribute('aria-label','Breadcrumb');
    var parts='<a href="'+ROOT+'">Modules</a>';
    if(mod){
      parts+='<span class="sep">›</span>';
      if(page==='hub') parts+='<span class="here">Mod '+mod.n+' · '+esc(mod.t)+'</span>';
      else{
        parts+='<a href="'+ROOT+mod.dir+'">Mod '+mod.n+'</a>';
        var cur=null; mod.pages.forEach(function(p){ if(p[0]===page) cur=p; });
        parts+='<span class="sep">›</span><span class="here">'+(cur?esc(cur[1]):'Study')+'</span>';
      }
    } else parts+='<span class="sep">›</span><span class="here">Word Bank</span>';
    cr.innerHTML=parts; main.insertBefore(cr,main.firstChild);
    if(mod && page!=='hub'){
      var ch=document.createElement('nav'); ch.className='chips'; ch.setAttribute('aria-label','Study sets in this module');
      var cs='<a href="'+ROOT+mod.dir+'">Mod '+mod.n+' home</a>';
      mod.pages.forEach(function(p){ cs+='<a href="'+ROOT+mod.dir+p[2]+'"'+(p[0]===page?' class="on" aria-current="page"':'')+'>'+esc(p[1])+'</a>'; });
      cs+='<a href="'+ROOT+WB+'">Word Bank</a>';
      ch.innerHTML=cs; cr.insertAdjacentElement('afterend',ch);
      var on=ch.querySelector('.on'); if(on&&on.scrollIntoView) try{ on.scrollIntoView({inline:'center',block:'nearest'}); }catch(e){}
    }
  }

  /* footer */
  var f=document.createElement('footer'); f.className='sf';
  f.innerHTML='<div class="in"><div class="logos"><img src="'+ROOT+'assets/safa-white.png" alt="South Alberta Flight Academy"><span class="tile"><img src="'+ROOT+'assets/sait-logo.png" alt="SAIT"></span></div>'+
    '<small>ASYS 245 Theory of Flight study sets, built from each class for South Alberta Flight Academy students. Not an official SAIT publication — confirm anything safety-critical against the manual. <a href="'+ROOT+'">All modules</a></small></div>';
  b.appendChild(f);
})();
