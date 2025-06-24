import pandas as pd
import os
from ModelPredict import modelpredict

# 获取脚本文件所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 拼接脚本目录与 CSV 文件名，形成完整路径
csv_path = os.path.join(script_dir, "CoalData_WWN.csv")

# 使用绝对路径读取 CSV 文件
data = pd.read_csv(csv_path)

# 拼接脚本目录与模型文件名，形成完整路径
model_path = os.path.join(script_dir, "model_weight", "Model_DIS_CSR.pkl")

# 使用绝对路径读取模型文件
model = pd.read_pickle(model_path)

# 继续执行代码
dis_data = data.iloc[:, 0:12]
dis_r = modelpredict(dis_data, model)
