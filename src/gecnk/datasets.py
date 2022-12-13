from constant import *
import os
import fasttext
import csv
import time
current_file = os.path.dirname(__file__)


def read_data(file_name):
    file = open(file_name, 'rt', encoding='UTF-8-sig')
    data = csv.reader(file)
    one_data = []
    two_data = []
    for line in data:
        one_data.append(line[0])
        two_data.append(line[1])
    file.close
    return one_data, two_data


def read_single_data(file_name):
    file = open(file_name, 'rt', encoding="UTF-8-sig")
    data = csv.reader(file)
    one_data = []
    for line in data:
        one_data.append(line[0])
    file.close
    return one_data


def phonetic_data():
    phonetic_data_directory = current_file + "/resources/phonetic_data.csv"
    phonetic_data = read_data(phonetic_data_directory)
    correct_phonetic = phonetic_data[1]
    error_phonetic = phonetic_data[0]
    return correct_phonetic, error_phonetic
