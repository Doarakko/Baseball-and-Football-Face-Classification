#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import glob
import random
import re
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_curve, auc

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


#レイヤー
layer_list = ['flatten', 'fc6', 'fc6/relu', 'fc7', 'fc7/relu', 'fc8', 'fc8/softmax']
layer = layer_list[1]

#人物のパスを取得
person_path_list = glob.glob('./data/*/*/*/*')
#シャッフル
random.shuffle(person_path_list)

#リストをnumpy配列に変換
person_path_list = np.array(person_path_list)

n_splits = [5, 8, 10, 20, 100, len(person_path_list)]
n_split = n_splits[3]

#データセットのshape
shapes = [4096, 500]
shape = shapes[0]


#ロジスティック回帰
solvers = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
solver = solvers[2]
#パラメータC

Cs = [10**i for i in range(-5, 5)]

#各Foldのacucuracyを入れる配列   
accuracy_list = np.zeros(len(Cs))
#各FoldのAUCを入れる配列
auc_list = np.zeros(len(Cs))

#使用する画像のリスト
img_path_list = []
age_begin = 16
age_end = 50
dir_num = str(6)
for age in range(age_begin, age_end+1):
    #野球選手
    load_path = './data/' + dir_num + '/baseball_image_path_list_age' + str(age) + '.txt'
    img_path_list.extend(load_image_path_list(load_path))

for age in range(age_begin, age_end+1):
    #サッカー選手                                                                                    
    load_path = './data/' + dir_num + '/football_image_path_list_age' + str(age) + '.txt'
    img_path_list.extend(load_image_path_list(load_path))

kf = KFold(n_splits=n_split, shuffle=True, random_state=0)
for k, (train_index, test_index) in enumerate(kf.split(person_path_list)):
    #学習用データ
    x_train = np.array([])
    y_train = np.array([])
    for person_path in person_path_list[train_index]:
        feature_path_list = glob.glob(person_path + '/*_' + layer + '_svd.npy')
        for feature_path in feature_path_list:
            label_dir = re.search(r'(data/.+/.+/.+/.+/).+_feature_.+_svd.npy', feature_path)
            label_dir = label_dir.group(1)
            dir_name = re.search(r'data/(.+/.+/.+/.+/).+_feature_.+_svd.npy', feature_path)
            dir_name = dir_name.group(1)
            file_name = re.search(r'data/.+/.+/.+/.+/(.+)_feature_.+_svd.npy', feature_path)
            file_name = file_name.group(1)
            #元の画像のパス
            img_path = './image/' + dir_name + file_name + '.jpg'
            if img_path in img_path_list:
                label_path = label_dir + file_name + '_label.npy'
                feature = np.load(feature_path)
                label = np.load(label_path)
                x_train = np.append(x_train, feature)
                y_train = np.append(y_train, label)
                print('*')

    #テスト用データ
    x_test = np.array([])
    y_test = np.array([])
    for person_path in person_path_list[test_index]:
        feature_path_list = glob.glob(person_path + '/*_' + layer + '_svd.npy')
        random.shuffle(feature_path_list)
        for feature_path in feature_path_list[0:1]:
            label_dir = re.search(r'(data/.+/.+/.+/.+/).+_feature_.+_svd.npy', feature_path)
            label_dir = label_dir.group(1)
            dir_name = re.search(r'data/(.+/.+/.+/.+/).+_feature_.+_svd.npy', feature_path)
            dir_name = dir_name.group(1)
            file_name = re.search(r'data/.+/.+/.+/.+/(.+)_feature_.+_svd.npy', feature_path)
            file_name = file_name.group(1)
            #元の画像のパス
            img_path = './image/' + dir_name + file_name + '.jpg'
            if img_path in img_path_list:
                label_path = label_dir + file_name + '_label.npy'  
                feature = np.load(feature_path)
                label = np.load(label_path)
                x_test = np.append(x_test, feature)
                y_test = np.append(y_test, label)
                print('***')

    x_train = np.reshape(x_train, (-1, shape))
    x_test = np.reshape(x_test, (-1, shape))

    #デバック
    print('train data: {0}\ttest data: {1}'.format(len(x_train), len(x_test))) 

    sc = StandardScaler()
    x_train_std = sc.fit_transform(x_train)
    x_test_std = sc.transform(x_test)
    for (i, c) in enumerate(Cs):
        clf = LogisticRegression(C=c, solver=solver)
        clf.fit(x_train_std, y_train)

        #accuracyの計算
        #学習用データのaccuracy
        train_accuracy = clf.score(x_train_std, y_train)
        #テスト用データのaccuracy
        test_accuracy = clf.score(x_test_std, y_test)
        #配列に追加
        accuracy_list[i] += test_accuracy

        #Area Under the Curveの計算
        y_test_pred = clf.predict(x_test)
        y_test_prob = clf.predict_proba(x_test)[:,1]
        precision, recall, thresholds = precision_recall_curve(y_test, y_test_prob)
        area = auc(recall, precision)
        #配列に追加
        auc_list[i] += area

        #デバック
        print ('k: {0}\tC: {1}\ttrain accuracy: {2}\ttest accuracy: {3}\tAUC: {4}'.format(k+1, c, train_accuracy, test_accuracy, area))
    print()

#solver
#print('solver: {0}'.format(solver))

#デバック
print('Age: {0}~{1} Layer: {2}'.format(age_begin, age_end, layer))

#accuracyの平均
accuracy_list /= n_split
#Area Under the Curveの平均
auc_list /= n_split

for (i, c) in enumerate(Cs):
    print('C: {0}\taverage accuracy: {1}\tAUC: {2}'.format(c, accuracy_list[i], auc_list[i]))
