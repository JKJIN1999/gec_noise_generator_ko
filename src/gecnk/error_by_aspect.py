from constant import *
from datasets import *
from tokenizer import *
import random
import os
from g2pk import G2p
g2p = G2p()


class ErrorByAspect:

    def om_error(words):

        def remove_josa(word):
            for token in word[0]:
                if token[1][0] == "J" and len(word[0]) > 1:
                    token[0] = ""
                    word[1][0] = "OM"
                    return word
            return word

        def middle_shiot_error(word):
            for token in word[0]:
                result = []
                if len(list(token[0])) >= 2 and token[1][0] == "N":
                    for character in token[0]:
                        if hangul_jamo.is_syllable(character):
                            jamos = list(
                                hangul_jamo.decompose_syllable(character))
                            if jamos[2] == "ㅅ":
                                jamos[2] = None
                                character = hangul_jamo.compose_jamo_characters(
                                    jamos[0], jamos[1], jamos[2])
                                word[1][0] = "OM"
                        result.append(character)
                if word[1][0] == "OM":
                    token[0] = "".join(result)
                    return word
            return word

        def delete_final_consonant(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if hangul_jamo.is_syllable(character):
                        jamos = list(hangul_jamo.decompose_syllable(character))
                        if jamos[2] == "ㅎ":
                            jamos[2] = None
                            character = hangul_jamo.compose_jamo_characters(
                                jamos[0], jamos[1], jamos[2])
                            word[1][0] = "OM"
                    result.append(character)
                if word[1][0] == "OM":
                    token[0] = "".join(result)
                    return word
            return word

        def convert_josa(word):
            for token in word[0]:
                if token[1][0] == "J":
                    for josa_list in JOSA_CONVERT_LIST:
                        if token[0] in josa_list:
                            new_josa = random.choice(
                                [x for x in josa_list if x != token[0]])
                            if len(new_josa) < len(token[0]):
                                word[1][0] = "OM"
                            token[0] = new_josa
                            return word
            return word

        functions = [remove_josa, middle_shiot_error,
                     delete_final_consonant, convert_josa]

        for word in words:
            func = random.choice(functions)
            if word[1][0] == "type":
                word = func(word)
        return words

    def mif_error(words):

        def singular_vowel_error(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if hangul_jamo.is_syllable(character):
                        jamos = list(hangul_jamo.decompose_syllable(character))
                        if jamos[1] in ["ㅐ", "ㅔ"]:
                            jamos[1] = "ㅔ" if jamos[1] == "ㅐ" else "ㅐ"
                            character = (hangul_jamo.compose_jamo_characters(
                                jamos[0], jamos[1], jamos[2]))
                            word[1][0] = "MIF"
                    result.append(character)
                if word[1][0] == "MIF":
                    token[0] = "".join(result)
                    return word
            return word

        def diphthong_vowel_error(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if hangul_jamo.is_syllable(character):
                        jamos = list(hangul_jamo.decompose_syllable(character))
                        if jamos[1] in ["ㅖ", "ㅔ"]:
                            jamos[1] = "ㅖ" if jamos[1] == "ㅔ"else "ㅔ"
                            word[1][0] = "MIF"
                        elif jamos[1] in ["ㅙ", "ㅚ"]:
                            jamos[1] = "ㅙ" if jamos[1] == "ㅚ"else "ㅚ"
                            word[1][0] = "MIF"
                        character = (hangul_jamo.compose_jamo_characters(
                            jamos[0], jamos[1], jamos[2]))
                    result.append(character)
                if word[1][0] == "MIF":
                    token[0] = "".join(result)
                    return word
            return word

        def busa_error(word):
            busa_one = ["이", "히"]
            busa_two = ["마져", "마저"]
            for token in word[0]:
                if token[1][0] == "M":
                    if token[0] in busa_two:
                        token[0] = "마져" if token[0] == "마저" else "마저"
                        word[1][0] = "MIF"
                        return word
                    elif token[1] == "MAG":
                        if token[0][-1] in busa_one:
                            characters = list(token[0])
                            characters[-1] = "이" if characters[-1] == "히" else "히"
                            token[0] = ''.join(characters)
                            word[1][0] = "MIF"
                            return word
            return word

        def add_final_consonant(word):
            previous_token = -1
            convert_previous = False
            for token in word[0]:
                result = []
                if token[1] == "EC":
                    if ''.join(list(token[0][:2])) == "으려":
                        result = ["을", "려"]
                        if len(token[0]) > 2:
                            for x in list(token[0][2:]):
                                result.append(x)
                        word[1][0] = "MIF"
                    elif previous_token > -1:
                        characters = list(token[0])
                        previous_token_characters = list(
                            word[0][previous_token][0])
                        if characters[0] == "려" and not list(hangul_jamo.decompose_syllable(previous_token_characters[-1]))[2]:
                            jamos = list(hangul_jamo.decompose_syllable(
                                previous_token_characters[-1]))
                            jamos[2] = "ㄹ"
                            previous_token_characters[-1] = hangul_jamo.compose_jamo_characters(
                                jamos[0], jamos[1], jamos[2])
                            word[1][0] = "MIF"
                            convert_previous = True
                            for x in previous_token_characters:
                                result.append(x)
                    if word[1][0] == "MIF":
                        if not convert_previous:
                            token[0] = "".join(result)
                            return word
                        else:
                            word[0][previous_token][0] = "".join(result)
                            return word
                previous_token += 1
            return word

        def typical_final_consonant(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if character in ["않", "안"]:
                        character = "않" if character == "안" else "안"
                        word[1][0] = "MIF"
                    elif character in ["많", "만"]:
                        character = "많" if character == "만" else "만"
                        word[1][0] = "MIF"
                    result.append(character)
                if word[1][0] == "MIF":
                    token[0] = "".join(result)
                    return word
            return word

        def phonetic_first_error(word):
            correct_phonetic, error_phonetic = phonetic_data()
            for token in word[0]:
                for phonetic in correct_phonetic:
                    if phonetic == token[0][0] and token[1][0] == "N" and len(token[0]) >= 2:
                        characters = list(token[0])
                        characters[0] = random.choice(
                            error_phonetic[correct_phonetic.index(phonetic)])
                        token[0] = "".join(characters)
                        word[1][0] = "MIF"
                        return word
            return word

        def overlapping_sound_error(word):
            for token in word[0]:
                characters = list(token[0])
                if len(token[0]) >= 2 and token[0][0] == token[0][1]:
                    if len(characters) == 2 and hangul_jamo.is_syllable(characters[1]):
                        jamos_one = list(
                            hangul_jamo.decompose_syllable(characters[0]))
                        jamos_two = list(
                            hangul_jamo.decompose_syllable(characters[1]))
                        if jamos_one[0] == jamos_two[0]:
                            for key in DUEN_SORI_DIC:
                                if jamos_two[0] == key:
                                    jamos_two[0] = DUEN_SORI_DIC[key]
                                    characters[1] = (
                                        hangul_jamo.compose_jamo_characters(jamos_two[0], jamos_two[1], jamos_two[2]))
                                    token[0] = "".join(characters)
                                    word[1][0] = "MIF"
                                    return word
            return word

        def convert_final_consonant(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if hangul_jamo.is_syllable(character):
                        jamos = list(hangul_jamo.decompose_syllable(character))
                        if jamos[2]:
                            for key, value in FINAL_CONSONANT_CONVERT_DIC.items():
                                jamos = list(
                                    hangul_jamo.decompose_syllable(character))
                                if jamos[2] == key:
                                    character = (hangul_jamo.
                                                 compose_jamo_characters(jamos[0], jamos[1], random.choice(value)))
                                    word[1][0] = "MIF"
                                elif jamos[2] in value and len(value) > 1:
                                    character = (hangul_jamo.
                                                 compose_jamo_characters(jamos[0], jamos[1], random.choice([x for x in value if x != jamos[2]])))
                                    word[1][0] = "MIF"
                    result.append(character)
                if word[1][0] == "MIF":
                    token[0] = "".join(result)
                    return word
            return word

        def affix_error(word):
            # 토큰의 행태소 품사가 "X"로 시작하면 율>률 또는 양>량 식으로 바꿔준다
            for token in word[0]:
                if token[1][0] == "X":
                    characters = list(token[0])
                    if characters[-1] in ["율", "률"]:
                        characters[-1] = "율" if characters[-1] == "률" else "률"
                        word[1][0] = "MIF"
                        token[0] = ''.join(characters)
                        return word
                    elif characters[-1] in ["양", "량"]:
                        characters[-1] = "양" if characters[-1] == "량" else "량"
                        word[1][0] = "MIF"
                        token[0] = ''.join(characters)
                        return word
            return word

        def g2p_error(word):
            text = converge_word(word, "source")
            isHangul = True
            for character in text:
                if not hangul_jamo.is_syllable(character):
                    isHangul = False
                    break
            word_g2p = g2p(text)
            if word_g2p != text and len(word_g2p) == len(text) and isHangul:
                start = 0
                word[1][0] = "MIF"
                for token in word[0]:
                    token_len = len(token[0])
                    token[0] = word_g2p[start:start + token_len]
                    start += token_len
                return word
        return word

        functions = [affix_error, convert_final_consonant, overlapping_sound_error, phonetic_first_error,
                     typical_final_consonant, add_final_consonant, busa_error, diphthong_vowel_error, singular_vowel_error, g2p_error]

        for word in words:
            func = random.choice(functions)
            if word[1][0] == "type":
                word = func(word)
        return words

    def rep_error(words):

        def convert_josa(word):
            for token in word[0]:
                if token[1][0] == "J":
                    for josa_list in JOSA_CONVERT_LIST:
                        if token[0] in josa_list:
                            new_josa = random.choice(
                                [x for x in josa_list if x != token[0]])
                            if len(token[0]) == len(new_josa):
                                check_josa = [token[0], new_josa]
                                if set(check_josa).issubset(["에", "께", "의"]) or set(check_josa).issubset(["이", "가"]) or set(check_josa).issubset(["처럼", "마냥"]):
                                    word[1][0] = "REP"
                                    token[0] = new_josa
                                    return word
            return word

        def diphthong_vowel_error(word):
            for token in word[0]:
                result = []
                characters = list(token[0])
                for character in characters:
                    if character in ["의", "이"]:
                        character = "의" if character == "이" else "이"
                        word[1][0] = "REP"
                    result.append(character)
                if word[1][0] == "REP":
                    token[0] = "".join(result)
                    return word
            return word

        functions = [convert_josa, diphthong_vowel_error]

        for word in words:
            func = random.choice(functions)
            if word[1][0] == "type":
                word = func(word)
        return words

    def add_error(words):
        for word in words:
            if word[1][0] == "type":
                for token in word[0]:
                    if token[1][0] == "J":
                        for josa_list in JOSA_CONVERT_LIST:
                            if token[0] in josa_list:
                                new_josa = random.choice(
                                    [x for x in josa_list if x != token[0]])
                                if len(new_josa) > len(token[0]):
                                    word[1][0] = "ADD"
                                    token[0] = new_josa
                                    break
                        if word[1][0] == "type":
                            break
        return words

    def s_add_error(words):
        for word in words:
            if word[1][0] == "type":
                for token_num in range(1, len(word[0])-1):
                    token_tag = word[0][token_num][1]
                    prev_token_tag = word[0][token_num - 1][1]
                    # 가장 흔한 오류인 조사 또는 접사를 띄어써서 생기는 오류
                    if token_tag[0] == "J" or token_tag == [a for a in SPACING_ADD_DIC] or prev_token_tag == "XPN":
                        word[1][0] = "S_ADD"
                        word[0][token_num][0] = " " + \
                            str(word[0][token_num][0])
        return words

    def s_del_error(words):
        ignore_next = False
        remove_list = []
        for words_count in range(0, len(words)-1):
            if words[words_count][1][0] == "type" and not ignore_next:
                # front word last token tag
                front_word_tag = words[words_count][0][-1][1]
                # back word first token tag
                back_word_tag = words[words_count + 1][0][0][1]
                for key, value in SPACING_DEL_DIC.items():
                    if front_word_tag == key and back_word_tag in value:
                        text = ""
                        words[words_count][0][-1][2] += " "
                        words[words_count][0].extend(words[words_count+1][0])
                        words[words_count][1][0] = "S_DEL"
                        remove_list.append(words[words_count + 1])
                        ignore_next = True
            else:
                ignore_next = False
        for i in remove_list:
            words.remove(i)
        return words
