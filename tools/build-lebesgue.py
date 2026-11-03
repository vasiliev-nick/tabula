import sys, re
src, dst, css_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:60], s.count(old))
    s = s.replace(old, new)

rep('<title>Мера и интеграл Лебега. Глава ∅</title>', '<title>Интеграл Лебега · Tabula</title>')
rep('family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&family=PT+Sans+Caption:wght@400;700',
    'family=Lora:ital,wght@0,500;0,600;1,500&family=Onest:wght@400;500;600;700')

old_tokens = s[s.index(':root{\n  --paper:#f5eee0'):s.index('body{background:var(--paper)')]
new_tokens = ''':root{
  --paper:#FFFEFB; --ink:#1E1C19; --muted:#6E6A63; --rule:#DDD7CC;
  --ether:#4F6BFF; --ether-soft:#EEF1FF; --warm:#F45B3E; --warm-soft:#FFE9E3;
  --desk:#F4F1EB; --fill:#F6F3EE; --fill-2:#E8E3DA; --ink-3:#9A958D; --line:#ECE7DF; --cream:#FCF7EA;
  --ether-ink:#2C47D6; --warm-ink:#C7402A;
  --yellow:#FFD23F; --blue:#4F6BFF; --coral:#FF6F59; --green:#2FBF85; --violet:#9A6BFF; --pink:#FF7EB6; --sky:#3CC3F2;
  --blue-ink:#2C47D6; --green-ink:#12784F; --blue-soft:#EAEEFF; --green-soft:#E2F5EC; --sticky:#FFF3C2; --sky-soft:#E3F5FC;
  --lift:0 1px 2px rgba(40,30,10,.05),0 10px 34px rgba(40,30,10,.06);
  --pop:0 2px 6px rgba(40,30,10,.07),0 16px 40px rgba(40,30,10,.13);
  --font-body:"Onest", system-ui, sans-serif;
  --font-ui:"Onest", system-ui, sans-serif;
  --font-display:"Lora", Georgia, serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#232220; --ink:#EFEBE4; --muted:#A8A296; --rule:#3E3B36;
  --ether:#8EA0FF; --ether-soft:#252B42; --warm:#FF8A70; --warm-soft:#3A2621;
  --desk:#191816; --fill:#2A2926; --fill-2:#38362F; --ink-3:#7C776E; --line:#34322E; --cream:#2E2A20;
  --ether-ink:#A9B7FF; --warm-ink:#FF9C85; --blue-ink:#9FB0FF; --green-ink:#6FDCAF;
  --blue-soft:#232B45; --green-soft:#1D3128; --sticky:#3A3219; --sky-soft:#1C3039;
  --lift:0 1px 2px rgba(0,0,0,.3),0 10px 34px rgba(0,0,0,.25); --pop:0 16px 40px rgba(0,0,0,.45); color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#232220; --ink:#EFEBE4; --muted:#A8A296; --rule:#3E3B36;
  --ether:#8EA0FF; --ether-soft:#252B42; --warm:#FF8A70; --warm-soft:#3A2621;
  --desk:#191816; --fill:#2A2926; --fill-2:#38362F; --ink-3:#7C776E; --line:#34322E; --cream:#2E2A20;
  --ether-ink:#A9B7FF; --warm-ink:#FF9C85; --blue-ink:#9FB0FF; --green-ink:#6FDCAF;
  --blue-soft:#232B45; --green-soft:#1D3128; --sticky:#3A3219; --sky-soft:#1C3039;
  --lift:0 1px 2px rgba(0,0,0,.3),0 10px 34px rgba(0,0,0,.25); --pop:0 16px 40px rgba(0,0,0,.45); color-scheme:dark}
'''
s = s.replace(old_tokens, new_tokens)

rep("TB.serif='Literata, Georgia, serif';TB.ui='\"PT Sans Caption\", \"PT Sans\", sans-serif';",
    "TB.serif='Lora, Georgia, serif';TB.ui='Onest, system-ui, sans-serif';")

hero = '''<header class="ch">
  <svg class="hero" viewBox="0 0 240 150" aria-hidden="true">
    <rect x="22" y="116" width="196" height="12" rx="3" fill="var(--yellow)"/>
    <rect x="34" y="98" width="170" height="12" rx="3" fill="var(--green)"/>
    <rect x="50" y="80" width="50" height="12" rx="3" fill="var(--blue)"/>
    <rect x="130" y="80" width="62" height="12" rx="3" fill="var(--blue)"/>
    <rect x="62" y="62" width="26" height="12" rx="3" fill="var(--coral)"/>
    <rect x="146" y="62" width="32" height="12" rx="3" fill="var(--coral)"/>
    <path d="M12 134 C 40 128, 46 40, 75 40 S 103 92, 115 92 S 140 30, 162 32 S 200 104, 230 134" fill="none" stroke="var(--ink)" stroke-width="2" stroke-linecap="round"/>
    <line x1="12" y1="134.5" x2="230" y2="134.5" stroke="var(--ink-3)" stroke-width="1"/>
  </svg>'''
rep('<header class="ch">', hero)

for a,b2 in [('Фиолетовая','Синяя'),('фиолетовая','синяя'),('фиолетовым','синим'),('Фиолетовый','Синий')]:
    s=s.replace(a,b2)
assert 'иолет' not in s
# new control icons
import re
ic_list='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 7h14M5 12h9M5 17h11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ic_gloss='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><text x="12" y="17" text-anchor="middle" font-family="Lora, Georgia, serif" font-style="italic" font-weight="600" font-size="17" fill="currentColor">α</text></svg>'
ic_theme='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><g class="moon"><path d="M19.5 14.2A7.5 7.5 0 0 1 9.8 4.5a7.5 7.5 0 1 0 9.7 9.7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></g><g class="sun" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/></g></svg>'
n0=len(s)
s=re.sub(r'(<button class="gbtn" type="button" aria-label="Содержание"[^>]*>)<svg.*?</svg>',lambda m:m.group(1)+ic_list,s,count=1)
s=re.sub(r'(<button class="gbtn" type="button" aria-label="Обозначения"[^>]*>)<svg.*?</svg>',lambda m:m.group(1)+ic_gloss,s,count=1)
s=re.sub(r'(<button class="tbtn"[^>]*>)<svg.*?</svg>',lambda m:m.group(1)+ic_theme,s,count=1)
assert s.count('class="moon"')==1 and 'M5 7h14M5 12h9' in s and '>α</text>' in s
# Tabula: selective bright colours in the figures
def rr(a,b2,n=1):
    global s
    assert s.count(a)==n,(a,s.count(a))
    s=s.replace(a,b2)
rr("TB.tok=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();",
   "TB.tok=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();\n  TB.pal=i=>TB.tok(['--yellow','--green','--blue','--coral','--violet','--pink','--sky'][((i%7)+7)%7]);")
rr("for(let k=1;k<=K;k++){const lv=k*h;let run=-1;c.fillStyle=TB.rgba(eth,k%2?0.30:0.42);",
   "for(let k=1;k<=K;k++){const lv=k*h;let run=-1;c.fillStyle=TB.rgba(TB.pal(k-1),0.62);")
rr("c.fillStyle=TB.rgba(eth,0.18+0.62*(1-(m-1)/7));","c.fillStyle=TB.rgba(TB.pal(m-1),0.78);")
rr("const y=top+k*rh,col=TB.mixh(warm,eth,K?k/K:0);","const y=top+k*rh,col=TB.pal(k);")
rr("const cols=[muted,warm,TB.mixh(warm,eth,0.5),eth];","const cols=[muted,TB.tok('--coral'),TB.tok('--green'),eth];")
css = open(css_path, encoding='utf8').read()
tail = '''<script>
/* Tabula: each numbered statement gets its kind, so that the card takes the colour of its kind. */
(function(){var K={'Определение':'def','Теорема':'thm','Факт':'thm','Лемма':'lem','Предложение':'lem','Следствие':'cor'};
document.querySelectorAll('.stmt>.lbl').forEach(function(l){var w=l.textContent.trim().split(/\\s+/)[0];l.parentNode.dataset.k=K[w]||'thm';});})();
/* Tabula: pills in the contents take the colour of their kind. */
(function(){var P={'Опр.':'def','Теор.':'thm','Факт':'thm','Лемма':'lem','Предл.':'lem','След.':'lem','Упр.':'ex','Вопр.':'ex'};document.querySelectorAll('.nlist a.npill').forEach(function(a){var w=a.textContent.trim().split(/\\s+/)[0];if(P[w])a.dataset.k=P[w];});})();
</script>
<style id="tabula">
''' + css + '''
</style>
</body></html>'''
rep('\n</body></html>', '\n' + tail)
open(dst, 'w', encoding='utf8').write(s)
print('ok', len(s))
