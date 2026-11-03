LEB=/home/claude/tabula/explorations/lebesgue-ch0.html; T=/root/.claude/projects/-home-claude-tabula/4fd00abf-c932-5f05-b652-915468aedcb5/tool-results
mkdir -p grid/orig
i=0
while read name src orig title; do
  python3 figs.py $src grid/$name.html "Рисунки · $title" tabula-book.css $LEB new $i
  python3 figs.py $orig grid/orig/$name.html "Было · $title" tabula-book.css $LEB orig 0
  i=$((i+3))
done <<LIST
lebesgue-1 $LEB $T/artifact-7f25361c-1793577184-4081.html ∅,_часть_1
lebesgue-2 $T/artifact-14c27b4a-1793577185-b7e0.html $T/artifact-14c27b4a-1793577185-b7e0.html ∅,_часть_2
lebesgue-3 $T/artifact-98bbfc85-1793577186-c0fb.html $T/artifact-98bbfc85-1793577186-c0fb.html ∅,_часть_3
curves $T/artifact-3532e014-1793577187-1481.html $T/artifact-3532e014-1793577187-1481.html ∇
vectors $T/artifact-06aba8f5-1793577188-ad50.html $T/artifact-06aba8f5-1793577188-ad50.html ∠
gauss-1 $T/artifact-2dd39bcf-1793577189-b0aa.html $T/artifact-2dd39bcf-1793577189-b0aa.html 𝒩,_часть_1
xent $T/artifact-33075d3c-1793577183-ec55.html $T/artifact-33075d3c-1793577183-ec55.html Кросс-энтропия
optim $T/artifact-f44aa49e-1793624680-732c.html $T/artifact-f44aa49e-1793624680-732c.html Оптимизаторы
LIST
