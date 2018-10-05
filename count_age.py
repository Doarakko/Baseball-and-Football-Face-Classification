# -*- coding: utf-8 -*-
import glob
import re
import json
import os
import shutil
import numpy as np


def load_person_list(load_path):
    person_list = []
    with open(load_path, 'r') as f:
        for line in f:
            person_data = line.strip().split(',')
            person_list.append(person_data)
    return person_list


if __name__ == '__main__':
    baseball_player_list_file_path = './data/baseball_player_list_age.txt'
    football_player_list_file_path = './data/football_player_list_age.txt'

    baseball_player_list = load_person_list(baseball_player_list_file_path)
    football_player_list = load_person_list(football_player_list_file_path)

    # 年齢データの抜き取り
    baseball_age_list = np.array([])
    for baseball_player in baseball_player_list:
        baseball_age_list = np.append(baseball_age_list, int(baseball_player[2]))

    football_age_list = np.array([])
    for football_player in football_player_list:
        football_age_list = np.append(football_age_list, int(football_player[2]))

    cnt_baseball_age_list = np.zeros(40)
    cnt_football_age_list = np.zeros(40)

    cut_num = 4
    min_age = 16

    # 野球選手
    print('[baseball] {0}'.format(len(baseball_age_list)))
    for baseball_age in baseball_age_list:
        if baseball_age >= min_age:
            cnt_baseball_age_list[int(baseball_age-min_age)] += 1
    for (i, num) in enumerate(cnt_baseball_age_list):
        print('{0}: {1}'.format(i+min_age, int(num)))
        if (i+1) % cut_num == 0:
            print('[sum] {0}'.format(int(np.sum(cnt_baseball_age_list[int((i+1)/cut_num*cut_num-cut_num):int((i+1)/cut_num*cut_num-cut_num)+cut_num]))))
            print('')
    print()

    # サッカー選手
    print('[football] {0}'.format(len(football_age_list)))
    for football_age in football_age_list:
        if football_age >= min_age:
            cnt_football_age_list[int(football_age-min_age)] += 1
    for (i, num) in enumerate(cnt_football_age_list):
        print('{0}: {1}'.format(i+min_age, int(num)))
        if (i+1) % cut_num == 0:
            print('[sum] {0}'.format(int(np.sum(cnt_football_age_list[int((i+1)/cut_num*cut_num-cut_num):int((i+1)/cut_num*cut_num-cut_num)+cut_num]))))
            print('')
    # '''
    sum = 0
    for (i, cnt_baseball_age) in enumerate(cnt_baseball_age_list):
        sum += cnt_baseball_age
        print(i+16, sum)
        if (i+16+1) % 10 == 0:
            sum = 0
    '''

    sum = 0
    for (i, cnt_football_age) in enumerate(cnt_football_age_list):
        sum += cnt_football_age
        print(i+16, sum)
        if (i+16+1) % 10 == 0:
            sum = 0
    '''
