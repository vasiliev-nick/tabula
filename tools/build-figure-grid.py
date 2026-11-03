import sys, re
src, dst, title, css_path, lebsrc = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
s = open(src, encoding='utf8').read()
css = open(css_path, encoding='utf8').read()
L = open(lebsrc, encoding='utf8').read()
new_tokens = L[L.index(':root{\n  --paper:#FFFEFB'):L.index('body{background:var(--paper)')]
new_tokens = new_tokens.replace('--sky:#3CC3F2;', '--sky:#3CC3F2; --sage:#1FA472;').replace('--green-ink:#6FDCAF;', '--green-ink:#6FDCAF; --sage:#6FDCAF;')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
if 'id="tabula"' in s:   # already restyled (chapter ∅, part 1): swap in the current stylesheet
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
rep('<article class="book">', '<article class="book mathjax_ignore" aria-hidden="true">')
s = s.replace('<nav class="gloss', '<nav class="mathjax_ignore gloss')
grid = '''<main id="figgrid" class="figgrid" aria-label="Рисунки"></main>
<script>
/* Figures page: every figure leaves the (hidden) text and goes into one grid, with its listeners intact. */
(function(){
  var g=document.getElementById('figgrid');
  document.querySelectorAll('article.book figure').forEach(function(f){g.appendChild(f);});
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
.figgrid figure{margin:0!important;padding:12px 12px 10px;background:var(--paper);border:1px solid var(--line);border-radius:6px;min-width:0;max-width:none!important}
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
i = s.rindex('<style id="tabula">')
s = s[:i] + grid + s[i:]
open(dst, 'w', encoding='utf8').write(s)
print(dst, 'figures', s.count('<figure'))
