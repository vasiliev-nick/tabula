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
  --ether:#7352F5; --ether-soft:#F0ECFF; --warm:#F45B3E; --warm-soft:#FFE9E3;
  --desk:#F4F1EB; --fill:#F3EFE8; --fill-2:#E8E3DA; --ink-3:#9A958D;
  --ether-ink:#5B3BE0; --warm-ink:#C7402A;
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
  --ether:#A08BFF; --ether-soft:#2D2841; --warm:#FF8A70; --warm-soft:#3A2621;
  --desk:#191816; --fill:#2C2B28; --fill-2:#38362F; --ink-3:#7C776E;
  --ether-ink:#B5A4FF; --warm-ink:#FF9C85; --blue-ink:#9FB0FF; --green-ink:#6FDCAF;
  --blue-soft:#232B45; --green-soft:#1D3128; --sticky:#3A3219; --sky-soft:#1C3039;
  --lift:0 1px 2px rgba(0,0,0,.3),0 10px 34px rgba(0,0,0,.25); --pop:0 16px 40px rgba(0,0,0,.45); color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#232220; --ink:#EFEBE4; --muted:#A8A296; --rule:#3E3B36;
  --ether:#A08BFF; --ether-soft:#2D2841; --warm:#FF8A70; --warm-soft:#3A2621;
  --desk:#191816; --fill:#2C2B28; --fill-2:#38362F; --ink-3:#7C776E;
  --ether-ink:#B5A4FF; --warm-ink:#FF9C85; --blue-ink:#9FB0FF; --green-ink:#6FDCAF;
  --blue-soft:#232B45; --green-soft:#1D3128; --sticky:#3A3219; --sky-soft:#1C3039;
  --lift:0 1px 2px rgba(0,0,0,.3),0 10px 34px rgba(0,0,0,.25); --pop:0 16px 40px rgba(0,0,0,.45); color-scheme:dark}
'''
s = s.replace(old_tokens, new_tokens)

rep("TB.serif='Literata, Georgia, serif';TB.ui='\"PT Sans Caption\", \"PT Sans\", sans-serif';",
    "TB.serif='Lora, Georgia, serif';TB.ui='Onest, system-ui, sans-serif';")

hero = '''<header class="ch">
  <svg class="hero" viewBox="0 0 240 150" aria-hidden="true">
    <rect x="18" y="112" width="204" height="20" rx="10" fill="var(--yellow)"/>
    <rect x="30" y="88" width="176" height="20" rx="10" fill="var(--green)"/>
    <rect x="50" y="64" width="50" height="20" rx="10" fill="var(--blue)"/>
    <rect x="130" y="64" width="62" height="20" rx="10" fill="var(--blue)"/>
    <rect x="62" y="40" width="26" height="20" rx="10" fill="var(--coral)"/>
    <rect x="146" y="40" width="32" height="20" rx="10" fill="var(--pink)"/>
    <path d="M10 136 C 40 128, 44 30, 74 30 S 104 88, 115 88 S 140 22, 162 24 S 200 100, 232 134" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linecap="round"/>
    <circle cx="74" cy="30" r="5" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.6"/>
  </svg>'''
rep('<header class="ch">', hero)

css = open(css_path, encoding='utf8').read()
tail = '''<script>
/* Tabula: each numbered statement gets its kind, so that the card takes the colour of its kind. */
(function(){var K={'Определение':'def','Теорема':'thm','Факт':'thm','Лемма':'lem','Предложение':'lem','Следствие':'cor'};
document.querySelectorAll('.stmt>.lbl').forEach(function(l){var w=l.textContent.trim().split(/\\s+/)[0];l.parentNode.dataset.k=K[w]||'thm';});})();
</script>
<style id="tabula">
''' + css + '''
</style>
</body></html>'''
rep('\n</body></html>', '\n' + tail)
open(dst, 'w', encoding='utf8').write(s)
print('ok', len(s))
