
import pandas as pd
import sklearn
import pandas as pd
import sklearn
import warnings

# Ignore divide by zero warnings
warnings.filterwarnings("ignore", message="divide by zero encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero encountered")
warnings.filterwarnings("ignore", message="invalid value encountered")

def dataRebuild(data: pd.DataFrame, k: float, c: float, r: float, i: int, aim: str) -> pd.DataFrame:
    """
    基于线性拟合结果通过去除异常值重建数据。

    参数：
        data (pd.DataFrame): 输入的DataFrame，包含两个变量的列。
        k (float): 拟合直线的斜率。
        c (float): 拟合直线的截距。
        r (float): 半范围值，用于确定异常值的阈值。
        i (int): x 变量的列索引。
        aim (str): 目标变量的列名（y 变量）。

    返回值：
        pd.DataFrame: 修改后的DataFrame，标记了待删除的异常行。

    示例：
        >>> import pandas as pd
        >>> data = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [2, 4, 10, 8]})
        >>> k, c, r = 2.0, 0, 1.0
        >>> cleaned_data = dataRebuild(data, k, c, r, 0, 'y')
        >>> print(cleaned_data)
        # 输出含有标记为 'Delist' 的异常行
    """
    # 提取 x 和 y 的实际值
    x_value = data.iloc[:, i].values
    y_true = data.loc[:, aim].values
    
    # 遍历每个数据点，计算其是否为异常值
    for idx in range(x_value.size):
        # 计算拟合的上下边界
        y_high = k * x_value[idx] + c + r
        y_low = y_high - 2 * r  # 异常值的下限
        
        # 如果实际值超出该范围，标记该行待删除
        if y_true[idx] < y_low or y_true[idx] > y_high:
            data = data.rename(index={idx: 'Delist'})
    
    return data


def dataclean(data: pd.DataFrame, aim: str, round: int = 100, fit: float = 0.7, size: float = 0.9, printresult: bool = False) -> pd.DataFrame:
    """
    清洗数据，移除不在正常范围内的异常值。
    
    参数：
        data (pd.DataFrame): 输入的DataFrame，包含待清洗的数据。
        aim (str): 目标变量的列名，用作参考进行数据清洗。
        round (int, optional): 拟合的迭代次数，默认值为100。
        fit (float, optional): 用于线性拟合的比例，默认值为0.7。
        size (float, optional): 用于确定有效范围的面积大小，默认值为0.9。
        printresult (bool, optional): 是否打印拟合结果，默认值为False。

    返回值：
        pd.DataFrame: 清洗后的DataFrame，行已被随机打乱。
    
    示例：
        >>> import pandas as pd
        >>> data = pd.DataFrame({'x1': [1, 2, 3, 4], 'y': [2, 4, 6, 8], 'x2': [1, 3, 5, 7]})
        >>> cleaned_data = dataclean(data, 'y', round=50, fit=0.8, size=1.0, printresult=True)
        >>> print(cleaned_data)
    """
    # 遍历数据中的每一列（除去目标列）
    for i in range(1, data.shape[1] - 2):  # data.shape[1] - 2 是根据数据的输出调整的范围
        # 选择包含 x 和 y 变量的处理数据
        process_data = pd.concat([data.iloc[:, i], data.loc[:, aim]], axis=1)
        process_data = process_data.dropna(axis=0, how='any')  # 删除包含NaN值的行
        
        label = process_data.columns.values.tolist()  # 获取列标签
        x_label = label[0]  # x 变量标签
        y_label = label[1]  # y 变量标签
        
        # 使用模型拟合并找到数据的范围
        k, c, r = ModelFit.rangefinder(
            process_data,
            ratio=fit, area=size, n=round,
            printstatus=printresult
        )
        
        # 如果需要，打印拟合结果
        if printresult is True:
            ModelFit.rangeprint(process_data, x_label, y_label, k, c, r)
        
        # 通过移除离群值重建数据
        data = dataRebuild(data, k, c, r, i, aim)

    # 删除标记为 'Delist' 的行
    data = data.drop(index='Delist', axis=0)
    # 随机打乱数据的行
    data = sklearn.utils.shuffle(data)

    return data

