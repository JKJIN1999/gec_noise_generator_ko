import sys
sys.path.append("./")
sys.path.append("./src/")
sys.path.append("./src/gecnk/")
from g2pk import G2p
from mecab import MeCab
from wisekmapy.wisekma import Wisekma
from tokenizer import *



black = Wisekma()
mec = MeCab()
g2p = G2p()

print(round(2342.234234,2))
# print(g2p("원래"))
text = "국화는 아름답다."
# print(black.pos(text))
print(mec.pos("라고 했다"))
print(g2p("국화"))


print(len("라고 했다"))
