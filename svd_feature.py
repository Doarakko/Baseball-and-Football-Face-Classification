#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import glob, re

#使用する画像のリストを取得する関数
def load_image_path_list(load_path):
    img_path_list = []
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除
            img_path = line.strip()
            img_path_list.append(img_path)
    #ソート
    img_path_list.sort()
    return img_path_list

layer_list = ["flatten", "fc6", "fc6/relu", "fc7", "fc7/relu", "fc8", "fc8/softmax"]
layer = layer_list[1]


#使用する画像のリストを取得
img_path_list = load_image_path_list(load_path="./data/image_path_list.txt")



'''
feature_path_list = glob.glob("./data/*/*/*/*/*_feature_" + layer + ".npy")
for feature_path in feature_path_list:
    #ファイル名を取得
    file_name = re.search(r'./data/.+/.+/.+/.+/(.+)_feature_.+.npy', feature_path)
    file_name = file_name.group(1)
    #ディレクトリのパスを取得
    dir_path = re.search(r'(./data/.+/.+/.+/.+/).+_feature_.+.npy', feature_path)
    dir_path = dir_path.group(1)
    dir_name = re.search(r'data/(.+/.+/.+/.+/).+_feature_.+.npy', feature_path)
    dir_name = dir_name.group(1)

    img_path = "./image/" + dir_name + file_name + ".jpg"
    if not img_path in img_path_list:
        feature_path_list.remove(feature_path)
'''

#使用するファイルのみのリストを作成
feature_path_list = []
for img_path in img_path_list:
     #ファイル名を取得
    file_name = re.search(r'./image/.+/.+/.+/.+/(.+).jpg', img_path)
    file_name = file_name.group(1)
    #ディレクトリのパスを取得
    dir_path = re.search(r'(./image/.+/.+/.+/.+/).+.jpg', img_path)
    dir_path = dir_path.group(1)
    dir_name = re.search(r'image/(.+/.+/.+/.+/).+.jpg', img_path)
    dir_name = dir_name.group(1)
    feature_path = "./data/" + dir_name + file_name + "_feature_" + layer + ".npy"
    feature_path_list.append(feature_path)
    print(feature_path)

feature_data_list = np.array([])
for feature_path in feature_path_list:
    feature_data = np.load(feature_path)
    feature_data_list = np.append(feature_data_list, feature_data)
#デバック
print("[Load] {0} feature data".format(layer))
#デバック
print("[Calculate] SVD")

#次元削減
A = feature_data_list
A = np.reshape(A, (-1, 500))
U, s, Vt_svd = np.linalg.svd(A, full_matrices=True)
V_svd = Vt_svd.T
feature_svd_data_list = np.dot(A, V_svd[0:, :500])

for (feature_path, feature_svd_data) in zip(feature_path_list, feature_svd_data_list):
    #ファイル名を取得
    file_name = re.search(r'./data/.+/.+/.+/.+/(.+)_feature_.+.npy', feature_path)
    file_name = file_name.group(1)
    #ディレクトリのパスを取得
    dir_path = re.search(r'(./data/.+/.+/.+/.+/).+_feature_.+.npy', feature_path)
    dir_path = dir_path.group(1)
    dir_name = re.search(r'data/(.+/.+/.+/.+/).+_feature_.+_svd.npy', feature_path)
    dir_name = dir_name.group(1)

    
    #特徴データを保存するパス
    save_path = dir_path + file_name + "_feature_" + layer + "_svd.npy"
    #抽出した特徴データをファイルに保存
    np.save(save_path, feature_svd_data)
    #デバック
    print("[Save] {0}".format(save_path))
