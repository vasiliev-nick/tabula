import sys, re
src, dst, title, css_path, lebsrc, mode, off = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], int(sys.argv[7])
NEW = mode == 'new'
title = title.replace('_', ' ')
import os
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf8').read()
css = open(css_path, encoding='utf8').read()
L = open(lebsrc, encoding='utf8').read()
new_tokens = L[L.index(':root{\n  --paper:#FFFEFB'):L.index('body{background:var(--paper)')]
new_tokens = new_tokens.replace('--sky:#3CC3F2;', '--sky:#3CC3F2; --sage:#1FA472;').replace('--green-ink:#6FDCAF;', '--green-ink:#6FDCAF; --sage:#6FDCAF;')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
if not NEW:
    pass
elif 'id="tabula"' in s:   # already restyled (chapter ∅, part 1): swap in the current stylesheet
    a = s.index('<style id="tabula">'); b = s.index('</style>', a)
    s = s[:a] + '<style id="tabula">\n' + css + '\n' + s[b:]
else:
    rep('family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&family=PT+Sans+Caption:wght@400;700',
        'family=Lora:ital,wght@0,500;0,600;1,500&family=Onest:wght@400;500;600;700')
    old = s[s.index(':root{\n  --paper:#f5eee0'):s.index('body{background:var(--paper)')]
    s = s.replace(old, new_tokens)
    rep("TB.serif='Literata, Georgia, serif';TB.ui='\"PT Sans Caption\", \"PT Sans\", sans-serif';",
        "TB.serif='Lora, Georgia, serif';TB.ui='Onest, system-ui, sans-serif';", s.count("TB.serif='Literata"))
    for a, b in [('Фиолетовая','Синяя'),('фиолетовая','синяя'),('фиолетовый','синий'),('фиолетовые','синие'),('фиолетовым','синим'),
                 ('Фиолетовые','Синие'),('Фиолетовый','Синий'),('фиолетового','синего')]:
        s = s.replace(a, b)
    assert 'иолетов' not in s
    s = s.replace('\n</body></html>', '\n<style id="tabula">\n' + css + '\n</style>\n</body></html>')
s = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', s, count=1)
s = s.replace("V.intro=function(st,redraw){if(TB.reduced()||st.introDone)return;", "V.intro=function(st,redraw){return;")
PAIRCSS = ''
if NEW:
    PAL={'blue':['#4F6BFF','#EAEEFF','#2C47D6'],'green':['#22B07A','#E0F5EC','#12784F'],'violet':['#8A5CFF','#EFE8FF','#5B33C9'],'sky':['#1FB2EA','#E0F4FC','#0B7FAD'],
         'coral':['#FF6F59','#FFE9E3','#C7402A'],'yellow':['#FFC21A','#FFF4CC','#B37F00'],'pink':['#FF6BA8','#FFE6F0','#C2306F']}
    for c,(m,soft,ink) in PAL.items():
        PAIRCSS += f'figure[data-pal^="{c}-"]{{--ether:{m};--ether-soft:{soft};--ether-ink:{ink};--tint-bg:color-mix(in srgb,{soft} 65%,#fff)}}\n'
        PAIRCSS += f'figure[data-pal$="-{c}"]{{--warm:{m};--warm-soft:{soft};--warm-ink:{ink}}}\n'
        PAIRCSS += f':root[data-theme="dark"] figure[data-pal^="{c}-"]{{--ether-soft:color-mix(in srgb,{m} 22%,var(--paper));--tint-bg:color-mix(in srgb,{m} 8%,var(--paper))}}\n'
        PAIRCSS += f':root[data-theme="dark"] figure[data-pal$="-{c}"]{{--warm-soft:color-mix(in srgb,{m} 22%,var(--paper))}}\n'
    D = '\n'.join(l.replace(':root[data-theme="dark"] ', ':root:not([data-theme="light"]) ') for l in PAIRCSS.split('\n') if l.startswith(':root'))
    PAIRCSS += '@media (prefers-color-scheme: dark){' + D + '}\n'
    PAIRCSS += 'figure[data-pal] canvas{background:var(--tint-bg)}\n'
head = '<style>article.book{position:absolute!important;left:-99999px!important;top:0;width:44rem;visibility:hidden!important}.gloss,.tbtn{display:none!important}</style>'
if NEW:
    head += '<script>document.documentElement.dataset.palOffset="%d";\n' % off + open(os.path.join(HERE,'juice.js'),encoding='utf8').read() + '\n</script>'
i = s.index('<body>') + len('<body>')
s = s[:i] + head + s[i:]
rep('<article class="book">', '<article class="book mathjax_ignore" aria-hidden="true">')
s = s.replace('<nav class="gloss', '<nav class="mathjax_ignore gloss')
grid = '''<style>''' + PAIRCSS + '''</style>
<main id="figgrid" class="figgrid" aria-label="Рисунки"></main>
<script>
/* Figures page: every figure leaves the (hidden) text and goes into one grid, with its listeners intact. */
(function(){
  var g=document.getElementById('figgrid');
  document.querySelectorAll('article.book figure').forEach(function(f){g.appendChild(f);});
  /* each figure takes its colour pair; colour words in the text follow the cold colour */
  if(window.TabulaPal){var E={soft:{'ий':'ий','яя':'яя','ее':'ее','ие':'ие','им':'им','его':'его','ей':'ей','их':'их','юю':'юю','ими':'ими','ему':'ему','ем':'ем'},
      hard:{'ий':'ый','яя':'ая','ее':'ое','ие':'ые','им':'ым','его':'ого','ей':'ой','их':'ых','юю':'ую','ими':'ыми','ему':'ому','ем':'ом'}};
    E.hardo=Object.assign({},E.hard,{'ий':'ой'});
    [].forEach.call(g.querySelectorAll('figure'),function(f){TabulaPal.assign(f);var nm=TabulaPal.NAMES[f.dataset.pal.split('-')[0]];if(!nm||nm[0]==='син')return;
      var w=document.createTreeWalker(f,NodeFilter.SHOW_TEXT),n;while(n=w.nextNode()){var t=n.nodeValue;if(t.indexOf('ин')<0)continue;
        n.nodeValue=t.replace(/([Сс])ин(ий|яя|ее|ие|ими|им|его|ей|их|юю|ему|ем)(?![а-яё])/g,function(m,c,e){var r=nm[0]+E[nm[1]][e];return c==='С'?r[0].toUpperCase()+r.slice(1):r;});}});TabulaPal.fixAll();}
  g.addEventListener('click',function(e){var c=e.target.closest('figcaption');if(c)c.classList.toggle('open');});
  function post(){try{parent.postMessage({figH:Math.ceil(g.getBoundingClientRect().bottom+scrollY+12),src:location.pathname},'*');}catch(e){}}
  new ResizeObserver(post).observe(g);addEventListener('load',post);post();
  addEventListener('message',function(e){var t=e.data&&e.data.theme;if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}else if(t==='auto'){document.documentElement.removeAttribute('data-theme');}});
})();
</script>
<style>
html,body{background:transparent!important}
body{padding:4px 0 8px!important;margin:0}
.gloss,.tbtn,article.book{display:none!important}
.figgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;align-items:start;font-size:14px;line-height:1.45}
.figgrid figure{margin:0!important;padding:12px 12px 10px;background:var(--paper);border:1px solid var(--line,var(--rule));border-radius:6px;min-width:0;max-width:none!important}
.figgrid figure .fig1.sq{max-width:none}
.figgrid canvas{border-radius:4px}
.figgrid .controls{font-size:.78rem;gap:.5rem .9rem;margin-top:.55rem}
.figgrid .controls input[type=range]{width:96px}
.figgrid .fx{font-size:.84rem;margin-top:.45rem}
.figgrid .ro{margin-top:.4rem}
.figgrid .rr{grid-template-columns:minmax(0,1fr) 2.8rem}.figgrid .rl{grid-column:1/-1;text-align:left;font-size:.82rem;margin:.2rem 0 0}
.figgrid figcaption{font-size:.74rem;line-height:1.4;margin-top:.5rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
.figgrid figcaption.open{display:block}
.figgrid figcaption ul{margin:.2rem 0;padding-left:1rem}
@media (min-width:700px){.figgrid figure:has(.boxfig,.hier,.modes){grid-column:span 2}}
.figgrid .svgwrap{overflow:hidden}.figgrid .boxfig,.figgrid .hier,.figgrid .modes{min-width:0!important}
</style>
'''
rep('</article>', '</article>\n<!--GRID-->')
# the grid must come after every figure script, so it goes right before the stylesheet at the end
s = s.replace('<!--GRID-->', '')
i = s.rindex('<style id="tabula">') if NEW else s.rindex('</body></html>')
s = s[:i] + grid + s[i:]
open(dst, 'w', encoding='utf8').write(s)
print(dst, 'figures', s.count('<figure'))
