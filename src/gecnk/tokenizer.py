from constant import *
from log_manage import __get_logger
import hangul_jamo
from mecab import MeCab
import sys
sys.path.append("./")
from wisekmapy.wisekma import Wisekma
logger = __get_logger()


""" 띄어쓰기 단위로 토크나이징 및 각 토큰에 시작과 끝을 부여
    token은 리스트로 네가지 정보다 담기는데 [[어절변형,품사,어절원형], 오류양상, 시작점, 끝점] 
    현재 mecab을 위해 빌드된 버젼이고 black으로 실행할 경우 오류가 존재 할 가능성이 존재합니다."""


def tokenize_words(words, tokenizer_type):
    mec = MeCab()
    words_list = []
    count = 0
    if tokenizer_type == "mecab":
        tok = MeCab()
    elif tokenizer_type == "black":
        tok = Wisekma()
    else:
        logger.error("Unknown tokenizer name : {}".format(tokenizer_type))
        raise SystemExit
    for word in words:
        word_list = []
        word_tokens = []
        tokens = tok.pos(word)
        for token in tokens:
            token = list(token)
            token.append(token[0])
            word_tokens.append(token)
        word_list.append(word_tokens)
        word_list.append(["type", 0, 0])
        words_list.append(word_list)
    return words_list


def tagging(words):
    mec = MeCab()


def converge_word(word, word_type):
    converged_text = ""
    position = 2 if word_type == "target" else 0
    for token in word[0]:
        converged_text += str(token[position])
    return converged_text


def converge_words(words):
    converged_text = ""
    for word in words:
        word_text = ""
        for token in word[0]:
            word_text += str(token[0])
        if word_text != "":
            converged_text += word_text + " "
    return converged_text.strip()


def add_position(words):
    position = 0
    for word in words:
        word[1][1] = position
        for token in word[0]:
            if word[1][0] == "type":
                position += len(token[2])
            else:
                position += len(token[0])
        word[1][2] = position
        position += 1
    return words
