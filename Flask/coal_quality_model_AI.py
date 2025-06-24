import tensorflow as tf
from tensorflow import keras 
import numpy as np
import os

# 获取脚本文件所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 拼接脚本目录与 CSV 文件名，形成完整路径
weight_path = os.path.join(script_dir, "model_weight\predict_model.h5")

model = keras.models.load_model(weight_path)
print(model)

