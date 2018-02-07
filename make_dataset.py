#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, re, json, os, shutil
from PIL import Image
import numpy as np

from keras.preprocessing.image import img_to_array, load_img

#画像サイズ
IMAGE_SIZE = 224
#チャネル数
CHANNEL_SIZE = 3 

#ラベルを作成する関数
def make_label_list():
    #ディレクトリのパスを取得
    dir_path_list = glob.glob('image/*')
    #辞書を準備
    label_dic = {}
    #各ディレクトリごとにラベルを振り分け
    for i, dir_path in enumerate(dir_path_list):
        key = re.search(r'image/(.+)', dir_path)
        key = key.group(1)
        #label_dic[key] = i
        label_dic[key] = 1
    #辞書をjsonで保存
    with open("./data/label_dic.json", "w") as f: 
        label_json = json.dumps(label_dic)
        json.dump(label_json, f)
    return label_dic

#画像を数値データに変換する関数
def convert_image(img_path):
    try:
        #画像をロード
        img = load_img(img_path, target_size=(IMAGE_SIZE,IMAGE_SIZE))
        x = img_to_array(img)
        #正規化
        x = x / 255.0
        return x
    except Exception as e:
        #移動
        shutil.move(img_path, "noise")
        #空
        x = []
        #デバック
        print("[Error] {0} <{1}>".format(img_path, e))
        return x
    

#ラベルデータを取得する関数
def get_label_data(img_path, label_dic):
    #画像のディレクトリのパスを取得
    key = re.search(r'image/(.+)/.+/.+/.+/.+', img_path)
    key = key.group(1)
    #辞書からラベルを取得
    t = label_dic[key]
    #ラベルをnumpy配列に変換
    t = np.asarray(t, dtype=np.int32)
    return t

#画像のパスから画像のファイル名を取得する関数
def get_image_name(img_path):
    image_name = re.search(r'image/.+/.+/.+/.+/(.+).jpg', img_path)
    image_name = image_name.group(1)
    return image_name

#データセットを作成する関数
def make_dataset(label_dic):
    #各人物のディレクトリのリストを取得
    person_path_list = glob.glob('image/*/*/*/*')
    for person_path in person_path_list:
        #写真の人物の名前を取得
        person_name = re.search(r'image/.+/.+/.+/(.+)', person_path)
        person_name = person_name.group(1)
        #画像のあるディレクトリの名前を取得
        dir_name = re.search(r'image/(.+/.+/.+)/.+', person_path)
        dir_name = dir_name.group(1)

        #画像データ・ラベルデータのファイルを保存するディレクトリ
        save_dir = "./data/" + dir_name + "/" + person_name
        #ファイルを保存するディレクトリを作成
        if not os.path.exists(save_dir): os.makedirs(save_dir)

        #人物のディレクト内の画像のリストを取得
        img_path_list = glob.glob(person_path+'/*.jpg')
        if img_path_list == []:
            #移動
            shutil.move(person_path, "noise")
            print("[Remove] {0}".format(person_path))
        #画像データを入れるリストを準備
        image_data = []
        #ラベルデータを入れるリストを準備
        label_data = []
        for img_path in img_path_list:
            #画像を数値データに変換
            x = convert_image(img_path)
            if x == []:
                continue
            #ラベルデータを取得
            t = get_label_data(img_path, label_dic)

            image_name = get_image_name(img_path)

            #画像データを保存するパス
            save_image_path = save_dir + "/" + image_name + "_image.npy"
            #ラベルデータを保存するパス
            save_label_path = save_dir + "/" + image_name + "_label.npy"

            #画像データをファイルに保存
            np.save(save_image_path, x)
            #ラベルデータをファイルに保存
            np.save(save_label_path, t)

        #デバック
        print("[Save] {0}: {1}".format(person_name, len(img_path_list)))
    #改行
    print()
    
    occupation_path_list = glob.glob('image/*')
    for occupation_path in occupation_path_list:
        #職業を取得
        occupation_name = re.search(r'image/(.+)', occupation_path)
        occupation_name = occupation_name.group(1)
        #全画像のリストを取得
        img_path_list = glob.glob(occupation_path + '/*/*/*')
        #デバック
        print("{0}: {1}".format(occupation_name, len(img_path_list)))
    print()

    #全画像のリストを取得
    img_path_list = glob.glob('image/*/*/*/*/*')
    #デバック
    print("total: {0}".format(len(img_path_list)))


if __name__ == '__main__':
    #ラベルを作成
    label_dic = make_label_list()
    #データセットを作成
    make_dataset(label_dic)