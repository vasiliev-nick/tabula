import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()
a = s.index('<article class="book">'); b = s.index('</article>') + len('</article>')
head, body, tail = s[:a], s[a:b], s[b:]
head = head.replace('<title>Интеграл Лебега · Tabula</title>', '<title>Рисунки главы ∅</title>')
# drop the contents and glossary navs (they describe the chapter text)
head = re.sub(r'<nav class="gloss navm".*?</nav>', '', head, flags=re.S)
head = re.sub(r'<nav class="gloss" aria-label="Обозначения главы">.*?</nav>', '', head, flags=re.S)
# every figure, in order, with its section heading
figs = []
for m in re.finditer(r'<h2>(.*?)</h2>|<figure[ >].*?</figure>', body, flags=re.S):
    figs.append('<h2>' + m.group(1) + '</h2>' if m.group(1) else m.group(0))
# keep only headings that have figures after them
out = []
for i, x in enumerate(figs):
    if x.startswith('<h2>') and (i + 1 == len(figs) or figs[i + 1].startswith('<h2>')):
        continue
    out.append(x)
TOK = [('--blue','Синий: основной акцент рисунков (--ether)'),('--coral','Коралловый: тёплый акцент (--warm)'),
       ('--yellow','Жёлтый'),('--green','Зелёный'),('--violet','Фиолетовый'),('--pink','Розовый'),('--sky','Голубой'),
       ('--ink','Чернила'),('--muted','Приглушённый'),('--rule','Оси и сетка'),('--paper','Поле рисунка'),('--fill','Подложка рисунка')]
rows = ''.join(f'<label class="sw"><input type="color" data-t="{t}"><span>{n}</span><code>{t}</code></label>' for t, n in TOK)
lab = '''<article class="book figs">
<header class="ch"><div class="eyebrow">Глава ∅ · Мера и интеграл Лебега</div>
<h1>Рисунки главы</h1>
<p class="lead">Все рисунки главы на одной странице, живые. Цвета справа меняют токены, и рисунки перерисовываются сразу. Набор можно скопировать кнопкой внизу панели.</p></header>
''' + '\n'.join(out) + '''
</article>
<aside class="lab" aria-label="Цвета">
<div class="lab-h">Цвета <button type="button" class="lab-x" aria-label="Свернуть панель">−</button></div>
<div class="lab-b">''' + rows + '''
<div class="lab-a"><button type="button" class="lab-r">Сбросить</button><button type="button" class="lab-c">Скопировать CSS</button></div>
<pre class="lab-o" hidden></pre></div>
</aside>
<script>
(function(){
  const R=document.documentElement,inp=[...document.querySelectorAll('.lab input[type=color]')];
  const cs=()=>getComputedStyle(R);
  const base={};
  function sync(){inp.forEach(i=>{const v=cs().getPropertyValue(i.dataset.t).trim();base[i.dataset.t]=base[i.dataset.t]||v;i.value=/^#[0-9a-f]{6}$/i.test(v)?v:'#000000';});}
  /* --ether and --warm follow the blue and coral pickers, so the canvases pick them up */
  const LINK={'--blue':['--ether'],'--coral':['--warm']};
  function poke(){const t=R.getAttribute('data-theme');if(t)R.setAttribute('data-theme',t);else{R.setAttribute('data-theme','x');R.removeAttribute('data-theme');}}
  inp.forEach(i=>i.addEventListener('input',()=>{R.style.setProperty(i.dataset.t,i.value);(LINK[i.dataset.t]||[]).forEach(k=>R.style.setProperty(k,i.value));poke();}));
  document.querySelector('.lab-r').onclick=()=>{R.removeAttribute('style');poke();setTimeout(sync,30);};
  document.querySelector('.lab-c').onclick=()=>{const o=document.querySelector('.lab-o');
    o.textContent=':root{\\n'+inp.map(i=>'  '+i.dataset.t+':'+i.value.toUpperCase()+';').join('\\n')+'\\n}';o.hidden=false;
    try{navigator.clipboard.writeText(o.textContent);}catch(e){}};
  document.querySelector('.lab-x').onclick=e=>{const l=document.querySelector('.lab');l.classList.toggle('min');e.target.textContent=l.classList.contains('min')?'+':'−';};
  new MutationObserver(()=>{if(!R.getAttribute('style'))setTimeout(sync,30);}).observe(R,{attributes:true,attributeFilter:['data-theme']});
  if(innerWidth<1180){document.querySelector('.lab').classList.add('min');document.querySelector('.lab-x').textContent='+';}
  sync();
})();
</script>
<style>
@media (min-width:1181px){.book.figs{margin-left:max(16px,calc((100vw - 296px - 51rem)/2));margin-right:auto}}
.figs h2{margin-top:3.2rem}
.figs figure{margin:1.4rem 0 2rem}
.lab{position:fixed;right:16px;top:64px;z-index:40;width:264px;max-height:calc(100vh - 80px);overflow:auto;background:var(--paper);border-radius:12px;box-shadow:var(--pop);font-family:var(--font-ui);font-size:.82rem}
.lab-h{display:flex;justify-content:space-between;align-items:center;padding:.7rem .9rem .4rem;font-family:var(--font-display);font-weight:600;font-size:1.05rem}
.lab-x{border:none;background:var(--fill);color:var(--ink);border-radius:6px;width:26px;height:26px;cursor:pointer;font:600 16px/1 var(--font-ui)}
.lab.min .lab-b{display:none}
.lab-b{padding:0 .5rem .7rem}
.sw{display:grid;grid-template-columns:28px 1fr;grid-template-rows:auto auto;column-gap:.6rem;align-items:center;padding:.3rem .4rem;border-radius:8px;cursor:pointer}
.sw:hover{background:var(--fill)}
.sw input{grid-row:1 / span 2;width:28px;height:28px;padding:0;border:none;border-radius:6px;background:none;cursor:pointer}
.sw input::-webkit-color-swatch-wrapper{padding:0}.sw input::-webkit-color-swatch{border:1px solid var(--line);border-radius:6px}
.sw span{color:var(--ink);line-height:1.25}.sw code{color:var(--muted);font-size:.72rem}
.lab-a{display:flex;gap:.4rem;padding:.6rem .4rem 0}
.lab-a button{flex:1;font:500 .8rem var(--font-ui);border-radius:8px;padding:.4rem .5rem;cursor:pointer;border:1px solid var(--line);background:var(--paper);color:var(--ink)}
.lab-a .lab-c{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.lab-o{margin:.6rem .4rem 0;padding:.6rem;background:var(--fill);border-radius:8px;font-size:.72rem;white-space:pre-wrap}
@media (max-width:1180px){.lab{top:auto;bottom:12px;right:12px;left:12px;width:auto;max-height:45vh}}
@media (max-width:1180px){.figs{margin-bottom:80px}}
</style>'''
open(dst, 'w', encoding='utf8').write(head + lab + tail)
print('figures:', sum(1 for x in out if x.startswith('<figure')))
