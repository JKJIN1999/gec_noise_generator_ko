import os
import json
import statistics
from tokenizer import *
from constant import *
import random
import hangul_jamo
import time
from error_by_category import ErrorByCategory
from error_by_aspect import ErrorByAspect


def __avg_cal(total, total_amount):
    return total * 100 / total_amount


def print_error(text_list):
    print()
    print("===========오류=============")
    for text in text_list:
        print(text)
    print("============================")
    print()


def __dump_file(result, file_name):
    try:
        with open(file_name, 'w', encoding="UTF-8") as noised:
            json.dump(result, noised, ensure_ascii=False, indent=4)
            logger.info("Json을 " + file_name + " 에 추가 합니다 ")
    except:
        logger.error(" 파일 {} 생성 도중 오류 발생".format(file_name))
        print_error([" 파일 {} 생성 도중 오류 발생".format(file_name)])


def noise(data_directory, error_list, result_directory, json_maximum, tokenizer_type, label_type, error_by):
    error_count_dic = {"OM": 0, "REP": 0,
                       "MIF": 0, "ADD": 0, "S_ADD": 0, "S_DEL": 0}
    file_num = 0
    last_line = 0
    result = []
    id = data_directory.split("/")[-1]
    print("=====GEC Noise Generator Ko=====")

    print(" 오류 : {} 을 생성합니다".format(str(error_list)))

    try:
        print(" 데이터 파일에서 문장을 추출중입니다...")
        sentences = open(data_directory, 'rt', encoding='UTF-8').readlines()
        print(" 데이터 파일에서 문장을 추출완료... 노이즈 생성을 시작합니다")
        logger.info(" 데이터 파일에서 문장을 추출완료... 노이즈 생성을 시작합니다")
        logger.info(" 오류 종류 : [ " + ", ".join(error_list) + " ]")
    except FileNotFoundError as fe:
        print(fe)
        logger.error(fe)
        return

    if error_by == "aspect":
        error_labels = ASPECT_LABEL
    elif error_by == "category":
        error_labels = CATEGORY_LABEL
    else:
        message = ([" 잘못된 인자를 입력됬습니다 error_by : " + error_labels,
                   " [aspect] 와 [category] 중 하나를 입력해주십시오"])
        logger.error(message[0])
        logger.error(message[1])
        print_error([message])
        return

    if error_list[0] == "random_two":
        error_one, error_two = random.sample(error_labels.keys(), 2)
        error_list = [error_one, error_two]
    elif error_list[0] == "ALL":
        error_list = list(error_labels.keys())

    for error in error_list:
        if error not in error_labels.keys():
            error_label_list = list(error_labels.keys())
            message = ([" 잘못된 오류 유형을 입력했습니다 : " + error,
                       " 이 리스트에 존재하는 오류 유형을 입력해주십시오 : " + str(error_label_list)])
            logger.error(message[0])
            logger.error(message[1])
            print_error([message])
            return
    start_time = time.time()
    avg_time = start_time
    for sentence_num in range(0, len(sentences)):
        sentence = sentences[sentence_num].replace("\n", "").strip()
        words = tokenize_words(sentence.split(), tokenizer_type)
        sentence_dic = {}
        sentence_dic["id"] = id + "." + str(sentence_num)
        sentence_dic["source"] = []
        sentence_dic["target"] = sentence
        sentence_dic["word"] = []
        sentence_dic["GEC"] = []
        random.shuffle(error_list)

        for error_type in error_list:
            try:
                error_func = error_labels[error_type]
                if error_by == "aspect":
                    noise_generator = getattr(ErrorByAspect, error_func)
                else:
                    noise_generator = getattr(ErrorByCategory, error_func)
                words = noise_generator(words)

                # error_by 가 유형별로 오류 생성인 경우에만 확인
                if error_by == "category" and label_type == "original":
                    for word in words:
                        word[1][0] == error_type if word[1][0] != "type" else "type"
            except:
                message = (" 오류 유형 {} 을 {} 번째 문장에 생성도중 오류가 발생했습니다... 다음 문장으로 넘어갑니다".format(
                    error_type, sentence_num))
                logger.error(message)
                print_error([message])

        # 오류가 생성된 어절들중 한 문장당 (1~5)개의 오류만 변경시 선택받지 못한 나머지 오류들을 원상태로 되돌리기
        conv_list = [word for word in words if word[1][0] != "type"]
        max_error = random.randrange(1, 5)
        indices = sorted(random.sample(range(len(conv_list)), max_error)) if len(
            conv_list) > max_error else range(len(conv_list))

        converted_words = []
        for ind in indices:
            converted_words.append(conv_list[ind])

        for word in words:
            if word not in conv_list:
                word[1][0] = "type"
                for token in word[0]:
                    token[0] = token[2]

        words = add_position(words)
        sentence_dic["source"] = converge_words(words)
        check_sentence = sentence_dic["source"].strip()

        for converted_word in converted_words:
            gec_dic = {}
            if not converted_words:
                break
            else:
                gec_dic["id"] = words.index(converted_word)
                gec_dic["source"] = converge_word(converted_word, "source")
                gec_dic["target"] = converge_word(converted_word, "target")
                gec_dic["label"] = converted_word[1][0]
                for x in ASPECT_LABEL.keys():
                    if converted_word[1][0] == x:
                        error_count_dic[x] += 1
                gec_dic["begin"] = converted_word[1][1]
                gec_dic["end"] = converted_word[1][2]
                sentence_dic["GEC"].append(gec_dic)
        word_id = 0
        for word in words:
            word_dic = {}
            word_dic["id"] = word_id
            if word[1][0] == "type":
                word_dic["source"] = converge_word(word, "target")
            else:
                word_dic["source"] = converge_word(word, "source")
            word_dic["begin"] = word[1][1]
            word_dic["end"] = word[1][2]
            sentence_dic["word"].append(word_dic)
            word_id += 1

        result.append(sentence_dic)
        logger.debug("Noised {}".format(sentence_num))

        if sentence_num > 0 and (sentence_num+1) % json_maximum == 0:

            current_time = int((len(sentences)/sentence_num)
                               * int(time.time()-start_time))
            avg_time = current_time if avg_time == start_time else current_time
            avg_time = statistics.mean([avg_time, current_time])

            file_name = result_directory + id + "_" + str(file_num) + ".json"
            __dump_file(result, file_name)
            message = (" 문장 {} ~ {} 까지 오류가 생성되었고 json 리스트를 새로운 파일 {} 에 저장했습니다.\n 모든 문장에 오류 생성까지 : {} 초 예상됩니다".format(
                sentence_num - json_maximum + 1, sentence_num, file_name, avg_time))
            logger.info(message)
            print(message)
            result = []
            last_line = sentence_num + 1
            file_num += 1

    if result:
        file_name = result_directory + id + "_" + str(file_num) + ".json"
        __dump_file(result, file_name)
        message = (" 문장 {} ~ {} 까지 오류가 생성되었고 json 리스트를 새로운 파일에 저장했습니다.\n 완료까지 {} 줄 남았습니다".format(
            last_line, len(sentences)-1, (total_sentences - sentence_num + 1)))
        logger.info(message)
        print(message)

    end_time = time.time()
    total_time = end_time - start_time
    message = ("노이즈 생성을 완료했습니다. 소요 시간 : {} 초".format(total_time))
    logger.info(message)
    print(message)
    print("=======================================")

    if label_type == "benchmark":
        total_amount = sum([x for x in error_count_dic.values()])
        for e_type, e_count in error_count_dic.items():
            message = ([" 오류 유형 {} 에 생성된 오류 총량은 : {} 입니다".format(
                e_type, e_count), " 오류 생성 확률은 : {} 입니다".format(__avg_cal(e_count, total_amount))])
            logger.info(message[0])
            logger.info(message[1])
            print(message)
