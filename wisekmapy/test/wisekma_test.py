#! /usr/bin/python
# -*- coding: utf-8 -*-
from wisekmapy import Wisekma

# Need knowlege, lib directory
black = Wisekma()
black.setCharset("utf-8")


def analyze(inputfile, outputfile):
    fw = open(outputfile, 'w', encoding='utf-8')
    with open(inputfile, 'r', encoding='utf-8') as f:
        for line in f:
            res = black.pos(line, join=True)
            fw.write(" + ".join(res) + "\n")

    fw.close()


if __name__ == '__main__':
    # import timeit
    # input =
    # output = './result.txt'
    # print(timeit.timeit("analyze('./data/ratings-10k.txt',  './result.txt')", setup="from __main__ import analyze", number=10))
    import time
    input = './data/ratings-100k.txt'
    output = './result.txt'
    start_time = time.time()
    analyze(input, output)
    print('analyzed time %s' % (time.time() - start_time))