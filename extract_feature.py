#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, re, os
import numpy as np

from keras.engine import  Model
from keras.preprocessing.image import img_to_array, load_img
from keras.utils import plot_model

from keras_vggface.vggface import VGGFace
from keras_vggface import utils

layer_list = ["flatten", "fc6", "fc6/relu", "fc7", "fc7/relu", "fc8", "fc8/softmax"]
layer = layer_list[5]

#特徴を抽出する関数
def extract_feature(model, image_data):
    #推論
    x = np.expand_dims(image_data, axis=0)
    x = utils.preprocess_input(x)
    y = model.predict(x)[0]
    return y

if __name__ == '__main__':
    vgg_model = VGGFace(include_top=True, weights='vggface', input_tensor=None, input_shape=None, pooling=None, classes=2622)
    out = vgg_model.get_layer(layer).output
    model = Model(vgg_model.input, out)

    #モデルを可視化
    #plot_model(model, to_file='./log/model.png')
    
    image_data_path_list = glob.glob("./data/*/*/*/*/*_image.npy")
    for (i, image_data_path) in enumerate(image_data_path_list):
        dir_path = re.search(r'(.+)/.+npy', image_data_path)
        dir_path = dir_path.group(1)

        file_name = re.search(r'./data/.+/.+/.+/.+/(.+)_image.npy', image_data_path)
        file_name = file_name.group(1)

        #特徴データを保存するパス
        save_feature_data_path = dir_path + "/" + file_name + "_feature_" + layer + ".npy"
        if os.path.exists(save_feature_data_path):
            #デバック
            print("[Skip] {0}".format(save_feature_data_path))
        else:
            #データセットをロード
            image_data = np.load(image_data_path)
            #特徴を抽出
            feature_data = extract_feature(model, image_data)
            #抽出した特徴データをファイルに保存
            np.save(save_feature_data_path, feature_data)
            #デバック
            print("[Save] {0}\t{1} / {2}".format(save_feature_data_path, i+1, len(image_data_path_list)))
