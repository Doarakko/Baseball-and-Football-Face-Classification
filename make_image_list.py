#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import glob
import random

for age in range(16, 55):
    # 野球選手
    # ロードするパス
    load_path = './data/baseball_player_list_age' + str(age) + '.txt'
    # 保存するパス
    save_path = './data/baseball_image_path_list_age' + str(age) + '.txt'
    
    person_path_list = []
    with open(load_path, 'r') as f:
        for line in f:
            person_data = line.strip().split(',')
            if len(person_data) == 3:
                person_path_list.append(person_data[1])
    # シャッフル
    random.shuffle(person_path_list)
    baseball_num = len(person_path_list)

    # テキストファイルに保存
    with open(save_path, 'w') as f:
        for person_path in person_path_list:
            person_img_path_list = glob.glob('./image/' + person_path + '/*.jpg')
            for person_img_path in person_img_path_list:
                f.write(person_img_path + '\n')
    print('[Save] {0}'.format(save_path))

    # サッカー選手
    # ロードするパス
    load_path = './data/football_player_list_age' + str(age) + '.txt'
    # 保存するパス
    save_path = './data/football_image_path_list_age' + str(age) + '_origin.txt'

    person_path_list = []
    with open(load_path, 'r') as f:
        for line in f:
            person_data = line.strip().split(',')
            if len(person_data) == 3:
                person_path_list.append(person_data[1])
    # シャッフル
    random.shuffle(person_path_list)
    person_path_list = person_path_list

    # テキストファイルに保存
    with open(save_path, 'w') as f:
        for person_path in person_path_list:
            person_img_path_list = glob.glob('./image/' + person_path + '/*.jpg')
            for person_img_path in person_img_path_list:
                f.write(person_img_path + '\n')
    # 保存するパス
    save_path = './data/football_image_path_list_age' + str(age) + '.txt'

    person_path_list = []
    with open(load_path, 'r') as f:
        for line in f:
            person_data = line.strip().split(',')
            if len(person_data) == 3:
                person_path_list.append(person_data[1])
    # シャッフル
    random.shuffle(person_path_list)
    person_path_list = person_path_list[:baseball_num]

    # テキストファイルに保存
    with open(save_path, 'w') as f:
        for person_path in person_path_list:
            person_img_path_list = glob.glob('./image/' + person_path + '/*.jpg')
            for person_img_path in person_img_path_list:
                f.write(person_img_path + '\n')

    print('[Save] {0}'.format(save_path))
