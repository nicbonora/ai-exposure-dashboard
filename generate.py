import csv, json
BASE = '/Users/n.bonora/Downloads/ai-exposure-dashboard'
jobs = []
with open(f'{BASE}/data/job_exposure.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        jobs.append({'code': row['occ_code'], 'title': row['title'], 'exp': round(float(row['observed_exposure']), 4)})
jobs.sort(key=lambda x: x['title'])
jobs_json = json.dumps(jobs, ensure_ascii=False)
out = open(f'{BASE}/index.html', 'w', encoding='utf-8')
out.write('''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI e Lavoro \u2014 Anthropic Economic Index 2026</title>
<style>
:root{--bg:#0a0a0a;--s1:#141414;--s2:#1e1e1e;--bd:#272727;--tx:#f0f0f0;--mu:#a0a0a0;--ac:#e06c2c;--r:14px}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;display:flex;flex-direction:column;align-items:center}
.screen{display:none;width:100%;max-width:620px;padding:2.5rem 1.5rem;min-height:100vh;flex-direction:column}
.screen.active{display:flex}
.logo{font-size:.94rem;color:var(--mu);letter-spacing:.12em;text-transform:uppercase;margin-bottom:3.5rem;display:flex;align-items:center;gap:.6rem}
.logo-dot{display:inline-block;width:18px;height:18px;background:var(--ac);border-radius:4px;flex-shrink:0}
.hero-title{font-size:2.6rem;font-weight:700;line-height:1.15;margin-bottom:.75rem}
.hero-sub{color:var(--mu);margin-bottom:2.5rem;line-height:1.65;font-size:1.24rem}
.search-wrap{position:relative}
#search{width:100%;padding:1rem 1.25rem;background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);color:var(--tx);font-size:1.3rem;outline:none;transition:border-color .2s}
#search::placeholder{color:var(--mu)}
#search:focus{border-color:var(--ac)}
#suggestions{position:absolute;top:calc(100% + 6px);left:0;right:0;background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);list-style:none;overflow-y:auto;max-height:280px;z-index:10;display:none}
#suggestions.open{display:block}
#suggestions li{padding:.85rem 1.25rem;cursor:pointer;font-size:1.17rem;border-bottom:1px solid var(--bd);transition:background .15s}
#suggestions li:last-child{border-bottom:none}
#suggestions li:hover{background:var(--s2)}
.hint{margin-top:1rem;font-size:1rem;color:var(--mu)}
.footer-note{margin-top:auto;padding-top:1.5rem;border-top:1px solid var(--bd);font-size:.94rem;color:var(--mu);line-height:1.7}
.back-btn{display:inline-flex;align-items:center;gap:.4rem;font-size:1.1rem;cursor:pointer;margin-bottom:2rem;background:none;border:none;color:var(--mu);transition:color .2s;padding:0;font-family:inherit}
.back-btn:hover{color:var(--tx)}
.job-heading{font-size:2.08rem;font-weight:700;margin-bottom:.3rem}
.job-cat{color:var(--mu);font-size:1.1rem;margin-bottom:2.5rem}
.gauge-wrap{display:flex;flex-direction:column;align-items:center;margin-bottom:2rem}
.tier-card{width:100%;border-radius:var(--r);padding:1.25rem 1.5rem;background:var(--s1);border-left:4px solid var(--ac);margin-bottom:1.5rem}
.tier-name{font-weight:700;font-size:1.37rem;margin-bottom:.4rem}
.tier-desc{color:var(--mu);font-size:1.15rem;line-height:1.65}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:.85rem;margin-bottom:1.75rem}
.stat-box{background:var(--s1);border-radius:var(--r);padding:1rem 1.25rem;border:1px solid var(--bd)}
.stat-lbl{font-size:.94rem;color:var(--mu);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.35rem}
.stat-val{font-size:1.75rem;font-weight:700}
.cta-btn{width:100%;padding:1rem;background:var(--ac);color:#fff;border:none;border-radius:var(--r);font-size:1.3rem;font-weight:600;cursor:pointer;transition:opacity .2s;font-family:inherit}
.cta-btn:hover{opacity:.85}
.section-lbl{font-size:.94rem;text-transform:uppercase;letter-spacing:.1em;color:var(--mu);margin-bottom:.5rem}
.ctx-title{font-size:1.75rem;font-weight:700;margin-bottom:2rem}
.dist-wrap{margin-bottom:2rem}
.dist-track{height:8px;background:var(--s2);border-radius:4px;position:relative;margin:.85rem 0}
.dist-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,#3b82f6 0%,#10b981 30%,#f59e0b 60%,#ef4444 100%)}
.dist-marker{position:absolute;top:-5px;width:3px;height:18px;background:#fff;border-radius:2px;transform:translateX(-50%);transition:left 1.1s cubic-bezier(.4,0,.2,1)}
.dist-labels{display:flex;justify-content:space-between;font-size:.94rem;color:var(--mu)}
.dist-you{font-size:1rem;color:var(--tx);margin-top:.5rem;text-align:center;min-height:1.2rem}
.ctx-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.85rem;margin-bottom:2rem}
.cs-val{font-size:1.7rem;font-weight:700;margin-bottom:.3rem}
.cs-lbl{font-size:.88rem;color:var(--mu);line-height:1.4}
.notes-title{font-size:1.24rem;font-weight:600;margin-bottom:1rem}
.note-item{display:flex;gap:.75rem;margin-bottom:.85rem;font-size:1.1rem;color:var(--mu);line-height:1.55}
.note-dot{width:6px;height:6px;border-radius:50%;background:var(--ac);flex-shrink:0;margin-top:.42rem}
.source{margin-top:auto;padding-top:1.5rem;border-top:1px solid var(--bd);font-size:.94rem;color:var(--mu);line-height:1.65}
.source a{color:var(--mu)}
.gauge-bg{fill:none;stroke:var(--s2);stroke-width:12;stroke-linecap:round}
.gauge-fill{fill:none;stroke-width:12;stroke-linecap:round;transition:stroke-dasharray 1.1s cubic-bezier(.4,0,.2,1),stroke .3s}
.stat-lbl-wrap{display:flex;align-items:center;gap:.4rem;margin-bottom:.35rem}
.tip-wrap{position:relative;display:inline-flex;align-items:center}
.tip-icon{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;border:1.5px solid var(--mu);color:var(--mu);font-size:.65rem;font-weight:700;cursor:help;flex-shrink:0;font-style:normal;line-height:1;user-select:none}
.tip-box{display:none;position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#242424;border:1px solid var(--bd);border-radius:10px;padding:.7rem 1rem;font-size:.88rem;color:#d0d0d0;line-height:1.55;width:220px;z-index:50;pointer-events:none;box-shadow:0 4px 20px rgba(0,0,0,.5)}
.tip-box::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:6px solid transparent;border-top-color:#242424}
.tip-wrap:hover .tip-box,.tip-wrap:focus-within .tip-box{display:block}
.cs{position:relative;background:var(--s1);border-radius:var(--r);padding:1.25rem 1rem;text-align:center;border:1px solid var(--bd)}
.cs .tip-wrap{position:absolute;top:.6rem;right:.6rem}
.cs .tip-box{left:auto;right:0;transform:none}
.cs .tip-box::after{left:auto;right:12px;transform:none}
.explore-link{display:block;text-align:center;margin-top:1.5rem;color:var(--mu);font-size:1rem;cursor:pointer;text-decoration:none;transition:color .2s}.explore-link:hover{color:var(--tx)}
.chart-wrap{width:100%;overflow-x:auto;margin-bottom:1.5rem}
.chart-svg{display:block;width:100%;max-width:640px;margin:0 auto}
.bubble{cursor:pointer;transition:opacity .15s}.bubble.dimmed{opacity:.1}.bubble.highlighted{opacity:1;stroke:#fff;stroke-width:1.5}
.chart-tip{display:none;position:fixed;background:#242424;border:1px solid #333;border-radius:10px;padding:.6rem .9rem;font-size:.82rem;color:#d0d0d0;line-height:1.5;width:190px;z-index:100;pointer-events:none;box-shadow:0 4px 16px rgba(0,0,0,.5)}
.legend-wrap{display:flex;flex-wrap:wrap;gap:.5rem .9rem;margin-bottom:1.5rem}
.legend-item{display:flex;align-items:center;gap:.35rem;font-size:.88rem;color:var(--mu)}.legend-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
#chart-search{width:100%;padding:.7rem 1rem;background:var(--s1);border:1px solid var(--bd);border-radius:var(--r);color:var(--tx);font-size:1rem;outline:none;margin-bottom:1rem;font-family:inherit}
#chart-search::placeholder{color:var(--mu)}#chart-search:focus{border-color:var(--ac)}
.chart-axis-lbl{font-size:11px;fill:#666;font-family:-apple-system,sans-serif}
</style>
''')
out.write('''</head>
<body>
<section id="s-search" class="screen active">
  <div class="logo"><span class="logo-dot"></span>Anthropic Economic Index 2026</div>
  <h1 class="hero-title">Il tuo lavoro<br>e l&#39;AI</h1>
  <p class="hero-sub">Cerca la tua professione e scopri in che misura i Large Language Model vengono gi&#224; usati &#8212; in contesti professionali reali &#8212; per svolgere i tuoi task quotidiani.</p>
  <div class="search-wrap">
    <input id="search" type="text" placeholder="E.g. Software Developer, Financial Analyst, Writer..." autocomplete="off">
    <ul id="suggestions"></ul>
  </div>
  <p class="hint">~758 occupazioni del Bureau of Labor Statistics (USA)</p>
  <a class="explore-link" onclick="showOverview()">&#127358; Oppure esplora tutte le 756 professioni nel grafico &rarr;</a>
  <p class="footer-note">Basato su: Massenkoff &amp; McCrory, <em>Labor market impacts of AI: A new measure and early evidence</em>, Anthropic, 5 marzo 2026.</p>
</section>

<section id="s-profile" class="screen">
  <button id="profile-back-btn" class="back-btn" onclick="goBackProfile()">&#8592; Cambia professione</button>
  <h2 class="job-heading" id="p-title">&#8212;</h2>
  <p class="job-cat" id="p-cat">&#8212;</p>
  <div class="gauge-wrap">
    <svg width="220" height="130" viewBox="0 0 220 130">
      <path class="gauge-bg" d="M 20 120 A 90 90 0 0 1 200 120"/>
      <path class="gauge-fill" id="gauge-fill" d="M 20 120 A 90 90 0 0 1 200 120" stroke="#e06c2c" stroke-dasharray="0 282.74"/>
      <text id="gauge-pct" x="110" y="105" text-anchor="middle" font-size="36" font-weight="700" fill="#f0f0f0">0%</text>
      <text x="110" y="126" text-anchor="middle" font-size="14" fill="#a0a0a0">esposizione osservata</text>
    </svg>
  </div>
  <div class="tier-card" id="tier-card">
    <div class="tier-name" id="tier-name">&#8212;</div>
    <div class="tier-desc" id="tier-desc">&#8212;</div>
  </div>
  <div class="stats-grid">
    <div class="stat-box">
      <div class="stat-lbl-wrap">
        <div class="stat-lbl">Media categoria</div>
        <div class="tip-wrap"><span class="tip-icon">i</span><div class="tip-box">Esposizione media di tutte le occupazioni nella stessa categoria BLS. Ti dice se questa professione \u00e8 pi\u00f9 o meno esposta rispetto al suo settore di riferimento.</div></div>
      </div>
      <div class="stat-val" id="p-catavg">&#8212;</div>
    </div>
    <div class="stat-box">
      <div class="stat-lbl-wrap">
        <div class="stat-lbl">Ranking</div>
        <div class="tip-wrap"><span class="tip-icon">i</span><div class="tip-box">Posizione di questa occupazione tra le 756 censite, ordinate per esposizione crescente. #1 = meno esposta, #756 = pi\u00f9 esposta.</div></div>
      </div>
      <div class="stat-val" id="p-rank">&#8212;</div>
    </div>
  </div>
  <button class="cta-btn" onclick="showContext()">Vedi nel contesto generale &#8594;</button>
</section>

<section id="s-context" class="screen">
  <button class="back-btn" onclick="goBack('s-profile')">&#8592; Torna al profilo</button>
  <p class="section-lbl">Contesto</p>
  <h2 class="ctx-title" id="c-title">&#8212;</h2>
  <div class="dist-wrap">
    <p class="section-lbl">Dove si colloca tra tutte le professioni</p>
    <div class="dist-track">
      <div class="dist-fill" style="width:100%"></div>
      <div class="dist-marker" id="dist-marker" style="left:0%"></div>
    </div>
    <div class="dist-labels"><span>0% &#8212; nessuna</span><span>75% &#8212; massima rilevata</span></div>
    <p class="dist-you" id="dist-you"></p>
  </div>
  <div class="ctx-stats">
    <div class="cs">
      <div class="tip-wrap"><span class="tip-icon">i</span><div class="tip-box">In che percentuale di occupazioni questa \u00e8 meno esposta. 90\u00b0 percentile = pi\u00f9 esposta del 90% delle professioni censite.</div></div>
      <div class="cs-val" id="c-pct">&#8212;</div>
      <div class="cs-lbl">percentile di esposizione</div>
    </div>
    <div class="cs">
      <div class="tip-wrap"><span class="tip-icon">i</span><div class="tip-box">Il 30% delle professioni censite ha esposizione zero: nessun task osservato su Claude in contesti professionali. Tipicamente lavori manuali, fisici o molto specializzati.</div></div>
      <div class="cs-val">30%</div>
      <div class="cs-lbl">occupazioni a esposizione zero</div>
    </div>
    <div class="cs">
      <div class="tip-wrap"><span class="tip-icon">i</span><div class="tip-box">Stima derivata dalla correlazione del report: ogni +10% di esposizione corrisponde a -0,6% di crescita occupazionale prevista dal BLS. Valore indicativo, non ufficiale.</div></div>
      <div class="cs-val" id="c-bls">&#8212;</div>
      <div class="cs-lbl">crescita BLS stimata 2024&#8211;34</div>
    </div>
  </div>
  <p class="notes-title">Dal report Anthropic</p>
  <div class="note-item"><div class="note-dot"></div><span>Nessun aumento sistematico della disoccupazione nei settori pi&#249; esposti (dati CPS, 2022&#8211;2026).</span></div>
  <div class="note-item"><div class="note-dot"></div><span id="note-young">&#8212;</span></div>
  <div class="note-item"><div class="note-dot"></div><span>I lavoratori nelle occupazioni pi&#249; esposte guadagnano in media il 47% in pi&#249;, sono pi&#249; istruiti e pi&#249; spesso donne.</span></div>
  <p class="source">Fonte: Massenkoff &amp; McCrory, <em>Anthropic Economic Index</em>, 5 marzo 2026 &#8212; <a href="https://www.anthropic.com/research/labor-market-impacts" target="_blank">anthropic.com/research</a><br>Dataset: <a href="https://huggingface.co/datasets/Anthropic/EconomicIndex" target="_blank">huggingface.co/datasets/Anthropic/EconomicIndex</a></p>
</section>

<section id="s-overview" class="screen">
  <button class="back-btn" onclick="showScreen('s-search')">&#8592; Cerca per professione</button>
  <p class="section-lbl">Vista globale</p>
  <h2 class="ctx-title">756 professioni &mdash; esposizione vs crescita attesa</h2>
  <input id="chart-search" type="text" placeholder="Filtra per professione..." autocomplete="off">
  <div class="chart-wrap">
    <svg id="chart-svg" class="chart-svg" viewBox="0 0 640 428" preserveAspectRatio="xMidYMid meet">
      <g id="bubbles-layer"></g>
    </svg>
  </div>
  <div class="legend-wrap" id="legend-wrap"></div>
  <div id="chart-tip" class="chart-tip"></div>
  <p class="source">Dati: Massenkoff &amp; McCrory, <em>Anthropic Economic Index</em>, 2026 &mdash; <a href="https://www.anthropic.com/research/labor-market-impacts" target="_blank">anthropic.com/research</a></p>
</section>
''')
out.write('<script>\nconst JOBS = ')
out.write(jobs_json)
out.write(''';\nconst CATS={'11':'Management','13':'Business & Financial','15':'Computer & Matematica','17':'Architettura & Ingegneria','19':'Scienze naturali e sociali','21':'Servizi sociali','23':'Legale','25':'Educazione & Biblioteca','27':'Arte, Media & Intrattenimento','29':'Sanit\u00e0 \u2014 Professionisti','31':'Sanit\u00e0 \u2014 Supporto','33':'Sicurezza pubblica','35':'Ristorazione','37':'Pulizie & Manutenzione','39':'Servizi personali','41':'Vendite','43':'Ufficio & Amministrazione','45':'Agricoltura & Pesca','47':'Costruzioni','49':'Installazioni & Riparazioni','51':'Produzione','53':'Trasporti'};
const SORTED=[...JOBS].sort((a,b)=>a.exp-b.exp);
const ARC=282.74;
let sel=null,prevScreen='s-search',chartInited=false,legendInited=false;
function pct(e){return Math.round(e*100)+'%';}
function getTier(e){
  if(e===0)return{label:'Non rilevata',desc:'Nessun task di questa professione \u00e8 stato osservato in uso su Claude in contesti professionali. Pu\u00f2 dipendere da bassa diffusione o dalla natura fisica del lavoro.',color:'#6b7280'};
  if(e<0.1)return{label:'Molto bassa',desc:'Il '+pct(e)+' dei task risulta gi\u00e0 coperto in contesti professionali reali. La diffusione \u00e8 nelle fasi iniziali e riguarda attivit\u00e0 circoscritte.',color:'#3b82f6'};
  if(e<0.25)return{label:'Bassa',desc:'Il '+pct(e)+' dei task mostra uso reale di Claude. La tecnologia \u00e8 presente ma coinvolge una minoranza delle attivit\u00e0 quotidiane.',color:'#10b981'};
  if(e<0.45)return{label:'Moderata',desc:'Il '+pct(e)+' dei task \u00e8 gi\u00e0 coperto. Una parte significativa del lavoro quotidiano viene supportata o automatizzata da Claude.',color:'#f59e0b'};
  if(e<0.65)return{label:'Alta',desc:'Il '+pct(e)+' dei task mostra esposizione osservata. L\\'AI sta ridefinendo concretamente molte attivit\u00e0 di questo ruolo.',color:'#ef4444'};
  return{label:'Molto alta',desc:'Il '+pct(e)+' dei task \u00e8 coperto \u2014 tra le professioni pi\u00f9 esposte. Cambiamenti sostanziali sono gi\u00e0 in corso.',color:'#dc2626'};
}
function selectJob(code,from){
  if(from)prevScreen=from;
  sel=JOBS.find(j=>j.code===code);if(!sel)return;
  const e=sel.exp,tier=getTier(e),catCode=code.split('-')[0];
  const catName=CATS[catCode]||'Altra categoria';
  const catJobs=JOBS.filter(j=>j.code.split('-')[0]===catCode);
  const catAvg=catJobs.reduce((s,j)=>s+j.exp,0)/catJobs.length;
  const rank=SORTED.findIndex(j=>j.code===code)+1;
  const percentile=Math.round((rank/JOBS.length)*100);
  const blsRaw=+(4.5-e*6).toFixed(1);
  sel._tier=tier;sel._cat=catName;sel._catAvg=catAvg;sel._rank=rank;sel._pct=percentile;
  sel._bls=(blsRaw>0?'+':'')+blsRaw+'%';
  document.getElementById('p-title').textContent=sel.title;
  document.getElementById('p-cat').textContent=catName;
  document.getElementById('tier-name').textContent=tier.label;
  document.getElementById('tier-desc').textContent=tier.desc;
  document.getElementById('tier-card').style.borderLeftColor=tier.color;
  document.getElementById('p-catavg').textContent=pct(catAvg);
  document.getElementById('p-rank').textContent='#'+rank+' / '+JOBS.length;
  const bb=document.getElementById('profile-back-btn');
  if(bb)bb.textContent=prevScreen==='s-overview'?'\u2190 Torna al grafico':'\u2190 Cambia professione';
  showScreen('s-profile');
  document.getElementById('suggestions').classList.remove('open');
  document.getElementById('search').value='';
  setTimeout(()=>{document.getElementById('gauge-fill').setAttribute('stroke-dasharray',(e*ARC)+' '+ARC);document.getElementById('gauge-fill').setAttribute('stroke',tier.color);document.getElementById('gauge-pct').textContent=pct(e);},150);
}
function showContext(){
  if(!sel)return;
  document.getElementById('c-title').textContent=sel.title;
  document.getElementById('c-pct').textContent=sel._pct+'\u00b0';
  document.getElementById('c-bls').textContent=sel._bls;
  const mp=Math.min((sel.exp/0.75)*100,100).toFixed(1);
  setTimeout(()=>{document.getElementById('dist-marker').style.left=mp+'%';document.getElementById('dist-you').textContent='\u2191 '+sel.title+' \u2014 '+pct(sel.exp);},80);
  document.getElementById('note-young').textContent=sel._pct>=70?'Per i giovani (22\u201325 anni) nelle occupazioni pi\u00f9 esposte, il tasso di hiring \u00e8 calato del 14% rispetto al 2022. Il segnale \u00e8 statisticamente significativo ma ancora da confermare.':'Nelle occupazioni a bassa esposizione, i trend di hiring per i lavoratori giovani restano sostanzialmente stabili rispetto al periodo pre-ChatGPT.';
  showScreen('s-context');
}
function showScreen(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');window.scrollTo(0,0);}
function goBack(id){showScreen(id);}
function goBackProfile(){showScreen(prevScreen);}
const srch=document.getElementById('search'),sugg=document.getElementById('suggestions');
srch.addEventListener('input',()=>{const q=srch.value.toLowerCase().trim();if(q.length<2){sugg.innerHTML='';sugg.classList.remove('open');return;}const hits=JOBS.filter(j=>j.title.toLowerCase().includes(q)).slice(0,8);sugg.innerHTML=hits.map(j=>'<li onclick="selectJob(\\'' +j.code+ '\\')">' +j.title+ '</li>').join('');sugg.classList.toggle('open',hits.length>0);});
document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap')){sugg.innerHTML='';sugg.classList.remove('open');}});
function showOverview(){initChart();initLegend();showScreen('s-overview');}
function initLegend(){
  if(legendInited)return;legendInited=true;
  const G=[{l:'Tech, Ingegneria & Scienze',c:'#3b82f6'},{l:'Business, Legale & Amm.',c:'#8b5cf6'},{l:'Sanit\u00e0',c:'#10b981'},{l:'Educazione & Arte',c:'#f59e0b'},{l:'Servizi sociali',c:'#ec4899'},{l:'Vendite & Servizi',c:'#f97316'},{l:'Lavoro manuale & Trades',c:'#6b7280'}];
  const w=document.getElementById('legend-wrap');
  G.forEach(g=>{const d=document.createElement('div');d.className='legend-item';d.innerHTML='<div class="legend-dot" style="background:'+g.c+'"></div>'+g.l;w.appendChild(d);});
}
function initChart(){
  if(chartInited)return;chartInited=true;
  const svg=document.getElementById('chart-svg'),tip=document.getElementById('chart-tip');
  const X1=60,X2=600,Y1=18,Y2=390,ns='http://www.w3.org/2000/svg';
  function el(tag,a){const e=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(a))e.setAttribute(k,v);return e;}
  function eX(e){return X1+(e/0.75)*(X2-X1);}
  function bY(b){return Y2-(b/4.5)*(Y2-Y1);}
  function hj(code,i){let h=0;for(const c of code)h=(h*31+c.charCodeAt(0))&0xffff;return((h+i*7919)%200-100)/100;}
  const COL={'11':'#8b5cf6','13':'#8b5cf6','15':'#3b82f6','17':'#3b82f6','19':'#3b82f6','23':'#06b6d4','43':'#06b6d4','29':'#10b981','31':'#10b981','25':'#f59e0b','27':'#f59e0b','21':'#ec4899','33':'#ec4899','39':'#ec4899','35':'#f97316','37':'#f97316','41':'#f97316','45':'#f97316','47':'#6b7280','49':'#6b7280','51':'#6b7280','53':'#6b7280'};
  function col(code){return COL[code.split('-')[0]]||'#6b7280';}
  svg.appendChild(el('line',{'x1':X1,'y1':Y2,'x2':X2,'y2':Y2,'stroke':'#333','stroke-width':'1'}));
  svg.appendChild(el('line',{'x1':X1,'y1':Y1,'x2':X1,'y2':Y2,'stroke':'#333','stroke-width':'1'}));
  [0,0.15,0.30,0.45,0.60,0.75].forEach(e=>{const x=eX(e);svg.appendChild(el('line',{'x1':x,'y1':Y1,'x2':x,'y2':Y2,'stroke':'#1c1c1c','stroke-width':'1'}));const t=el('text',{'x':x,'y':Y2+13,'text-anchor':'middle','class':'chart-axis-lbl'});t.textContent=Math.round(e*100)+'%';svg.appendChild(t);});
  [0,1.5,3,4.5].forEach(b=>{const y=bY(b);svg.appendChild(el('line',{'x1':X1,'y1':y,'x2':X2,'y2':y,'stroke':'#1c1c1c','stroke-width':'1'}));const t=el('text',{'x':X1-5,'y':y+4,'text-anchor':'end','class':'chart-axis-lbl'});t.textContent=(b>0?'+':'')+b.toFixed(1)+'%';svg.appendChild(t);});
  const xl=el('text',{'x':(X1+X2)/2,'y':420,'text-anchor':'middle','class':'chart-axis-lbl'});xl.textContent='Esposizione osservata \u2192';svg.appendChild(xl);
  svg.appendChild(el('line',{'x1':eX(0),'y1':bY(4.5),'x2':eX(0.75),'y2':bY(0),'stroke':'#333','stroke-width':'1','stroke-dasharray':'4 3'}));
  const layer=document.getElementById('bubbles-layer');
  JOBS.forEach(j=>{
    const bls=4.5-j.exp*6,x0=eX(j.exp),y0=bY(bls);
    const cx=Math.max(X1+4,Math.min(X2-4,x0+hj(j.code,0)*16));
    const cy=Math.max(Y1+4,Math.min(Y2-4,y0+hj(j.code,1)*20));
    const c=el('circle',{'cx':cx,'cy':cy,'r':'4','fill':col(j.code),'opacity':'0.72','class':'bubble','data-code':j.code,'data-title':j.title,'data-exp':j.exp});
    c.addEventListener('mouseenter',()=>{tip.innerHTML='<strong>'+j.title+'</strong><br>Esposizione: '+pct(j.exp)+'<br>'+getTier(j.exp).label;tip.style.display='block';});
    c.addEventListener('mousemove',ev=>{tip.style.left=(ev.clientX+14)+'px';tip.style.top=(ev.clientY-54)+'px';});
    c.addEventListener('mouseleave',()=>{tip.style.display='none';});
    c.addEventListener('click',()=>{selectJob(j.code,'s-overview');});
    layer.appendChild(c);
  });
}
const cs=document.getElementById('chart-search');
if(cs)cs.addEventListener('input',()=>{const q=cs.value.toLowerCase().trim();document.querySelectorAll('.bubble').forEach(b=>{if(!q){b.classList.remove('dimmed','highlighted');}else if(b.getAttribute('data-title').toLowerCase().includes(q)){b.classList.remove('dimmed');b.classList.add('highlighted');}else{b.classList.add('dimmed');b.classList.remove('highlighted');}});});
''')
out.write('</script>\n</body>\n</html>\n')
out.close()
print(f'index.html generato con {len(jobs)} professioni.')
