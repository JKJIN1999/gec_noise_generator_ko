import sys
from wisekmapy import Wisekma

black = Wisekma()

if __name__ == '__main__':
    print("input string...")
    for line in sys.stdin:
        res = black.pos(line, join=True)
        print(">> " + " + ".join(res))