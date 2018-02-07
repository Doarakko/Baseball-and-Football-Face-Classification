#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, re, json, os, shutil
import numpy as np

def load_person_list(load_path):
    person_list = []
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除, カンマで区切る
            person_data = line.strip().split(',')
            person_list.append(person_data)
    return person_list

def load_img_path_list(load_path):
    person_list = []
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除, カンマで区切る
            person_data = line.strip()
            person_list.append(person_data)
    return person_list

if __name__ == '__main__':
    #player_list_file_path = "./data/baseball_player_list_age.txt"
    player_list_file_path = "./data/football_player_list_age.txt"

    player_list = load_person_list(player_list_file_path)

    img_path_list_path = "./data/image_path_list.txt"
    img_path_list = load_img_path_list(img_path_list_path)

    file_name_list = []
    for img_path in img_path_list:
        file_name = re.search(r'./image/(.+/.+/.+/.+)/.+.jpg', img_path)
        file_name = file_name.group(1)
        file_name_list.append(file_name)
    
    for age in range(16,55): 
        #保存するパス
        #save_path = "./data/baseball_player_list_age" + str(age) + ".txt"
        save_path = "./data/football_player_list_age" + str(age) + ".txt"
        with open(save_path, 'w') as f:
            for player in player_list:
                if player[2] + player[1] in file_name_list:
                    if int(player[4]) == age:
                        f.write(player[0] + "," + player[2] + player[1] + "," + player[4] + "\n")
        #デバック
        print("[Save] {0}".format(save_path))





