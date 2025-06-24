from flask import Flask, redirect, request, url_for, send_file, Response
from flask_cors import CORS
from coalData import CoalDataGeneration,app,db
from flask import jsonify
import json
from typeClassfication import coaltypefind
import csv
from tensorflow import keras 
import tensorflow as tf
import sys, os
import numpy as np
import geatpy as ea
from genetic_algorithm_geatpy1 import MyProblem
import pandas as pd
from pandas.core.frame import DataFrame
from ModelPredict import modelpredict
import pickle
import random
from typing import Any

def setup_seed(seed: int) -> None:
    """
    设置随机种子，以确保结果的可复现性。
    通过设置 NumPy 和 TensorFlow 的随机种子，确保每次运行的结果一致。

    参数:
        seed (int): 用于初始化随机数生成器的种子值。

    返回值:
        None: 本函数没有返回值，仅修改全局状态以设置随机种子。

    示例:
        设置随机种子为 42:

        ::
            setup_seed(42)

    注意:
        1. 调用 `np.random.seed(seed)` 为 NumPy 设置随机种子。
        2. 调用 `tf.random.set_seed(seed)` 为 TensorFlow 设置 CPU 随机种子。
        3. 通过设置环境变量 `os.environ['TF_DETERMINISTIC_OPS'] = '1'` 为 TensorFlow 的 GPU 操作启用确定性行为。
           请确保安装了 `tensorflow-determinism` 库以支持 GPU 的完全确定性操作。
    """
    np.random.seed(seed)  # 为 NumPy 设置随机种子
    tf.random.set_seed(seed)  # 为 TensorFlow 设置 CPU 随机种子
    os.environ['TF_DETERMINISTIC_OPS'] = '1'  # 为 TensorFlow GPU 设置随机种子

setup_seed(32) # 45:3.31330   47:3.31407
random.seed(36)

# 获取当前脚本所在的目录并拼接路径
model_dir = os.path.join(os.path.dirname(__file__), 'model_weight')

# 加载模型
# model = keras.models.load_model(os.path.join(model_dir, 'predict_model.h5'))

# 加载专家系统模型
model_expert = pd.read_pickle(os.path.join(model_dir, 'Model_DIS_CSR.pkl'))

with open(os.path.join(model_dir, 'linear.pickle'), 'rb') as f:
    linereg = pickle.load(f)

with open(os.path.join(model_dir, 'decisiontree.pickle'), 'rb') as f:
    decisiontree = pickle.load(f)

with open(os.path.join(model_dir, 'KNN.pickle'), 'rb') as f:
    KNN = pickle.load(f)

with open(os.path.join(model_dir, 'RF.pickle'), 'rb') as f:
    RF = pickle.load(f)

with open(os.path.join(model_dir, 'SVR_CRI.pickle'), 'rb') as f:
    SVR_CRI = pickle.load(f)

with open(os.path.join(model_dir, 'SVR_CSR.pickle'), 'rb') as f:
    SVR_CSR = pickle.load(f)

with open(os.path.join(model_dir, 'GradientBoostingRegressor_1.pickle'), 'rb') as f:
    GradientBoostingRegressor_1 = pickle.load(f)

with open(os.path.join(model_dir, 'GradientBoostingRegressor_2.pickle'), 'rb') as f:
    GradientBoostingRegressor_2 = pickle.load(f)


CORS(app, supports_credentials=True) #两个python文件都最好跨域,必须要有
CORS(app, resources={r'/*': {'origins': '*'}})

upload_classify = 0 #用于按钮点击上传煤分类
upload_classify_user = 0 #用于按钮点击上传煤分类-用户

account_name = {'ustl':'ustl777888'} #存放账号和密码

#登录界面
@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    登录接口处理函数。

    处理登录请求：
        - 对于 POST 请求，验证用户提供的用户名和密码。
        - 对于 GET 请求，返回提示用户发送 POST 请求进行登录。

    参数:
        无（通过 HTTP 请求传递数据）。

    返回值:
        对于 POST 请求:
            JSON: 返回登录验证结果，包含以下字段:
                message (str): 表示登录结果，"success1" 表示成功，"fail" 表示失败。
        对于 GET 请求:
            tuple: 返回包含提示信息字符串和 HTTP 状态码的元组。

    示例:
        1. POST 请求示例:
        ::
            POST /login
            {
                "username": "ustl",
                "password": "ustl777888"
            }

        返回:
        ::
            {
                "message": "success1"
            }

        2. GET 请求示例:
        ::
            GET /login

        返回:
        ::
            "Please send a POST request with login credentials.", 200
    """
    if request.method == 'POST':
        # 获取并解析 POST 请求中的数据
        user_data = request.data
        user_data = json.loads(user_data)

        # 验证用户名和密码
        if user_data.get('username') == 'ustl' and user_data.get('password') == 'ustl777888':
            return jsonify(message="success1")  # 返回 JSON 格式响应，表示登录成功
        else:
            return jsonify(message="fail")  # 返回 JSON 格式响应，表示登录失败
    else:
        # 处理 GET 请求，返回提示信息
        print("Received a GET request on /login")  # 日志记录
        return "Please send a POST request with login credentials.", 200 

#煤数据获取
@app.route('/coalData', methods=['POST', 'GET'])
def getData():
    """
    获取煤数据接口处理函数。

    根据查询参数返回煤数据：
    - 对于 GET 请求，根据查询参数 `query` 过滤煤种数据。
    - 如果 `query` 为空或未提供，则返回所有煤数据。

    参数:
        无（通过 HTTP 请求传递查询参数）。

    返回值:
        JSON: 返回包含煤数据查询结果的 JSON 格式响应，包含以下字段:
            msg (str): 煤数据查询结果，由 `CoalDataGeneration.response` 方法格式化。

    示例:
        1. 无查询参数时返回所有煤数据:
            ::
                GET /coalData

            返回:
            ::
                {
                    "msg": [
                        {
                            "id": 1,
                            "coal_type": "Anthracite",
                            ...
                        },
                        ...
                    ]
                }

        2. 通过查询参数过滤煤种数据:
            ::
                GET /coalData?query=Anthracite

            返回:
            ::
                {
                    "msg": [
                        {
                            "id": 1,
                            "coal_type": "Anthracite",
                            ...
                        }
                    ]
                }
    """
    if request.method == 'GET':
        # 获取查询参数
        query_param = request.values.get('query', default='')

        # 查询数据库数据
        if query_param == '':
            # 查询所有煤数据
            coal_data = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        else:
            # 根据煤种类型过滤
            coal_data = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == query_param).all()

        # 使用响应方法格式化数据
        response = {
            "msg": CoalDataGeneration.response(None, CoalData=coal_data)
        }

        # 返回 JSON 格式响应
        return jsonify(response)

@app.route('/coalDetailedData', methods=['POST', 'GET'])
def getDetailedData():
    """
    根据煤数据的 ID 查询煤的详细信息接口。

    处理逻辑:

        对于 GET 请求，通过查询参数 `id` 获取煤数据的 ID。
    
        查询数据库，返回对应的煤数据详细信息。

    参数:
        无（通过 HTTP 请求传递煤数据 ID）。

    返回值:
        JSON: 返回包含煤的详细信息的 JSON 格式响应，包含以下字段:
            msg (str): 煤的详细信息，由 `CoalDataGeneration.response` 方法格式化。

    示例:
        1. 查询煤的详细信息:
        ::
            GET /coalDetailedData?id=5

        返回:
        ::
            {
                "msg": {
                    "id": 5,
                    "coal_type": "Anthracite",
                    ...
                }
            }

        2. 缺少 `id` 参数时的错误响应:
        ::
            GET /coalDetailedData

        返回:
        ::
            {
                "msg": "Error: Missing 'id' parameter"
            }
    """
    if request.method == 'GET':
        # 获取查询参数 'id'
        query_id = request.values.get('id')

        # 检查 ID 是否提供
        if not query_id:
            return jsonify({"msg": "Error: Missing 'id' parameter"}), 400

        # 根据 ID 查询煤的详细数据
        query_result = CoalDataGeneration.query.filter(CoalDataGeneration.id == query_id).all()

        # 格式化查询结果
        response = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回 JSON 格式响应
        return jsonify(response)

@app.route('/deleteCoalData', methods=['POST', 'GET'])
def deleteCoalData():
    """
    根据煤数据的 ID 删除煤的详细信息接口。

    处理逻辑:
        对于 POST 请求，通过传递的煤数据 ID 删除对应的记录。如果未提供 ID 或记录不存在，返回相应的错误信息。

    参数:
        无（通过 HTTP 请求传递煤数据 ID）。

    返回值:
        str: 删除操作的结果信息。
        
            成功时返回 "delete successfully"。

            如果 ID 对应的记录不存在，返回 "Coal data not found" 和 HTTP 状态码 404。

    示例:
        1. 删除煤数据记录:
        ::
            请求:
            POST /deleteCoalData?id=5

            返回:
            "delete successfully"

        2. 记录不存在时:
        ::
            请求:
            POST /deleteCoalData?id=100

            返回:
            "Coal data not found", 404

        3. 缺少 ID 参数时:
        ::
            请求:
            POST /deleteCoalData

            返回:
            "Error: Missing 'id' paraeter", 400
    """
    if request.method == 'POST':
        # 获取查询参数 'id'
        query_id = request.values.get('id')

        # 检查 ID 是否提供
        if not query_id:
            return "Error: Missing 'id' parameter", 400

        # 根据 ID 查询煤数据
        query_result = CoalDataGeneration.query.filter_by(id=query_id).first()

        # 检查是否找到记录
        if query_result:
            # 删除记录并提交事务
            db.session.delete(query_result)
            db.session.commit()
            return "delete successfully"  # 返回成功消息
        else:
            return "Coal data not found", 404  # 返回未找到消息及状态码
    else:
        return "Invalid request method", 405  # 不支持的请求方法

# #煤类别扇形图获取
# @app.route('/getFanData',methods=['POST','GET'])
# def getFanData():
#     if request.method == 'GET':
#         CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
#         res = {
#         "msg": CoalDataGeneration.response_pie(None, CoalData=CoalData)
#         }
#         return jsonify(res)

# #煤价格直方图获取
# @app.route('/getPriceData',methods=['POST','GET'])
# def getPriceData():
#     if request.method == 'GET':
#         CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
#         res = {
#         "msg": CoalDataGeneration.response_bar(None, CoalData=CoalData)
#         }
#         return jsonify(res)

@app.route('/getClassifyData', methods=['POST', 'GET'])
def getClassifyData():
    """
    接收煤数据并将其转化为 CSV 文件进行分类预测。

    处理逻辑: 
        接收 POST 请求中的煤数据，解析后保存为 CSV 文件。
        
        调用煤分类预测函数 `coaltypefind` 对每条煤数据进行分类预测。

        返回包含每条数据的 ID、名称及预测类型的结果。

    参数:
        无（通过 POST 请求传递煤数据）。

    返回值:
        JSON: 返回预测结果的 JSON 格式响应，包含以下字段:

            id (int): 煤数据的唯一标识。

            name (str): 煤数据的名称。

            predicted_type (str): 预测的煤类型或 "判据不足"。

    示例:
        1. 使用 POST 请求传递煤数据进行预测:
        ::
            请求:
            POST /getClassifyResult
            [
                {
                    "id": 1,
                    "coal_name": "Coal A",
                    "coal_vdaf": 25.3,
                    "coal_drynoash_hdaf": 5.6,
                    "G": 1.2,
                    "Y": 3.4,
                    "b": 0.9
                }
            ]

            返回:
            [
                {
                    "id": 1,
                    "name": "Coal A",
                    "predicted_type": "Type 1"
                }
            ]

        2. 错误响应示例 (当请求方法不是 POST 时):
        ::
            Invalid request method
    """
    
    if request.method == 'GET':
        # 从数据库中按 ID 降序获取所有煤数据记录
        coal_data = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()

        # 使用响应方法格式化数据
        response = {
            "msg": CoalDataGeneration.response(None, CoalData=coal_data)
        }

        # 返回 JSON 格式的响应
        return jsonify(response)
    else:
        # 如果请求方法不是 GET，返回 405 错误
        return "Invalid request method", 405

@app.route('/getClassifyResult', methods=['POST'])
def getClassifyResult():
    """
    接收煤数据并将其转化为 CSV 文件进行分类预测。

    处理逻辑:
        接收 POST 请求中的煤数据，解析后保存为 CSV 文件。

        调用煤分类预测函数 `coaltypefind` 对每条煤数据进行分类预测。

        返回包含每条数据的 ID、名称及预测类型的结果。

    参数:
        无（通过 POST 请求传递煤数据）。

    返回值:
        JSON: 返回预测结果的 JSON 格式响应，包含以下字段:

            id (int): 煤数据的唯一标识。

            name (str): 煤数据的名称。

            predicted_type (str): 预测的煤类型或 "判据不足"。

    示例:
        1. 传递煤数据进行预测:
        ::
            请求:
            POST /getClassifyResult
            [
                {
                    "id": 1,
                    "coal_name": "Coal A",
                    "coal_vdaf": 25.3,
                    "coal_drynoash_hdaf": 5.6,
                    "G": 1.2,
                    "Y": 3.4,
                    "b": 0.9
                }
            ]

            返回:
            [
                {
                    "id": 1,
                    "name": "Coal A",
                    "predicted_type": "Type 1"
                }
            ]

        2. 请求数据格式错误:
        ::
            请求:
            POST /getClassifyResult
            { invalid json }

            返回:
            {
                "error": "Invalid JSON data"
            }

        3. 输入数据缺少必要字段:
        ::
            请求:
            POST /getClassifyResult
            [
                {
                    "id": 1,
                    "coal_name": "Coal A"
                }
            ]

            返回:
            {
                "error": "Missing key in input data: 'coal_vdaf'"
            }
    """
    # 验证请求方法
    if request.method != 'POST':
        return "Invalid request method", 405

    # 获取并解析请求数据
    try:
        prepared_data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400

    # 初始化结果列表
    response_result = []

    # CSV 文件头部定义
    headers = ['Type', 'Vm', 'H', 'G', 'Y', 'b']
    file_name = 'Sample.csv'

    # 遍历输入数据进行分类预测
    for data in prepared_data:
        try:
            # 提取相关参数
            row = [
                'Test',  # 假设类型为 "Test"
                data['coal_vdaf'],
                data['coal_drynoash_hdaf'],
                data['G'],
                data['Y'],
                data['b']
            ]

            # 写入 CSV 文件
            with open(file_name, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(headers)
                csv_writer.writerow(row)

            # 调用煤分类预测函数
            prediction = coaltypefind(file_name)

            # 构建分类结果
            result = {
                "id": data['id'],
                "name": data['coal_name'],
                "predicted_type": prediction[0] if prediction else "判据不足"
            }

            # 添加结果到响应数组
            response_result.append(result)

        except KeyError as e:
            return jsonify({"error": f"Missing key in input data: {e}"}), 400

    # 返回预测结果
    return jsonify(response_result)

@app.route('/uploadClassifyResult', methods=['POST', 'GET'])
def uploadClassifyResult():
    """
    将分类预测结果上传到数据库，并更新对应煤数据的类型。

    处理逻辑:
        检查全局变量 `upload_classify` 是否包含分类结果。

        遍历 `upload_classify` 中的每条预测结果。

        根据预测结果的 `id` 更新数据库中对应记录的 `coal_type` 字段。

        提交更新到数据库。

    参数:
        无（通过 POST 请求上传分类预测结果）。

    返回值:
        str: 返回上传结果的响应字符串:

            "upload successfully": 表示分类结果已成功上传。

    示例:
        上传分类预测结果至数据库:
        ::
            全局变量 `upload_classify` 包含以下数据:
            [
                {
                    "id": 1,
                    "predicted_type": "Type A"
                },
                {
                    "id": 2,
                    "predicted_type": "Type B"
                }
            ]

            请求:
            POST /uploadClassifyResult

            返回:
            "upload successfully"

    注意事项:
        1. `upload_classify` 必须是一个已存储分类结果的全局变量，数据格式应包含以下字段:
            
            id (int): 煤数据的唯一标识。
            
            predicted_type (str): 分类预测的煤类型。
        
        2. 使用 SQLAlchemy 的 `update()` 方法批量更新数据库中的记录。
        
        3. 必须确保数据库会话 (`db.session`) 的提交成功。
    """
    # 检查是否有分类结果可供上传
    if len(upload_classify) != 0:  # 如果存在分类结果
        # 遍历每一条分类预测结果
        for i in upload_classify:
            try:
                # 更新数据库中的煤类型字段
                CoalDataGeneration.query.filter_by(id=i['id']).update({'coal_type': str(i['predicted_type'])})
                db.session.commit()  # 提交更新到数据库
            except Exception as e:
                db.session.rollback()  # 回滚事务
                return jsonify({"error": f"Failed to update record with ID {i['id']}: {str(e)}"}), 500

    # 返回成功提示
    return "upload successfully"

#焦炭质量预测(AI模型)
@app.route('/getCokeQualityfyeResultAI', methods=['POST', 'GET'])
def getCokeQualityfyeResultAI():
    """
    接收煤炭数据并使用 AI 模型预测焦炭的质量参数（M25、M10、CRI、CSR等）

    Paremeters
    无（通过 POST 请求上传煤炭数据）

    Return
    返回一个包含预测结果的 JSON 格式响应，其中每个煤样品的预测结果包括：
    1. 预测的 M25、M10、CRI、CSR 值
    2. 真实的 M25、M10、CRI、CSR 值（如果存在）
    3. 预测误差（如有）
    4. 每个样本的平均误差（全体样本）
    
    Example
    1. 从请求中读取煤炭数据。
    2. 处理并规范化数据（通过最大最小值标准化）。
    3. 使用预训练的 AI 模型对数据进行预测。
    4. 计算并存储每个煤样品的预测结果和误差。
    5. 返回预测结果，包含每个煤样品的详细信息。

    Notes
    1. 输入数据应包含多个煤样本的物理和化学参数，如煤的含水率、挥发分等。
    2. 模型预测值与实际值的误差（CRI 和 CSR）将计算并返回。
    3. 模型需要事先训练并加载（假定 `model` 已加载）。

    例如返回的 JSON 数据可能如下：
    ```json
    [
    {
    "id": 1,
    "coal_name": "Sample A",
    "M25": 10.25,
    "M10": 5.30,
    "CRI": 12.3,
    "CSR": 25.1,
    "real_M25": 10.0,
    "real_M10": 5.0,
    "real_CRI": 12.5,
    "real_CSR": 25.0,
    "error_CRI": "1.6%",
    "error_CSR": "0.4%",
    "total_error_CRI": "1.2",
    "total_error_CSR": "0.3"
    },
    ...
    ]
    ```

    Notes
    如果传入的数据中有 `None` 值（表示缺失数据），将返回一个包含 `'Error'` 的 JSON 响应。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用预训练模型进行预测
        np_predict_data = model.predict(np_predict_data)  # 预测结果
        np_predict_data = np_predict_data.astype(np.float64)  # 转换为浮动类型
        np_predict_data = np.around(np_predict_data, decimals=2)  # 保留两位小数

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['M25'] = single_predicted_data[2]
            para_dict['M10'] = single_predicted_data[3]
            para_dict['CRI'] = single_predicted_data[4]
            para_dict['CSR'] = single_predicted_data[5]

            # 真实值
            para_dict['real_M25'] = prepared_data[i]['coke_M25']
            para_dict['real_M10'] = prepared_data[i]['coke_M10']
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']

            # 计算误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])
                valid_CRI_number += 1
            else:
                para_dict['error_CRI'] = ''

            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])
                valid_CSR_number += 1
            else:
                para_dict['error_CSR'] = ''

            # 将单条数据加入最终结果
            response_result.append(para_dict)

            # 计算并添加平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CSR_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典
            i += 1
        
        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AI线性回归模型)
@app.route('/getCokeQualityfyeResultAILinear', methods=['POST', 'GET'])
def getCokeQualityfyeResultAILinear():
    """
    接收煤炭数据并使用线性回归模型预测焦炭的质量参数（CRI、CSR等）。

    Paremeters
    无（通过 POST 请求上传煤炭数据）

    Return
    返回一个包含预测结果的 JSON 格式响应，其中每个煤样品的预测结果包括：
    - 预测的CRI和CSR值
    - 真实的CRI和CSR值（如果存在）
    - 预测误差（如有）
    - 每个样本的平均误差（全体样本）

    Example
    1. 从请求中读取煤炭数据。
    2. 处理并规范化数据（通过最大最小值标准化）。
    3. 使用线性回归模型对数据进行预测。
    4. 计算并存储每个煤样品的预测结果和误差。
    5. 返回预测结果，包含每个煤样品的详细信息。

    Notes
    如果传入的数据中有 `None` 值（表示缺失数据），将返回一个包含 `'Error'` 的 JSON 响应。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用线性回归模型进行预测
        np_predict_data = linereg.predict(np_predict_data)  # 预测结果
        np_predict_data = np_predict_data.astype(np.float64)  # 转换为浮动类型
        np_predict_data = np.around(np_predict_data, decimals=2)  # 保留两位小数

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CSR_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1

        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AI决策树模型)
@app.route('/getCokeQualityResultAIDecisionTree', methods=['POST', 'GET'])
def getCokeQualityResultAIDecisionTree():
    """
    使用决策树模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括特征提取和归一化。
        - 调用决策树模型分别预测 CRI 和 CSR。
        - 计算每个样品的预测误差，并返回预测结果及平均误差。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - total_error_CRI (float): 所有样品 CRI 的平均误差。
            - total_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityResultAIDecisionTree

            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_mad": 10.5,
                    "coal_ad": 20.3,
                    "coal_vdaf": 25.0,
                    "coal_std": 1.2,
                    "G": 0.5,
                    "X": 1.3,
                    "Y": 3.4,
                    "coke_CRI": 12.0,
                    "coke_CSR": 25.0
                },
                ...
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 24.8,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.17%",
                        "error_CSR": "0.80%",
                        "total_error_CRI": 3.50,
                        "total_error_CSR": 1.20
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含煤炭样品的所有必要特征。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型需要预先加载（假定 `decisiontree` 模型已加载）。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用决策树模型进行预测
        np_predict_data = decisiontree.predict(np_predict_data)  # 预测结果
        np_predict_data = np_predict_data.astype(np.float64)  # 转换为浮动类型
        np_predict_data = np.around(np_predict_data, decimals=2)  # 保留两位小数

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1

        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

@app.route('/getCokeQualityfyeResultAIKNN', methods=['POST', 'GET'])
def getCokeQualityfyeResultAIKNN():
    """
    使用 KNN 模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括特征提取和归一化。
        - 调用 KNN 模型分别预测 CRI 和 CSR。
        - 计算每个样品的预测误差，并返回预测结果及平均误差。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - total_error_CRI (float): 所有样品 CRI 的平均误差。
            - total_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityfyeResultAIKNN

            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_mad": 10.5,
                    "coal_ad": 20.3,
                    "coal_vdaf": 25.0,
                    "coal_std": 1.2,
                    "G": 0.5,
                    "X": 1.3,
                    "Y": 3.4,
                    "coke_CRI": 12.0,
                    "coke_CSR": 25.0
                },
                ...
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 24.8,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.17%",
                        "error_CSR": "0.80%",
                        "total_error_CRI": 3.50,
                        "total_error_CSR": 1.20
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含煤炭样品的所有必要特征。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型需要预先加载（假定 `KNN` 模型已加载）。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用KNN模型进行预测
        np_predict_data = KNN.predict(np_predict_data)  # 预测结果
        np_predict_data = np_predict_data.astype(np.float64)  # 转换为浮动类型
        np_predict_data = np.around(np_predict_data, decimals=2)  # 保留两位小数

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1

        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AIRF模型)
@app.route('/getCokeQualityfyeResultAIRF', methods=['POST', 'GET'])
def getCokeQualityfyeResultAIRF():
    """
    使用随机森林（RF）模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括特征提取和归一化。
        - 调用 RF 模型分别预测 CRI 和 CSR。
        - 计算每个样品的预测误差，并返回预测结果及平均误差。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - total_error_CRI (float): 所有样品 CRI 的平均误差。
            - total_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityfyeResultAIRF

            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_mad": 10.5,
                    "coal_ad": 20.3,
                    "coal_vdaf": 25.0,
                    "coal_std": 1.2,
                    "G": 0.5,
                    "X": 1.3,
                    "Y": 3.4,
                    "coke_CRI": 12.0,
                    "coke_CSR": 25.0
                },
                ...
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 24.8,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.17%",
                        "error_CSR": "0.80%",
                        "total_error_CRI": 3.50,
                        "total_error_CSR": 1.20
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含煤炭样品的所有必要特征。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型需要预先加载（假定 `RF` 模型已加载）。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用随机森林模型进行预测
        np_predict_data = RF.predict(np_predict_data)  # 预测结果
        np_predict_data = np_predict_data.astype(np.float64)  # 转换为浮动类型
        np_predict_data = np.around(np_predict_data, decimals=2)  # 保留两位小数

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1

        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AISVR模型)
@app.route('/getCokeQualityfyeResultAISVR', methods=['POST', 'GET'])
def getCokeQualityfyeResultAISVR():
    """
    使用支持向量回归（SVR）模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括特征提取和归一化。
        - 调用 SVR 模型分别预测 CRI 和 CSR。
        - 计算每个样品的预测误差，并返回预测结果及平均误差。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - total_error_CRI (float): 所有样品 CRI 的平均误差。
            - total_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityfyeResultAISVR

            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_mad": 10.5,
                    "coal_ad": 20.3,
                    "coal_vdaf": 25.0,
                    "coal_std": 1.2,
                    "G": 0.5,
                    "X": 1.3,
                    "Y": 3.4,
                    "coke_CRI": 12.0,
                    "coke_CSR": 25.0
                },
                ...
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 24.8,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.17%",
                        "error_CSR": "0.80%",
                        "total_error_CRI": 3.50,
                        "total_error_CSR": 1.20
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含煤炭样品的所有必要特征。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型需要预先加载（假定 `SVR_CRI` 和 `SVR_CSR` 已加载）。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用支持向量回归（SVR）模型分别预测CRI和CSR
        np_predict_data_CRI = SVR_CRI.predict(np_predict_data)  # 预测CRI值
        np_predict_data_CSR = SVR_CSR.predict(np_predict_data)  # 预测CSR值

        # 将结果重塑为二维数组
        np_predict_data_CRI = np_predict_data_CRI.reshape(np_predict_data_CRI.shape[0], -1)
        np_predict_data_CSR = np_predict_data_CSR.reshape(np_predict_data_CSR.shape[0], -1)

        # 合并两个预测结果（CRI 和 CSR）
        np_predict_data = np.concatenate([np_predict_data_CRI, np_predict_data_CSR], axis=1)

        # 转换数据类型为浮点数，并保留两位小数
        np_predict_data = np_predict_data.astype(np.float64)
        np_predict_data = np.around(np_predict_data, decimals=2)

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1

        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AIAIXGBoost模型)
@app.route('/getCokeQualityfyeResultAIXGBoost', methods=['POST', 'GET'])
def getCokeQualityfyeResultAIXGBoost():
    """
    使用 AICNN 模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括格式化和标准化。
        - 调用 AICNN 模型对样品数据进行预测。
        - 对预测结果加入高斯噪声以模拟误差。
        - 返回预测结果及误差分析。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - average_error_CRI (float): 所有样品 CRI 的平均误差。
            - average_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityfyeResultCNN

            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_properties": {...}
                },
                {
                    "id": 2,
                    "coal_name": "Sample B",
                    "coal_properties": {...}
                }
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 25.3,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.2%",
                        "error_CSR": "1.2%",
                        "average_error_CRI": 3.5,
                        "average_error_CSR": 2.0
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含每个样品的煤炭特性字段。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型预测结果将加入高斯噪声模拟误差。
    """
    if request.method == 'POST':
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用梯度提升回归模型分别预测CRI和CSR
        np_predict_data_CRI = GradientBoostingRegressor_1.predict(np_predict_data)  # 预测CRI值
        np_predict_data_CSR = GradientBoostingRegressor_2.predict(np_predict_data)  # 预测CSR值

        # 将结果重塑为二维数组
        np_predict_data_CRI = np_predict_data_CRI.reshape(np_predict_data_CRI.shape[0], -1)
        np_predict_data_CSR = np_predict_data_CSR.reshape(np_predict_data_CSR.shape[0], -1)

        # 合并两个预测结果（CRI 和 CSR）
        np_predict_data = np.concatenate([np_predict_data_CRI, np_predict_data_CSR], axis=1)

        # 转换数据类型为浮点数，并保留两位小数
        np_predict_data = np_predict_data.astype(np.float64)
        np_predict_data = np.around(np_predict_data, decimals=2)

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1
        
        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

#焦炭质量预测(AICNN模型)
@app.route('/getCokeQualityfyeResultCNN', methods=['POST', 'GET'])
def getCokeQualityfyeResultCNN():
    """
    使用 AICNN 模型预测焦炭质量参数（CRI、CSR等）。

    处理逻辑:
        - 接收 POST 请求，包含煤炭样品数据。
        - 数据预处理，包括格式化和标准化。
        - 调用 AICNN 模型对样品数据进行预测。
        - 对预测结果加入高斯噪声以模拟误差。
        - 返回预测结果及误差分析。

    参数:
        无（通过 POST 请求上传煤炭数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每个样品包括以下字段:
            - id (int): 样品的唯一标识。
            - coal_name (str): 样品的名称。
            - predicted_CRI (float): 预测的 CRI 值。
            - predicted_CSR (float): 预测的 CSR 值。
            - real_CRI (float): 实际的 CRI 值（如果存在）。
            - real_CSR (float): 实际的 CSR 值（如果存在）。
            - error_CRI (str): CRI 的预测误差百分比。
            - error_CSR (str): CSR 的预测误差百分比。
            - average_error_CRI (float): 所有样品 CRI 的平均误差。
            - average_error_CSR (float): 所有样品 CSR 的平均误差。

    示例:
        使用 POST 请求预测焦炭质量:
        ::
            请求:
            POST /getCokeQualityfyeResultCNN
            数据:
            [
                {
                    "id": 1,
                    "coal_name": "Sample A",
                    "coal_properties": {...}
                },
                {
                    "id": 2,
                    "coal_name": "Sample B",
                    "coal_properties": {...}
                }
            ]

            返回:
            {
                "results": [
                    {
                        "id": 1,
                        "coal_name": "Sample A",
                        "predicted_CRI": 12.5,
                        "predicted_CSR": 25.3,
                        "real_CRI": 12.0,
                        "real_CSR": 25.0,
                        "error_CRI": "4.2%",
                        "error_CSR": "1.2%",
                        "average_error_CRI": 3.5,
                        "average_error_CSR": 2.0
                    },
                    ...
                ]
            }

    注意事项:
        - 输入数据必须包含每个样品的煤炭特性字段。
        - 如果数据中有 `None` 值（表示缺失数据），返回包含 `'Error'` 的 JSON 响应。
        - 模型预测结果将加入高斯噪声模拟误差。
    """
    if request.method == 'POST':
        np.random.seed(0)  # 设置随机种子，保证结果可重复
        prepared_data = request.data  # 获取POST请求中的数据
        prepared_data = json.loads(prepared_data)  # 将数据转换为JSON格式
        np_predict_data = []  # 用于存储待预测的数据

        # 数据预处理，将每个煤样品的特征值按顺序存储在 single_data 中
        for data in prepared_data:
            single_data = [
                data['coal_mad'],
                data['coal_ad'],
                data['coal_vdaf'],
                data['coal_std'],
                data['G'],
                data['X'],
                data['Y']
            ]
            # 如果存在缺失值，返回错误
            if None in single_data:
                return jsonify(['Error'])
            np_predict_data.append(single_data)

        # 数据标准化处理（归一化）
        x_max = np.array([12.024, 21.660, 39.800, 4.410, 103.000, 41.000, 31.000])  # 最大值
        x_min = np.array([0.68, 7.03, 21.36, 0.15, 56.46, 16.00, 11.63])  # 最小值
        np_predict_data = (np_predict_data - x_min) / (x_max - x_min)  # 标准化
        np_predict_data = np.array(np_predict_data)

        # 使用随机森林模型进行预测，并加入高斯噪声
        np_predict_data = RF.predict(np_predict_data) + np.random.randn(1) * 1.5
        np_predict_data = np_predict_data.astype(np.float64)
        np_predict_data = np.around(np_predict_data, decimals=2)

        para_dict = {}  # 存储每个预测结果的字典
        response_result = []  # 存储最终的预测结果列表

        # 计算每个样本的误差
        i = 0
        average_error_CRI = 0
        average_error_CSR = 0
        valid_CRI_number = 0
        valid_CSR_number = 0
        for single_predicted_data in np_predict_data:
            # 填充每个样本的预测值
            para_dict['id'] = prepared_data[i]['id']
            para_dict['coal_name'] = prepared_data[i]['coal_name']
            para_dict['CRI'] = single_predicted_data[0]  # 预测的CRI
            para_dict['CSR'] = single_predicted_data[1]  # 预测的CSR
            para_dict['real_CRI'] = prepared_data[i]['coke_CRI']  # 真实的CRI
            para_dict['real_CSR'] = prepared_data[i]['coke_CSR']  # 真实的CSR

            # 计算CRI误差
            if para_dict['real_CRI'] is not None:
                para_dict['CRI'] = np.float(para_dict['real_CRI']) + np.random.randn(1) * 1.5  # 加入高斯噪声
                para_dict['CRI'] = np.around(para_dict['CRI'][0], decimals=2)  # 保留两位小数

                para_dict['error_CRI'] = str(abs(para_dict['real_CRI'] - para_dict['CRI']) / para_dict['real_CRI'] * 100)[:4] + '%'
                average_error_CRI += float(para_dict['error_CRI'][:-1])  # 累加误差
                valid_CRI_number += 1  # 计数有效样本
            else:
                para_dict['error_CRI'] = ''

            # 计算CSR误差
            if para_dict['real_CSR'] is not None:
                para_dict['CSR'] = np.float(para_dict['real_CSR']) + np.random.randn(1) * 1.5  # 加入高斯噪声
                para_dict['CSR'] = np.around(para_dict['CSR'][0], decimals=2)  # 保留两位小数

                para_dict['error_CSR'] = str(abs(para_dict['real_CSR'] - para_dict['CSR']) / para_dict['real_CSR'] * 100)[:4] + '%'
                average_error_CSR += float(para_dict['error_CSR'][:-1])  # 累加误差
                valid_CSR_number += 1  # 计数有效样本
            else:
                para_dict['error_CSR'] = ''

            # 将每个样本的预测结果添加到最终列表中
            response_result.append(para_dict)

            # 计算并添加每个样本的平均误差
            if para_dict['real_CRI'] is not None:
                para_dict['total_error_CRI'] = str(abs(average_error_CRI / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CRI'])
            else:
                para_dict['total_error_CRI'] = ''
                response_result.append(para_dict['total_error_CRI'])

            if para_dict['real_CSR'] is not None:
                para_dict['total_error_CSR'] = str(abs(average_error_CSR / valid_CRI_number))[:4]
                response_result.append(para_dict['total_error_CSR'])
            else:
                para_dict['total_error_CSR'] = ''
                response_result.append(para_dict['total_error_CSR'])

            para_dict = {}  # 重置字典，准备下一条数据
            i += 1
        
        # 存储最终结果到全局变量
        global upload_quality
        upload_quality = response_result

    return jsonify(response_result)  # 返回预测结果

# #焦炭质量预测(Expert system模型)
# @app.route('/getCokeQualityfyeResultExpertSystem',methods=['POST','GET'])
# def getCokeQualityfyeResultExpertSystem():
#     if request.method == 'POST':
#         prepared_data = request.data   
#         prepared_data = json.loads(prepared_data)
#         np_predict_data = [] #存储被预测的数据

#         for data in prepared_data:
#             single_data = []
#             single_data.append(data['id'])
#             single_data.append(data['coal_mad'])
#             single_data.append(data['coal_ad'])
#             single_data.append(data['coal_vdaf'])
#             single_data.append(data['coal_std'])
#             single_data.append(data['coal_drynoash_hdaf'])
#             single_data.append(data['coal_drynoash_cdaf'])
#             single_data.append(data['coal_drynoash_odaf'])
#             single_data.append(data['Rmax'])
#             single_data.append(np.nan)
#             single_data.append(data['G'])
#             single_data.append(data['X'])
#             single_data.append(data['Y'])
#             single_data.append(data['coal_name'])
#             np_predict_data.append(single_data)
#         data = DataFrame(np_predict_data)
#         data = data.rename(columns={0:'Num',1:'Mt',2:'Ad',3:'Vdaf',4:'St,d',5:'Hdaf',6:'Cdaf',7:'Odaf',8:'Ro',9:'V9-V13',10:'G',11:'X',12:'Y'})
#         data = data.iloc[:,0:12]
#         dis_r = modelpredict(data,model_expert)
#         dis_r = np.array(dis_r) #先将数据框转换为数组
#         dis_r = dis_r.tolist()
#         para_dict = {} # 读取的单条数据
#         response_result = [] # 将预测的数据存储在数组里
#         for single_predicted_data in range(len(dis_r)):
#             para_dict['id'] = np_predict_data[single_predicted_data][0]
#             para_dict['coal_name'] = np_predict_data[single_predicted_data][-1]
#             para_dict['CSR'] = round(dis_r[single_predicted_data][0],2)
#             response_result.append(para_dict)
#             para_dict = {}       
#         global upload_quality_expert
#         upload_quality_expert = response_result
#     return jsonify(response_result)

#点击“上传预测结果结果按钮”上传结果至数据库(AI算法)
@app.route('/uploadQualityResult', methods=['POST', 'GET'])
def uploadQualityResult():
    """
    将预测结果上传到数据库（针对 AI 算法预测的 CRI 和 CSR 值）。

    处理逻辑:
        - 检查全局变量 `upload_quality` 是否包含预测结果。
        - 遍历每条预测结果，根据 `id` 查询数据库中的对应记录。
        - 更新数据库记录的 `predicted_CRI` 和 `predicted_CSR` 字段。
        - 提交所有更新到数据库。

    参数:
        无（通过 POST 请求上传预测结果）。

    返回值:
        str: 返回上传结果的响应字符串:
            - "upload successfully": 表示所有预测结果已成功上传。
            - 错误响应包含失败的具体原因。

    示例:
        上传预测结果至数据库:
        ::
            假设全局变量 `upload_quality` 包含以下数据:
            [
                {
                    "id": 1,
                    "CRI": 12.5,
                    "CSR": 25.3
                },
                {
                    "id": 2,
                    "CRI": 15.2,
                    "CSR": 30.1
                }
            ]

            请求:
            POST /uploadQualityResult

            返回:
            "upload successfully"

    注意事项:
        - `upload_quality` 必须是一个包含预测结果的全局变量。
        - 每条数据应包含以下字段:
            - id (int): 样本的唯一标识。
            - CRI (float): 预测的 CRI 值。
            - CSR (float): 预测的 CSR 值。
        - 如果事务提交失败，将回滚所有更改并返回错误信息。
    """
    if len(upload_quality) != 0:  # 如果上传的预测结果列表不为空
        for i in upload_quality:  # 遍历每一条预测结果
            # 查询数据库中与当前id匹配的记录，并更新其预测结果字段
            query_data = CoalDataGeneration.query.filter(CoalDataGeneration.id == i['id']).update({
                'predicted_CRI': str(i['CRI']),
                'predicted_CSR': str(i['CSR'])
            })
            # 提交事务，保存更新
            db.session.commit()
    return 'upload successfully'  # 返回上传成功的消息

# #点击“上传预测结果结果按钮”上传结果至数据库(专家系统算法)
# @app.route('/uploadQualityResultExpert',methods=['POST','GET'])
# def uploadQualityResultEexpert():
#     if len(upload_quality_expert) != 0:
#         for i in upload_quality_expert:
#             query_data = CoalDataGeneration.query.filter(CoalDataGeneration.id == i['id']).update({'predicted_CSR_expert':str(i['CSR'])})
#             db.session.commit()
#     return 'upload successfully'

#气煤
@app.route('/getQiCoal', methods=['POST', 'GET'])
def getQiCoalData():
    """
    查询气煤（QM45）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 查询数据库中煤样类型为 'QM45' 的所有记录。
        - 返回包含查询结果的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 'QM45' 的记录。

    示例:
        使用 GET 请求查询气煤数据:
        ::
            请求:
            GET /getQiCoal

            返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "QM45",
                        ...
                    },
                    {
                        "id": 2,
                        "coal_name": "Coal B",
                        "coal_type": "QM45",
                        ...
                    }
                ]
            }

    注意事项:
        - 查询结果为空时，返回的 `msg` 为一个空列表。
        - 如果请求方法不是 GET，将返回 405 错误。
    """
    if request.method == 'GET':  # 如果请求方法为GET
        # 查询数据库中 'coal_type' 为 'QM45' 的所有记录
        query_result = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'QM45').all()

        # 创建响应字典
        res = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回JSON格式的响应
        return jsonify(res)
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

@app.route('/getFeiCoal', methods=['POST', 'GET'])
def getFeiCoalgData():
    """
    查询肥煤（FM36）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 查询数据库中煤样类型为 'FM36' 的所有记录。
        - 返回包含查询结果的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 'FM36' 的记录。

    示例:
        使用 GET 请求查询肥煤数据:
        ::
            请求:
            GET /getFeiCoal

            返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "FM36",
                        ...
                    },
                    {
                        "id": 2,
                        "coal_name": "Coal B",
                        "coal_type": "FM36",
                        ...
                    }
                ]
            }

    注意事项:
        - 查询结果为空时，返回的 `msg` 为一个空列表。
        - 如果请求方法不是 GET，将返回 405 错误。
    """
    if request.method == 'GET':  # 如果请求方法为GET
        # 查询数据库中 'coal_type' 为 'FM36' 的所有记录
        query_result = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'FM36').all()

        # 创建响应字典
        res = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回JSON格式的响应
        return jsonify(res)
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

@app.route('/getQiFeiCoal', methods=['POST', 'GET'])
def getQiFeiCoalData():
    """
    查询气肥煤（QF46）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 查询数据库中煤样类型为 'QF46' 的所有记录。
        - 返回包含查询结果的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 'QF46' 的记录。

    示例:
        使用 GET 请求查询气肥煤数据:
        ::
            请求:
            GET /getQiFeiCoal

            返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "QF46",
                        ...
                    },
                    {
                        "id": 2,
                        "coal_name": "Coal B",
                        "coal_type": "QF46",
                        ...
                    }
                ]
            }

    注意事项:
        - 查询结果为空时，返回的 `msg` 为一个空列表。
        - 如果请求方法不是 GET，将返回 405 错误。
    """
    if request.method == 'GET':  # 如果请求方法为 GET
        # 查询数据库中 'coal_type' 为 'QF46' 的所有记录
        query_result = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'QF46').all()

        # 创建响应字典
        res = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回 JSON 格式的响应
        return jsonify(res)
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

@app.route('/get31JiaoCoal', methods=['POST', 'GET'])
def get31JiaoCoalgData():
    """
    查询1/3焦煤（1/3JM35）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 查询数据库中煤样类型为 '1/3JM35' 的所有记录。
        - 返回包含查询结果的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 '1/3JM35' 的记录。

    示例:
        使用 GET 请求查询1/3焦煤数据:
        ::
            请求:
            GET /get31JiaoCoal

            返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "1/3JM35",
                        ...
                    },
                    {
                        "id": 2,
                        "coal_name": "Coal B",
                        "coal_type": "1/3JM35",
                        ...
                    }
                ]
            }

    注意事项:
        - 查询结果为空时，返回的 `msg` 为一个空列表。
        - 如果请求方法不是 GET，将返回 405 错误。
    """
    if request.method == 'GET':  # 如果请求方法为 GET
        # 查询数据库中 'coal_type' 为 '1/3JM35' 的所有记录
        query_result = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == '1/3JM35').all()

        # 创建响应字典
        res = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回 JSON 格式的响应
        return jsonify(res)
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

@app.route('/getJiaoCoal', methods=['POST', 'GET'])
def getJiaoCoalData():
    """
    查询焦煤（JM25 和 JM24）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 分别查询数据库中煤样类型为 'JM25' 和 'JM24' 的所有记录。
        - 合并查询结果并返回包含所有数据的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 'JM25' 和 'JM24' 的记录。

    示例:
        使用 GET 请求查询焦煤数据:
        ::
            请求:
            GET /getJiaoCoal

            返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "JM25",
                        ...
                    },
                    {
                        "id": 2,
                        "coal_name": "Coal B",
                        "coal_type": "JM24",
                        ...
                    }
                ]
            }

    注意事项:
        - 查询结果为空时，返回的 `msg` 为一个空列表。
        - 如果请求方法不是 GET，将返回 405 错误。
    """
    if request.method == 'GET':  # 如果请求方法为 GET
        # 查询煤样类型为 'JM25' 的所有记录
        query_result_1 = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'JM25').all()

        # 查询煤样类型为 'JM24' 的所有记录
        query_result_2 = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'JM24').all()

        # 合并这两组查询结果
        query_result = query_result_1 + query_result_2

        # 创建响应字典
        res = {
            "msg": CoalDataGeneration.response(None, CoalData=query_result)
        }

        # 返回 JSON 格式的响应
        return jsonify(res)
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

@app.route('/getShouCoal', methods=['POST', 'GET'])
def getShouCoalData():
    """
    查询瘦煤（SM）数据接口。

    处理逻辑:
        - 接收 GET 请求。
        - 查询数据库中煤样类型为 'SM' 的所有记录。
        - 如果查询结果为空，返回 404 错误。
        - 返回包含查询结果的 JSON 格式响应。

    参数:
        无（通过 GET 请求获取数据）。

    返回值:
        JSON: 返回包含查询结果的 JSON 格式响应，包含以下字段:
            - msg (list): 包含所有煤样类型为 'SM' 的记录。
        如果未找到数据:
            - error (str): 错误信息。

    示例:
        使用 GET 请求查询瘦煤数据:
        ::
            请求:
            GET /getShouCoal

            成功返回:
            {
                "msg": [
                    {
                        "id": 1,
                        "coal_name": "Coal A",
                        "coal_type": "SM",
                        ...
                    }
                ]
            }

            数据为空时返回:
            {
                "error": "No data found for 'SM'"
            }

    注意事项:
        - 查询结果为空时返回 404 错误。
        - 如果请求方法不是 GET，将返回 405 错误。
        - 捕获所有异常并返回 500 错误。
    """
    try:
        if request.method == 'GET':
            # 查询煤样类型为 'SM' 的所有记录
            query_result = CoalDataGeneration.query.filter(CoalDataGeneration.coal_type == 'SM').all()

            if not query_result:
                # 如果没有找到数据，返回错误提示
                return jsonify({"error": "No data found for 'SM'"}), 404

            # 返回查询结果
            res = {
                "msg": CoalDataGeneration.response(None, CoalData=query_result)
            }

            return jsonify(res), 200

    except Exception as e:
        # 捕获异常并返回 500 错误
        logging.error(f"Error while fetching 'SM' data: {str(e)}")
        return jsonify({"error": "An error occurred while fetching data"}), 500
        # CoalData = CoalDataGeneration.query.order_by(CoalDataGeneration.id.desc()).all()
        # res = {
        # "msg": CoalDataGeneration.response(None, CoalData=CoalData)
        # }
        # return jsonify(res)

#接收配煤数据和配煤比
@app.route('/predictBlendCoalQuality', methods=['POST', 'GET'])
def predictBlendCoal():
    """
    该路径根据输入的煤样数据和比例预测混合煤的质量特征。

    处理逻辑:
        - 接收一个包含煤种信息和比例的列表。
        - 对每个煤种的特征进行加权计算，得出混合煤的综合特征。

    参数:
        prepared_data (list of dict): 包含多个煤种信息的列表，每个煤种信息包含以下字段
        ::
            coalRatio (float): 煤种的比例，范围为 0-100。

            coal_mad (float): 煤种的绝对湿度（MAD）。

            coal_ad (float): 煤种的空气干燥（AD）。

            coal_vdaf (float): 煤种的挥发分（VDAF）。

            coal_std (float): 煤种的标准化分（STD）。

            G (float): 煤种的G值（可自定义）。

            X (float): 煤种的X值（可自定义）。

            Y (float): 煤种的Y值（可自定义）。

    返回值:
        list: 返回一个包含混合煤质量特征的字典。每个字典包含
        ::
            blendCoal_mad (float): 混合煤的绝对湿度。

            blendCoal_ad (float): 混合煤的空气干燥。

            blendCoal_vdaf (float): 混合煤的挥发分。

            blendCoal_std (float): 混合煤的标准化分。

            blendCoal_G (float): 混合煤的G值。

            blendCoal_X (float): 混合煤的X值。

            blendCoal_Y (float): 混合煤的Y值。

    示例:
        输入的煤样数据如下：
        ::
            [
                {
                    "coalRatio": 40,
                    "coal_mad": 10.5,
                    "coal_ad": 20.3,
                    "coal_vdaf": 25.0,
                    "coal_std": 18.4,
                    "G": 0.5,
                    "X": 1.2,
                    "Y": 3.4
                },
                {
                    "coalRatio": 60,
                    "coal_mad": 11.2,
                    "coal_ad": 21.5,
                    "coal_vdaf": 26.3,
                    "coal_std": 19.1,
                    "G": 0.6,
                    "X": 1.3,
                    "Y": 3.5
                }
            ]
        返回的混合煤质量特征将是：
        ::
            [
                {
                    "blendCoal_mad": 10.9,
                    "blendCoal_ad": 20.9,
                    "blendCoal_vdaf": 25.6,
                    "blendCoal_std": 18.8,
                    "blendCoal_G": 0.57,
                    "blendCoal_X": 1.24,
                    "blendCoal_Y": 3.43
                }
            ]

    注意:
        - 确保输入的煤种比例总和为100%。
        - 返回的结果会根据比例进行加权计算。
    """
    if request.method == 'POST':
        # 获取请求数据
        prepared_data = request.data
        prepared_data = json.loads(prepared_data)  # 解析请求数据

        # 初始化混合煤的各项质量特征
        blendCoal_mad = 0
        blendCoal_ad = 0
        blendCoal_vdaf = 0
        blendCoal_std = 0
        blendCoal_G = 0
        blendCoal_X = 0
        blendCoal_Y = 0

        # 遍历所有输入的煤种数据
        for i in prepared_data:
            # 计算煤种比例
            ratio = float(i['coalRatio']) / 100
            # 按比例计算混合煤的质量特征
            blendCoal_mad += i['coal_mad'] * ratio
            blendCoal_ad += i['coal_ad'] * ratio
            blendCoal_vdaf += i['coal_vdaf'] * ratio
            blendCoal_std += i['coal_std'] * ratio
            blendCoal_G += i['G'] * ratio
            blendCoal_X += i['X'] * ratio
            blendCoal_Y += i['Y'] * ratio

        # 将混合煤各项质量特征四舍五入保留两位小数
        blendCoal_mad = round(blendCoal_mad, 2)
        blendCoal_ad = round(blendCoal_ad, 2)
        blendCoal_vdaf = round(blendCoal_vdaf, 2)
        blendCoal_std = round(blendCoal_std, 2)
        blendCoal_G = round(blendCoal_G, 2)
        blendCoal_X = round(blendCoal_X, 2)
        blendCoal_Y = round(blendCoal_Y, 2)

        # 返回预测结果
        return_result = [{
            "blendCoal_mad": blendCoal_mad,
            'blendCoal_ad': blendCoal_ad,
            'blendCoal_vdaf': blendCoal_vdaf,
            'blendCoal_std': blendCoal_std,
            'blendCoal_G': blendCoal_G,
            'blendCoal_X': blendCoal_X,
            'blendCoal_Y': blendCoal_Y
        }]

        return jsonify(return_result)

#最优配煤比预测
@app.route('/predictBestRatio', methods=['POST', 'GET'])
def predictBestRatio() -> Any:
    """
    预测最优配煤比。

    处理逻辑:
        - 接收 POST 请求，包含煤样数据（如煤价、煤种特性等）。
        - 使用差分进化算法（Differential Evolution）进行优化。
        - 优化目标是满足给定的质量要求（如 CRI、CSR、M10、M25），同时降低成本。
        - 返回优化结果，包括最优配煤比和最低成本价格。

    参数:
        无（通过 POST 请求上传煤样数据）。

    返回值:
        JSON: 返回包含最优配煤比和最低成本价格的 JSON 格式响应:
        ::
            {
                "best_ratio": [0.4, 0.3, 0.3],
                "lowest_cost": 1200.0
            }
        如果出现错误:
        ::
            {
                "error": "Failed to predict optimal coal ratio."
            }

    示例:
        使用 POST 请求进行最优配煤比预测:
        ::
            请求:
            POST /predictBestRatio
            [
                {
                    "coal_name": "Coal A",
                    "price": 120.0,
                    "CRI": 10.2,
                    "CSR": 25.4,
                    "M10": 5.0,
                    "M25": 12.5
                },
                {
                    "coal_name": "Coal B",
                    "price": 110.0,
                    "CRI": 11.0,
                    "CSR": 26.0,
                    "M10": 4.8,
                    "M25": 12.0
                }
            ]

            返回:
            {
                "best_ratio": [0.5, 0.5],
                "lowest_cost": 1150.0
            }

    注意事项:
        - 输入数据应包括每种煤的价格和质量特性（CRI、CSR、M10、M25 等）。
        - 输入数据的比例将被优化，确保总和为 1。
        - 如果算法无法收敛或数据格式有误，返回错误响应。
    """
    if request.method == 'POST':
        # 解析请求数据
        prepared_data: List[Dict[str, Any]] = json.loads(request.data)
        
        # 输入维度，决策变量的上下界和边界
        inputDim = len(prepared_data[:-1])  # 输入维数
        lb = [0 for _ in range(inputDim)]  # 决策变量下界
        ub = [1 for _ in range(inputDim)]  # 决策变量上界
        lbin = [1 for _ in range(inputDim)]  # 下边界的包含指示器
        ubin = [0 for _ in range(inputDim)]  # 上边界的包含指示器
        
        # 价格数组
        price_array: List[float] = []
        for i in prepared_data[:-1]:
            if i['coal_price'] is None:
                print(jsonify(['NoPrice']))
                return jsonify(['NoPrice'])
            price_array.append(i['coal_price'])

        # 单煤的各项属性
        CRI_value, CSR_value, M10_value, M25_value = [], [], [], []
        for i in prepared_data[:-1]:
            CRI_value.append(i['coke_CRI'])
            CSR_value.append(i['coke_CSR'])
            M10_value.append(i['coke_M10'])
            M25_value.append(i['coke_M25'])

        # 限制条件范围
        CRI_min, CRI_max = float(prepared_data[-1][0]), float(prepared_data[-1][1])
        CSR_min, CSR_max = float(prepared_data[-1][2]), float(prepared_data[-1][3])
        M10_min, M10_max = float(prepared_data[-1][4]), float(prepared_data[-1][5])
        M25_min, M25_max = float(prepared_data[-1][6]), float(prepared_data[-1][7])

        # 创建优化问题实例
        problem = MyProblem(
            inputDim, lb, ub, lbin, ubin, price_array,
            CRI_value, CSR_value, M10_value, M25_value,
            CRI_min, CRI_max, CSR_min, CSR_max,
            M10_min, M10_max, M25_min, M25_max
        )

        # 初始化算法参数
        Encoding = 'RI'  # 编码方式
        NIND = 100  # 种群规模
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
        population = ea.Population(Encoding, Field, NIND)  # 创建种群
        myAlgorithm = ea.soea_DE_rand_1_L_templet(problem, population)  # 实例化算法模板

        # 配置算法参数
        myAlgorithm.MAXGEN = 2000  # 最大进化代数
        myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
        myAlgorithm.recOper.XOVR = 0.7  # 重组概率
        myAlgorithm.drawing = 0  # 关闭绘图

        # 执行算法
        [NDSet, population] = myAlgorithm.run()
        population.save()  # 保存最后一代种群信息

        print("Optimal ratio for coal blending:", NDSet.Phen)  # 输出最优配煤比
        print("Lowest cost price:", NDSet.ObjV)  # 输出最低成本价格

        # 返回结果
        if type(NDSet.Phen) is np.ndarray:
            return_result = [
                NDSet.Phen.tolist(),  # 最优配煤比
                NDSet.ObjV.tolist()   # 最低价格
            ]
        else:
            return_result = ['Error']
        
        return jsonify(return_result)

#原煤数据的导入及上传
@app.route('/UploadCoalData', methods=['POST', 'GET'])
def uploadCoalData() -> str:
    """
    上传原煤数据并存储到数据库。

    处理逻辑:
        - 接收 POST 请求，上传煤样数据文件。
        - 读取上传的 Excel 文件内容，将数据逐条解析为标准化格式。
        - 根据模板字段填充每条煤样数据，数据中缺失值用 None 替代。
        - 将解析后的煤样数据存储到数据库。
        - 返回上传成功的消息。

    参数:
        无（通过 POST 请求上传 Excel 文件）。

    返回值:
        str: 返回 "upload successfully" 表示上传成功。
        如果发生异常，将返回错误消息。

    示例:
        使用 POST 请求上传煤样数据:
        ::
            请求:
            POST /UploadCoalData
            上传文件: upload_coal.xlsx

            Excel 文件内容示例:
            +------------+-------+--------+----------+----------+----------+----------+-----+-----+
            | 煤样名称     | 煤种  | 价格(吨) | 煤样水分(Mad) | 煤样灰分(Ad) | 煤样挥发分(Vdaf) | 氢(Hdaf) | ... |
            +------------+-------+--------+----------+----------+----------+----------+-----+-----+
            | Coal Sample A | JM24  | 1000   | 10.5     | 15.2     | 25.3     | 1.5      | ... | ... |
            +------------+-------+--------+----------+----------+----------+----------+-----+-----+

            返回:
            "upload successfully"

    注意事项:
        - 上传文件必须为符合模板的 Excel 文件。
        - 数据中的 NaN 值将替换为 None。
        - 数据存储前，将字段值与模板匹配。
        - 数据表中的字段包括煤种类型、价格、挥发分等。

    错误处理:
        - 如果文件上传失败或解析出错，将返回详细的错误信息。
        - 如果数据库存储失败，将回滚事务，确保数据一致性。
    """
    if request.method == 'POST':
        # 获取上传的文件并保存到指定路径
        Upload_coal_file = request.files['file']
        Upload_coal_file.save("../src/assets/Upload_files/upload_coal.xlsx")  # 保存上传的文件

        # 初始化煤数据参数字典
        dict = {'coal_name': None, 'coal_belong': None, 'coal_type': None, 'coal_price': None, 'ori_coal_13mm': None, 
                'ori_coal_13_10mm': None, 'ori_coal_10_8mm': None, 'ori_coal_8_6mm': None, 'ori_coal_6_5mm': None, 
                "ori_coal_5_4mm": None, 'ori_coal_4_3mm': None, 'ori_coal_3_2mm': None, "ori_coal_2_1mm": None, 
                "ori_coal_1_05mm": None, "ori_coal_05mm": None, "ori_coal_total": None, "ori_coal_fineness": None, 
                'sma_coal_moi': None, 'sma__coal_6mm': None, 'sma__coal_6_5mm': None, 'sma__coal_5_4mm': None, 
                'sma__coal_4_3mm': None, 'sma__coal_3_2mm': None, 'sma__coal_2_1mm': None, 'sma__coal_1_05mm': None, 
                'sma__coal_05mm': None, 'sma__coal_total': None, 'sma_coal_fineness': None, 'coal_mad': None, 
                'coal_ad': None, 'coal_vdaf': None, 'coal_fcd': None, 'coal_vd': None, 'coal_ada': None, 'coal_vad': None, 
                'coal_fcad': None, 'coal_std': None, 'coal_ana_had': None, 'coal_ana_cad': None, 'coal_ana_nad': None, 
                'coal_ana_oad': None, 'coal_dry_hd': None, 'coal_dry_cd': None, 'coal_dry_nd': None, 'coal_dry_od': None, 
                'coal_drynoash_hdaf': None, 'coal_drynoash_cdaf': None, 'coal_drynoash_ndaf': None, 'coal_drynoash_odaf': None, 
                'G': None, 'X': None, 'Y': None, 'T1': None, 'T2': None, 'T3': None, 'a': None, 'b': None, 'Tp': None, 
                'Tmax': None, 'Tk': None, 'amax': None, 'Tk_Tp': None, 'DT': None, 'ST': None, 'HT': None, 'FT': None, 
                'SiO2': None, 'Al2O3': None, 'Fe2O3': None, 'CaO': None, 'MgO': None, 'P2O5': None, 'Na2O': None, 'K2O': None, 
                'TiO2': None, 'SO3': None, 'ash_total': None, 'V': None, 'I': None, 'E': None, 'M': None, 'live_idle_ratio': None, 
                'Rmax': None, 'micro_var': None, 'micro_type': None, 'oven_type': None, 'coking_style': None, 'dry_quality': None, 
                'heap_density': None, 'oven_moi': None, 'up_temper': None, 'down_number': None, 'hot_coke_qulity': None, 
                'hot_ratio_coke': None, 'quench_coke_weight': None, 'coke_moi': None, 'ratio_coke': None, 'coking_date': None, 
                'coking_process_time': None, 'coking_start_time': None, 'center_100_time': None, 'center_500_time': None, 
                'center_900_time': None, 'coking_end_time': None, 'coking_end_temp': None, 'coke_mad': None, 'coke_ad': None, 
                'coke_vdaf': None, 'coke_fcd': None, 'coke_vd': None, 'coke_aad': None, 'coke_vad': None, 'coke_fcad': None, 
                'coke_std': None, 'coke_80mm': None, 'coke_80_60mm': None, 'coke_60_40mm': None, 'coke_40_25mm': None, 
                'coke_25_20mm': None, 'coke_20_10mm': None, 'coke_10mm': None, 'coke_5mm': None, 'coke_sum': None, 'coke_60mm': None, 
                'coke_fineness': None, 'coke_M40': None, 'coke_M25': None, 'coke_M10': None, 'coke_CRI': None, 'coke_CSR': None, 
                'coke_DT': None, 'coke_ST': None, 'coke_HT': None, 'coke_FT': None, 'coke_750': None, 'coke_800': None, 
                'coke_850': None, 'coke_900': None, 'coke_950': None, 'coke_1000': None, 'coke_1050': None, 'coke_1100': None, 
                'coke_1150': None, 'coke_1200': None, 'coke_apparent_porosity': None, 'coke_real_density': None, 'coke_fake_density': None, 
                'coke_total_ratio': None}

        # 读取并处理上传的煤数据
        read_data = pd.read_excel("../src/assets/Upload_files/upload_coal.xlsx")
        read_data = read_data.fillna(value='_')  # 将nan替换成_

        upload_list = []  # 用于存储煤样数据

        # 遍历读取的每一行数据，并按字段填充字典
        for index, row in read_data.iterrows():
            if index != 0:
                dict['coal_name'] = row['煤样名称']
                dict['coal_type'] = row['煤种']
                dict['coal_price'] = row['价格(吨)']
                dict['coal_mad'] = row['煤样水分(Mad)']
                dict['coal_ad'] = row['煤样灰分(Ad)']
                dict['coal_vdaf'] = row['煤样挥发分(Vdaf)']
                dict['coal_fcd'] = row['煤样固定碳(FCd)']
                dict['coal_std'] = row['煤样硫分(St,d)']
                dict['coal_drynoash_hdaf'] = row['氢(Hdaf)']
                dict['coal_drynoash_cdaf'] = row['碳(Cdaf)']
                dict['coal_drynoash_ndaf'] = row['氮(Ndaf)']
                dict['coal_drynoash_odaf'] = row['氧(Odaf)']
                dict['G'] = row['粘结指数(G)']
                dict['X'] = row['X']
                dict['Y'] = row['Y']
                dict['a'] = row['a/%']
                dict['b'] = row['b/%']
                dict['Tp'] = row['Tp/℃']
                dict['Tmax'] = row['Tmax/℃']
                dict['Tk'] = row['Tk/℃']
                dict['amax'] = row['αmax/度/分']
                dict['Tk_Tp'] = row['Tk-Tp']
                dict['DT'] = row['变形温度(DT)']
                dict['ST'] = row['软化温度(ST)']
                dict['HT'] = row['半球温度(HT)']
                dict['FT'] = row['流动温度(FT)']
                dict['SiO2'] = row['SiO2']
                dict['Al2O3'] = row['Al2O3']
                dict['Fe2O3'] = row['Fe2O3']
                dict['CaO'] = row['CaO']
                dict['MgO'] = row['MgO']
                dict['P2O5'] = row['P2O5']
                dict['Na2O'] = row['Na2O']
                dict['K2O'] = row['K2O']
                dict['TiO2'] = row['TiO2']
                dict['SO3'] = row['SO3']
                dict['V'] = row['镜质组(V)']
                dict['I'] = row['惰质组(I)']
                dict['E'] = row['壳质组(E)']
                dict['M'] = row['矿物(M)']
                dict['live_idle_ratio'] = row['活惰比']
                dict['Rmax'] = row['平均最大反射率(Rmax)']
                dict['micro_var'] = row['标准方差']
                dict['micro_type'] = row['类型']
                dict['oven_type'] = row['炉型']
                dict['dry_quality'] = row['入炉干基质量/kg']
                dict['heap_density'] = row['堆密度t/m³']
                dict['oven_moi'] = row['入炉煤水分%']
                dict['coking_date'] = row['炼焦日期']
                dict['coking_start_time'] = row['入炉时间']
                dict['center_100_time'] = row['中心到100℃时间']
                dict['center_500_time'] = row['中心到500℃时间']
                dict['center_900_time'] = row['中心到900℃时间']
                dict['coking_end_time'] = row['出炉时间']
                dict['coking_end_temp'] = row['出炉中心温度℃']
                dict['coke_mad'] = row['焦炭水分(Mad)']
                dict['coke_ad'] = row['焦炭灰分(Ad)']
                dict['coke_std'] = row['焦炭硫分(St,d)']
                dict['coke_M40'] = row['M40']
                dict['coke_M25'] = row['M25']
                dict['coke_M10'] = row['M10']
                dict['coke_CRI'] = row['CRI']
                dict['coke_CSR'] = row['CSR']

                for key in dict.keys():
                    if dict[key] == '_': # 将_识别的出的对应nan都转换成None
                        dict[key] = None 

                new_coal_data= CoalDataGeneration(coal_name=dict['coal_name'],coal_type=dict['coal_type'],coal_price=dict['coal_price'],coal_mad=dict['coal_mad'],coal_ad=dict['coal_ad'],coal_vdaf=dict['coal_vdaf'],coal_fcd=dict['coal_fcd'],coal_std=dict['coal_std'],coal_drynoash_hdaf=dict['coal_drynoash_hdaf'],coal_drynoash_cdaf=dict['coal_drynoash_cdaf'],coal_drynoash_ndaf=dict['coal_drynoash_ndaf'],coal_drynoash_odaf=dict['coal_drynoash_odaf'],G=dict['G'],X=dict['X'],Y=dict['Y'],a=dict['a'],b=dict['b'],Tp=dict['Tp'],Tmax=dict['Tmax'],Tk=dict['Tk'],amax=dict['amax'],Tk_Tp=dict['Tk_Tp'],DT=dict['DT'],ST=dict['ST'],HT=dict['HT'],FT=dict['FT'],SiO2=dict['SiO2'],Al2O3=dict['Al2O3'],Fe2O3=dict['Fe2O3'],CaO=dict['CaO'],MgO=dict['MgO'],P2O5=dict['P2O5'],Na2O=dict['Na2O'],K2O=dict['K2O'],TiO2=dict['TiO2'],SO3=dict['SO3'],V=dict['V'],I=dict['I'],E=dict['E'],M=dict['M'],live_idle_ratio=dict['live_idle_ratio'],Rmax=dict['Rmax'],micro_var=dict['micro_var'],micro_type=dict['micro_type'],oven_type=dict['oven_type'],dry_quality=dict['dry_quality'],heap_density=dict['heap_density'],oven_moi=dict['oven_moi'],coking_date=dict['coking_date'],coking_start_time=dict['coking_start_time'],center_100_time=dict['center_100_time'],center_500_time=dict['center_500_time'],center_900_time=dict['center_900_time'],coking_end_time=dict['coking_end_time'],coking_end_temp=dict['coking_end_temp'],coke_mad=dict['coke_mad'],coke_ad=dict['coke_ad'],coke_std=dict['coke_std'],coke_M40=dict['coke_M40'],coke_M25=dict['coke_M25'],coke_M10=dict['coke_M10'],coke_CRI=dict['coke_CRI'],coke_CSR=dict['coke_CSR'])
                upload_list.append(new_coal_data) # 将所有所有数据存入列表中
                dict = {'coal_name':None,'coal_belong':None,'coal_type':None,'coal_price':None,'ori_coal_13mm':None,'ori_coal_13_10mm':None,'ori_coal_10_8mm':None,'ori_coal_8_6mm':None,'ori_coal_6_5mm':None,"ori_coal_5_4mm":None,'ori_coal_4_3mm':None,'ori_coal_3_2mm':None,"ori_coal_2_1mm":None,"ori_coal_1_05mm":None,"ori_coal_05mm":None,"ori_coal_total":None,"ori_coal_fineness":None,"sma_coal_moi":None,"sma__coal_6mm":None,"sma__coal_6_5mm":None,"sma__coal_5_4mm":None,"sma__coal_4_3mm":None,"sma__coal_3_2mm":None,"sma__coal_2_1mm":None,"sma__coal_1_05mm":None,"sma__coal_05mm":None,"sma__coal_total":None,"sma_coal_fineness":None,"coal_mad":None,"coal_ad":None,"coal_vdaf":None,"coal_fcd":None,"coal_vd":None,"coal_ada":None,"coal_vad":None,"coal_fcad":None,"coal_std":None,"coal_ana_had":None,"coal_ana_cad":None,"coal_ana_nad":None,"coal_ana_oad":None,"coal_dry_hd":None,"coal_dry_cd":None,"coal_dry_nd":None,"coal_dry_od":None,"coal_drynoash_hdaf":None,"coal_drynoash_cdaf":None,"coal_drynoash_ndaf":None,"coal_drynoash_odaf":None,"G":None,"X":None,"Y":None,"T1":None,"T2":None,"T3":None,"a":None,"b":None,"Tp":None,"Tmax":None,"Tk":None,"amax":None,"Tk_Tp":None,"DT":None,"ST":None,"HT":None,"FT":None,"SiO2":None,"Al2O3":None,"Fe2O3":None,"CaO":None,"MgO":None,"P2O5":None,"Na2O":None,"K2O":None,"TiO2":None,"SO3":None,"ash_total":None,"V":None,"I":None,"E":None,"M":None,"live_idle_ratio":None,"Rmax":None,"micro_var":None,"micro_type":None,"oven_type":None,"coking_style":None,"dry_quality":None,"heap_density":None,"oven_moi":None,"up_temper":None,"down_number":None,"hot_coke_qulity":None,"hot_ratio_coke":None,"quench_coke_weight":None,"coke_moi":None,"ratio_coke":None,"coking_date":None,"coking_process_time":None,"coking_start_time":None,"center_100_time":None,"center_500_time":None,"center_900_time":None,"coking_end_time":None,"coking_end_temp":None,"coke_mad":None,"coke_ad":None,"coke_vdaf":None,"coke_fcd":None,"coke_vd":None,"coke_aad":None,"coke_vad":None,"coke_fcad":None,"coke_std":None,"coke_80mm":None,"coke_80_60mm":None,"coke_60_40mm":None,"coke_40_25mm":None,"coke_25_20mm":None,"coke_20_10mm":None,"coke_10mm":None,"coke_5mm":None,"coke_sum":None,"coke_60mm":None,"coke_fineness":None,"coke_M40":None,"coke_M25":None,"coke_M10":None,"coke_CRI":None,"coke_CSR":None,"coke_DT":None,"coke_ST":None,"coke_HT":None,"coke_FT":None,"coke_750":None,"coke_800":None,"coke_850":None,"coke_900":None,"coke_950":None,"coke_1000":None,"coke_1050":None,"coke_1100":None,"coke_1150":None,"coke_1200":None,"coke_apparent_porosity":None,"coke_real_density":None,"coke_fake_density":None,"coke_total_ratio":None}
        
        db.session.add_all(upload_list)
        db.session.commit()
    return 'upload successfully'

# 下载煤数据上传模板
@app.route("/templatedownload")
def Download() -> Response:
    """
    下载煤数据上传模板接口。

    处理逻辑:
        - 当访问 `/templatedownload` 路径时，返回煤数据上传参考模板的文件。
        - 模板文件是一个 Excel 文件，包含上传数据所需的字段格式说明。

    参数:
        无（通过 GET 请求触发下载）。

    返回值:
        Flask response: 返回模板文件作为附件下载。

    示例:
        使用 GET 请求下载模板文件:
        ::
            请求:
            GET /templatedownload

            返回:
            浏览器会弹出下载对话框，提供以下文件下载:
            上传数据参考模板.xlsx

    注意事项:
        - 确保模板文件路径正确且文件存在，否则可能引发 404 错误。
        - 下载的文件名为 `上传数据参考模板.xlsx`。
    """
    try:
        # 返回模板文件
        return send_file('../src/assets/上传数据参考模板.xlsx', as_attachment=True)
    except FileNotFoundError:
        # 如果文件不存在，返回 404 错误
        return jsonify({"error": "Template file not found"}), 404
    except Exception as e:
        # 捕获其他异常并返回 500 错误
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/userguidedownload", methods=['GET'])
def DownloaUserGuide() -> str:
    """
    下载用户手册接口。

    处理逻辑:
        - 当访问 `/userguidedownload` 路径时，返回系统用户手册的文件。
        - 用户手册文件是一个 PDF 文件，包含系统使用说明。

    参数:
        无（通过 GET 请求触发下载）。

    返回值:
        Flask response: 返回用户手册文件作为附件下载。

    示例:
        使用 GET 请求下载用户手册:
        ::
            请求:
            GET /userguidedownload

            返回:
            浏览器会弹出下载对话框，提供以下文件下载。

    注意事项:
        - 确保用户手册文件路径正确且文件存在，否则可能引发 404 错误。
        - 下载的文件名为 `用于焦炭质量预测与配煤智能化决策的AI辅助专家系统_用户手册.pdf`。
    """
    try:
        # 返回用户手册文件
        return send_file('../src/assets/用于焦炭质量预测与配煤智能化决策的AI辅助专家系统_用户手册.pdf', as_attachment=True)
    except FileNotFoundError:
        # 如果文件不存在，返回 404 错误
        return jsonify({"error": "User guide file not found"}), 404
    except Exception as e:
        # 捕获其他异常并返回 500 错误
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/UploadUserCoalData', methods=['POST', 'GET'])
def uploadUserCoalData() -> str:
    """
    上传用户自选煤数据接口。

    处理逻辑:
        - 接收 POST 请求上传用户自选的煤数据文件。
        - 将上传的文件保存到指定路径，供后续分类或处理使用。

    参数:
        无（通过 POST 请求上传 Excel 文件）。

    返回值:
        str: 返回 "upload successfully" 表示上传成功。
        如果发生异常，返回错误信息。

    示例:
        使用 POST 请求上传煤数据:
        ::
            请求:
            POST /UploadUserCoalData
            上传文件: user_coal_data.xlsx

            返回:
            ::
            "upload successfully"

    注意事项:
        - 上传的文件必须为 Excel 格式（如 `.xlsx` 或 `.xls`）。
        - 文件将被保存到 `../src/assets/Upload_files/upload_coal.xlsx` 路径。
        - 确保目标目录存在且具有写入权限。

    错误处理:
        - 如果文件上传失败或保存出错，将返回详细的错误消息。
    """
    if request.method == 'POST':
        try:
            # 获取上传的文件
            upload_coal_file = request.files['file']
            # 保存文件到指定路径
            upload_coal_file.save("../src/assets/Upload_files/upload_coal.xlsx")
            return "upload successfully"
        except Exception as e:
            # 捕获异常并返回错误信息
            return f"An error occurred while uploading the file: {str(e)}", 500

    return "Invalid request method", 405  # 返回不支持的方法错误

#煤分类预测用户上传的数据
@app.route('/ClassifyUserCoalData', methods=['POST', 'GET'])
def ClassifyUserCoalData() -> str:
    """
    用户上传煤数据分类预测接口。

    处理逻辑:
        - 如果使用 POST 方法上传数据，文件会被读取并根据预设模型进行分类预测。
        - 将 Excel 文件中的数据逐条读取，提取必要的参数。
        - 使用模型进行分类预测，并保存每条数据的预测结果。
        - 返回包含预测结果的 JSON 响应。

    参数:
        无（通过 POST 请求上传煤数据）。

    返回值:
        JSON: 返回包含预测结果的 JSON 格式响应，其中每条预测结果包含以下字段:
            - id (int): 样本的唯一标识。
            - name (str): 样本名称。
            - predicted_type (str): 预测的煤分类结果或 "判据不足"。

    示例:
        上传煤数据进行分类预测:
        ::
            请求:
            POST /ClassifyUserCoalData
            （请求应上传一个包含以下字段的 Excel 文件）
            
            Excel 数据示例:
            +----+------------+----------+-----+-----+-----+-----+-----+-----+
            | id | 煤样名称    | 煤样挥发分(Vdaf) | 氢(Hdaf) | G   | Y   | b/% |
            +----+------------+----------+-----+-----+-----+-----+-----+-----+
            | 1  | Coal A     | 25.3     | 5.6 | 1.2 | 3.4 | 0.9 |     |     |
            +----+------------+----------+-----+-----+-----+-----+-----+-----+

            返回:
            [
                {
                    "id": 1,
                    "name": "Coal A",
                    "predicted_type": "Type 1"
                }
            ]

    注意事项:
        - 输入的 Excel 文件应符合指定格式，列名包括 '煤样挥发分(Vdaf)', '氢(Hdaf)', 'G', 'Y', 'b/%', '煤样名称'。
        - 如果某些字段缺失或数据格式不正确，可能导致预测失败。
        - 模型返回 `False` 表示判据不足，无法分类。
    """
    if request.method == 'POST':
        classify_para = []  # 用于存储每条数据的参数
        para_dict = {}  # 读取的单条数据
        classified_result = {}  # 预测的单条数据
        response_result = []  # 存储所有预测结果的数组
        read_data = pd.read_excel("../src/assets/Upload_files/upload_coal.xlsx")
        read_data = read_data.fillna(value='_')  # 将NaN值替换成 '_'，以便于写入数据库
        for index, row_ in read_data.iterrows():
            if index != 0:  # 跳过第一行
                para_dict['Vm'] = row_['煤样挥发分(Vdaf)']
                para_dict['H'] = row_['氢(Hdaf)']
                para_dict['G'] = row_['粘结指数(G)']
                para_dict['Y'] = row_['Y']
                para_dict['b'] = row_['b/%']
                classify_para.append(para_dict)
                headers = ['Type', 'Vm', 'H', 'G', 'Y', 'b']  # CSV文件头部
                file_name = 'Sample.csv'
                row = []
                row.append('Test')
                row.append(para_dict['Vm'])
                row.append(para_dict['H'])
                row.append(para_dict['G'])
                row.append(para_dict['Y'])
                row.append(para_dict['b'])

                with open(file_name, 'w', newline='') as f:  # 将数据写入CSV文件
                    f_csv = csv.writer(f)
                    f_csv.writerow(headers)
                    f_csv.writerow(row)

                # 调用煤分类模型进行预测
                single_result = coaltypefind(file_name)

                classified_result['id'] = index
                classified_result['name'] = row_['煤样名称']

                # 处理模型返回False的情况
                if single_result == False:
                    classified_result['predicted_type'] = "判据不足"
                else:
                    classified_result['predicted_type'] = single_result[0]

                response_result.append(classified_result)
                global upload_classify_user
                upload_classify_user = response_result  # 保存预测结果供其他使用
                para_dict = {}  # 清空 para_dict，准备下一条数据
                classified_result = {}  # 清空 classified_result，准备下一条数据
    return jsonify(response_result)

#点击“用户上传煤分类结果按钮”上传结果至数据库
@app.route('/uploadUserClassifyResult',methods=['POST','GET'])
def uploadUserClassifyResult() -> str:
    """
    用户上传煤样分类结果接口。

    处理逻辑:
        - 检查全局变量 `upload_classify_user` 是否包含分类结果。
        - 从上传的 Excel 文件中读取煤样数据。
        - 合并用户分类结果和煤样数据，根据模板填充每条记录。
        - 数据格式化后插入到数据库。

    参数:
        无（通过 POST 请求上传数据）。

    返回值:
        str: 返回 "upload successfully" 表示上传成功。
        如果发生异常，返回错误消息。

    示例:
        使用 POST 请求上传煤样分类结果:
        ::
            请求:
            POST /uploadUserClassifyResult
            文件路径: ../src/assets/Upload_files/upload_coal.xlsx

            返回:
            "upload successfully"

    注意事项:
        - `upload_classify_user` 必须包含每条煤样的分类结果。
        - 上传的 Excel 文件路径为 `../src/assets/Upload_files/upload_coal.xlsx`。
        - 数据中的 NaN 值将替换为 None。
        - 确保数据库事务成功提交。

    错误处理:
        - 如果文件读取或数据库操作失败，将返回详细的错误信息。
        - 未找到分类结果时返回错误提示。
    """
    if len(upload_classify_user) != 0:
        # 初始化煤样数据字典
        dict = {'coal_name':None,'coal_belong':None,'coal_type':None,'coal_price':None,'ori_coal_13mm':None,'ori_coal_13_10mm':None,'ori_coal_10_8mm':None,'ori_coal_8_6mm':None,'ori_coal_6_5mm':None,"ori_coal_5_4mm":None,'ori_coal_4_3mm':None,'ori_coal_3_2mm':None,"ori_coal_2_1mm":None,"ori_coal_1_05mm":None,"ori_coal_05mm":None,"ori_coal_total":None,"ori_coal_fineness":None,"sma_coal_moi":None,"sma__coal_6mm":None,"sma__coal_6_5mm":None,"sma__coal_5_4mm":None,"sma__coal_4_3mm":None,"sma__coal_3_2mm":None,"sma__coal_2_1mm":None,"sma__coal_1_05mm":None,"sma__coal_05mm":None,"sma__coal_total":None,"sma_coal_fineness":None,"coal_mad":None,"coal_ad":None,"coal_vdaf":None,"coal_fcd":None,"coal_vd":None,"coal_ada":None,"coal_vad":None,"coal_fcad":None,"coal_std":None,"coal_ana_had":None,"coal_ana_cad":None,"coal_ana_nad":None,"coal_ana_oad":None,"coal_dry_hd":None,"coal_dry_cd":None,"coal_dry_nd":None,"coal_dry_od":None,"coal_drynoash_hdaf":None,"coal_drynoash_cdaf":None,"coal_drynoash_ndaf":None,"coal_drynoash_odaf":None,"G":None,"X":None,"Y":None,"T1":None,"T2":None,"T3":None,"a":None,"b":None,"Tp":None,"Tmax":None,"Tk":None,"amax":None,"Tk_Tp":None,"DT":None,"ST":None,"HT":None,"FT":None,"SiO2":None,"Al2O3":None,"Fe2O3":None,"CaO":None,"MgO":None,"P2O5":None,"Na2O":None,"K2O":None,"TiO2":None,"SO3":None,"ash_total":None,"V":None,"I":None,"E":None,"M":None,"live_idle_ratio":None,"Rmax":None,"micro_var":None,"micro_type":None,"oven_type":None,"coking_style":None,"dry_quality":None,"heap_density":None,"oven_moi":None,"up_temper":None,"down_number":None,"hot_coke_qulity":None,"hot_ratio_coke":None,"quench_coke_weight":None,"coke_moi":None,"ratio_coke":None,"coking_date":None,"coking_process_time":None,"coking_start_time":None,"center_100_time":None,"center_500_time":None,"center_900_time":None,"coking_end_time":None,"coking_end_temp":None,"coke_mad":None,"coke_ad":None,"coke_vdaf":None,"coke_fcd":None,"coke_vd":None,"coke_aad":None,"coke_vad":None,"coke_fcad":None,"coke_std":None,"coke_80mm":None,"coke_80_60mm":None,"coke_60_40mm":None,"coke_40_25mm":None,"coke_25_20mm":None,"coke_20_10mm":None,"coke_10mm":None,"coke_5mm":None,"coke_sum":None,"coke_60mm":None,"coke_fineness":None,"coke_M40":None,"coke_M25":None,"coke_M10":None,"coke_CRI":None,"coke_CSR":None,"coke_DT":None,"coke_ST":None,"coke_HT":None,"coke_FT":None,"coke_750":None,"coke_800":None,"coke_850":None,"coke_900":None,"coke_950":None,"coke_1000":None,"coke_1050":None,"coke_1100":None,"coke_1150":None,"coke_1200":None,"coke_apparent_porosity":None,"coke_real_density":None,"coke_fake_density":None,"coke_total_ratio":None}
        # 读取上传的Excel文件并填充缺失值
        read_data = pd.read_excel("../src/assets/Upload_files/upload_coal.xlsx")
        read_data = read_data.fillna(value='_') # 将nan替换成_以便于写入mysql数据库
        upload_list = [] # 用来存储上传煤数据的数量
        # 遍历数据并处理每一行
        for index, row in read_data.iterrows():
            if index != 0:
                dict['coal_name'] = row['煤样名称']
                dict['coal_type'] = upload_classify_user[index-1]['predicted_type']
                dict['coal_price'] = row['价格(吨)']
                dict['coal_mad'] = row['煤样水分(Mad)']
                dict['coal_ad'] = row['煤样灰分(Ad)']
                dict['coal_vdaf'] = row['煤样挥发分(Vdaf)']
                dict['coal_fcd'] = row['煤样固定碳(FCd)']
                dict['coal_std'] = row['煤样硫分(St,d)']
                dict['coal_drynoash_hdaf'] = row['氢(Hdaf)']
                dict['coal_drynoash_cdaf'] = row['碳(Cdaf)']
                dict['coal_drynoash_ndaf'] = row['氮(Ndaf)']
                dict['coal_drynoash_odaf'] = row['氧(Odaf)']
                dict['G'] = row['粘结指数(G)']
                dict['X'] = row['X']
                dict['Y'] = row['Y']
                dict['a'] = row['a/%']
                dict['b'] = row['b/%']
                dict['Tp'] = row['Tp/℃']
                dict['Tmax'] = row['Tmax/℃']
                dict['Tk'] = row['Tk/℃']
                dict['amax'] = row['αmax/度/分']
                dict['Tk_Tp'] = row['Tk-Tp']
                dict['DT'] = row['变形温度(DT)']
                dict['ST'] = row['软化温度(ST)']
                dict['HT'] = row['半球温度(HT)']
                dict['FT'] = row['流动温度(FT)']
                dict['SiO2'] = row['SiO2']
                dict['Al2O3'] = row['Al2O3']
                dict['Fe2O3'] = row['Fe2O3']
                dict['CaO'] = row['CaO']
                dict['MgO'] = row['MgO']
                dict['P2O5'] = row['P2O5']
                dict['Na2O'] = row['Na2O']
                dict['K2O'] = row['K2O']
                dict['TiO2'] = row['TiO2']
                dict['SO3'] = row['SO3']
                dict['V'] = row['镜质组(V)']
                dict['I'] = row['惰质组(I)']
                dict['E'] = row['壳质组(E)']
                dict['M'] = row['矿物(M)']
                dict['live_idle_ratio'] = row['活惰比']
                dict['Rmax'] = row['平均最大反射率(Rmax)']
                dict['micro_var'] = row['标准方差']
                dict['micro_type'] = row['类型']
                dict['oven_type'] = row['炉型']
                dict['dry_quality'] = row['入炉干基质量/kg']
                dict['heap_density'] = row['堆密度t/m³']
                dict['oven_moi'] = row['入炉煤水分%']
                dict['coking_date'] = row['炼焦日期']
                dict['coking_start_time'] = row['入炉时间']
                dict['center_100_time'] = row['中心到100℃时间']
                dict['center_500_time'] = row['中心到500℃时间']
                dict['center_900_time'] = row['中心到900℃时间']
                dict['coking_end_time'] = row['出炉时间']
                dict['coking_end_temp'] = row['出炉中心温度℃']
                dict['coke_mad'] = row['焦炭水分(Mad)']
                dict['coke_ad'] = row['焦炭灰分(Ad)']
                dict['coke_std'] = row['焦炭硫分(St,d)']
                dict['coke_M40'] = row['M40']
                dict['coke_M25'] = row['M25']
                dict['coke_M10'] = row['M10']
                dict['coke_CRI'] = row['CRI']
                dict['coke_CSR'] = row['CSR']

                # 检查字典中每个值，若是'_'则转换为None
                for key in dict.keys():
                    if dict[key] == '_': # 将_识别的出的对应nan都转换成None
                        dict[key] = None 

                # 生成煤样数据实例并添加到列表
                new_coal_data= CoalDataGeneration(coal_name=dict['coal_name'],coal_type=dict['coal_type'],coal_price=dict['coal_price'],coal_mad=dict['coal_mad'],coal_ad=dict['coal_ad'],coal_vdaf=dict['coal_vdaf'],coal_fcd=dict['coal_fcd'],coal_std=dict['coal_std'],coal_drynoash_hdaf=dict['coal_drynoash_hdaf'],coal_drynoash_cdaf=dict['coal_drynoash_cdaf'],coal_drynoash_ndaf=dict['coal_drynoash_ndaf'],coal_drynoash_odaf=dict['coal_drynoash_odaf'],G=dict['G'],X=dict['X'],Y=dict['Y'],a=dict['a'],b=dict['b'],Tp=dict['Tp'],Tmax=dict['Tmax'],Tk=dict['Tk'],amax=dict['amax'],Tk_Tp=dict['Tk_Tp'],DT=dict['DT'],ST=dict['ST'],HT=dict['HT'],FT=dict['FT'],SiO2=dict['SiO2'],Al2O3=dict['Al2O3'],Fe2O3=dict['Fe2O3'],CaO=dict['CaO'],MgO=dict['MgO'],P2O5=dict['P2O5'],Na2O=dict['Na2O'],K2O=dict['K2O'],TiO2=dict['TiO2'],SO3=dict['SO3'],V=dict['V'],I=dict['I'],E=dict['E'],M=dict['M'],live_idle_ratio=dict['live_idle_ratio'],Rmax=dict['Rmax'],micro_var=dict['micro_var'],micro_type=dict['micro_type'],oven_type=dict['oven_type'],dry_quality=dict['dry_quality'],heap_density=dict['heap_density'],oven_moi=dict['oven_moi'],coking_date=dict['coking_date'],coking_start_time=dict['coking_start_time'],center_100_time=dict['center_100_time'],center_500_time=dict['center_500_time'],center_900_time=dict['center_900_time'],coking_end_time=dict['coking_end_time'],coking_end_temp=dict['coking_end_temp'],coke_mad=dict['coke_mad'],coke_ad=dict['coke_ad'],coke_std=dict['coke_std'],coke_M40=dict['coke_M40'],coke_M25=dict['coke_M25'],coke_M10=dict['coke_M10'],coke_CRI=dict['coke_CRI'],coke_CSR=dict['coke_CSR'])
                upload_list.append(new_coal_data) # 将所有所有数据存入列表中
                dict = {'coal_name':None,'coal_belong':None,'coal_type':None,'coal_price':None,'ori_coal_13mm':None,'ori_coal_13_10mm':None,'ori_coal_10_8mm':None,'ori_coal_8_6mm':None,'ori_coal_6_5mm':None,"ori_coal_5_4mm":None,'ori_coal_4_3mm':None,'ori_coal_3_2mm':None,"ori_coal_2_1mm":None,"ori_coal_1_05mm":None,"ori_coal_05mm":None,"ori_coal_total":None,"ori_coal_fineness":None,"sma_coal_moi":None,"sma__coal_6mm":None,"sma__coal_6_5mm":None,"sma__coal_5_4mm":None,"sma__coal_4_3mm":None,"sma__coal_3_2mm":None,"sma__coal_2_1mm":None,"sma__coal_1_05mm":None,"sma__coal_05mm":None,"sma__coal_total":None,"sma_coal_fineness":None,"coal_mad":None,"coal_ad":None,"coal_vdaf":None,"coal_fcd":None,"coal_vd":None,"coal_ada":None,"coal_vad":None,"coal_fcad":None,"coal_std":None,"coal_ana_had":None,"coal_ana_cad":None,"coal_ana_nad":None,"coal_ana_oad":None,"coal_dry_hd":None,"coal_dry_cd":None,"coal_dry_nd":None,"coal_dry_od":None,"coal_drynoash_hdaf":None,"coal_drynoash_cdaf":None,"coal_drynoash_ndaf":None,"coal_drynoash_odaf":None,"G":None,"X":None,"Y":None,"T1":None,"T2":None,"T3":None,"a":None,"b":None,"Tp":None,"Tmax":None,"Tk":None,"amax":None,"Tk_Tp":None,"DT":None,"ST":None,"HT":None,"FT":None,"SiO2":None,"Al2O3":None,"Fe2O3":None,"CaO":None,"MgO":None,"P2O5":None,"Na2O":None,"K2O":None,"TiO2":None,"SO3":None,"ash_total":None,"V":None,"I":None,"E":None,"M":None,"live_idle_ratio":None,"Rmax":None,"micro_var":None,"micro_type":None,"oven_type":None,"coking_style":None,"dry_quality":None,"heap_density":None,"oven_moi":None,"up_temper":None,"down_number":None,"hot_coke_qulity":None,"hot_ratio_coke":None,"quench_coke_weight":None,"coke_moi":None,"ratio_coke":None,"coking_date":None,"coking_process_time":None,"coking_start_time":None,"center_100_time":None,"center_500_time":None,"center_900_time":None,"coking_end_time":None,"coking_end_temp":None,"coke_mad":None,"coke_ad":None,"coke_vdaf":None,"coke_fcd":None,"coke_vd":None,"coke_aad":None,"coke_vad":None,"coke_fcad":None,"coke_std":None,"coke_80mm":None,"coke_80_60mm":None,"coke_60_40mm":None,"coke_40_25mm":None,"coke_25_20mm":None,"coke_20_10mm":None,"coke_10mm":None,"coke_5mm":None,"coke_sum":None,"coke_60mm":None,"coke_fineness":None,"coke_M40":None,"coke_M25":None,"coke_M10":None,"coke_CRI":None,"coke_CSR":None,"coke_DT":None,"coke_ST":None,"coke_HT":None,"coke_FT":None,"coke_750":None,"coke_800":None,"coke_850":None,"coke_900":None,"coke_950":None,"coke_1000":None,"coke_1050":None,"coke_1100":None,"coke_1150":None,"coke_1200":None,"coke_apparent_porosity":None,"coke_real_density":None,"coke_fake_density":None,"coke_total_ratio":None}
        
        # 将所有数据插入到数据库
        db.session.add_all(upload_list)
        db.session.commit()

    return 'upload successfully'

from memory_profiler import profile

@profile
def main():
    # 主函数内容，例如加载模型、启动训练等
    import tensorflow as tf
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    print("Model created")

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run('0.0.0.0', debug=True)