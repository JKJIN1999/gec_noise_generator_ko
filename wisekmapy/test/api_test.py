from wisekmapy import Wisekma

black = Wisekma()

test = '롱테이크로 이루어진 영화임에도 불구하고 지루하지 않은 세심한 연출'
res = black.pos(test, join=True)
print(">> " + " + ".join(res))

res = black.pos(test)
print(res)

res = black.nouns(test, nbest=5, tagging=False)
print(res)

res = black.morph(test, nbest=5)
print(res)