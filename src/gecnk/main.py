from __future__ import absolute_import
import argparse
import json
import os
import sys
import shutil
import zipfile
import pandas as pd
from json_generate import noise

sys.path.append("./")
current_file = os.path.dirname(__file__)
sys.path.append("./src/")
sys.path.append("./src/gecnk/")
result_file = "./src"


def main(data_directory, error_list, result_directory, json_maximum, tokenizer_type, label_type, error_by):
    noise(data_directory, error_list,
          result_directory, json_maximum, tokenizer_type, label_type, error_by)
    error_name = ""
    # 파일 압축
    for x in error_list:
        error_name += "_" + x
    zip_name = (data_directory.split("/")[-1] + error_name)
    path_to_json = result_file + "/results/"
    json_files = [pos_json for pos_json in os.listdir(
        path_to_json) if pos_json.endswith('.json')]
    ZipFile = zipfile.ZipFile(path_to_json + zip_name+".zip", "a")
    for j_file in json_files:
        ZipFile.write(j_file)
        os.remove(path_to_json + j_file)
    ZipFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='한글 맞춤법 교정기를 학습 데이터를 위한 노이즈 생성기', add_help=False)

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='자세한 설명은 README.md 파일을 참고')
    parser.add_argument('-d', metavar='data_directory',
                        help='데이터 디렉토리를 -d 뒤에 입력하십시오 ', default=current_file + "/resources/test-tgt", type=str)
    parser.add_argument('-e', metavar='error_list',
                        help='오류 유형을 -e 뒤에 입력하십시오, 이것은 오류 생성 기준에 따라 달라질 수 있습니다. 자세한건 README.md를 참고', nargs='+',
                        default=["MIF"])
    parser.add_argument('-r', metavar='result_directory',
                        help='저장 디렉토리를 -r 뒤에 입력하십시오', default=result_file + "/results/", type=str)
    parser.add_argument('-m', metavar='json_maximum',
                        help='한 파일에 최대 json 리스트의 갯수를 -m 뒤에 입력하십시오', default=100000, type=int)
    parser.add_argument('-t', metavar='tokenizer_type',
                        help='원하는 토크나이저의 유형을 -t 뒤에 입력하십시오', default="mecab", type=str)
    parser.add_argument('-b', metavar='error_by',
                        help='오류 생성 기준을 오류 양상으로 할것인지 오류 유형으로 할것인지 -e 뒤에 입력하십시오 [aspect는 오류 양상 category는 오류 유형 ]', default="aspect", type=str)
    parser.add_argument('-l', metavar='label_type',
                        help='만약 오류 생성 기준인 error_by 가 category인 경우, json결과 파일에 label에 나오는 원하시는 오류 양상 태그 형태를 -l 뒤에 입력하십시오 [benchmark는 국립국어원 오류주석 original은 오류 생성 유형]', default="benchmark", type=str)

    args = parser.parse_args()
    main(data_directory=args.d, error_list=args.e,
         result_directory=args.r, json_maximum=args.m, tokenizer_type=args.t, label_type=args.l, error_by=args.b)
