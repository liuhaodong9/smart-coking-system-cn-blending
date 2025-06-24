import numpy as np
import geatpy as ea

class MyProblem(ea.Problem):
    """
    MyProblem 类定义了一个煤炭配比优化问题。
    优化目标是根据价格和煤炭特性 (CRI, CSR, M10, M25) 在满足约束条件的前提下，找到最优解。
    """
    def __init__(self, inputDim, lb, ub, lbin, ubin, price, CRI_range, CSR_range, 
                 M10_range, M25_range, CRI_min, CRI_max, CSR_min, CSR_max, 
                 M10_min, M10_max, M25_min, M25_max):
        """
        初始化 MyProblem 对象，设置决策变量维度、上下界、约束和优化目标。

        参数：
        ----------
        inputDim : int
            决策变量的维度（煤炭种类数）。
        lb : list of float
            决策变量的下界。
        ub : list of float
            决策变量的上界。
        lbin : list of int
            下界包含标志（1 表示包含，0 表示不包含）。
        ubin : list of int
            上界包含标志（1 表示包含，0 表示不包含）。
        price : list of float
            各变量对应的价格，用于目标函数。
        CRI_range : list of float
            各变量的 CRI 值，用于计算混合煤炭的 CRI。
        CSR_range : list of float
            各变量的 CSR 值，用于计算混合煤炭的 CSR。
        M10_range : list of float
            各变量的 M10 值，用于计算混合煤炭的 M10。
        M25_range : list of float
            各变量的 M25 值，用于计算混合煤炭的 M25。
        CRI_min, CRI_max : float
            混合煤炭的 CRI 的最小和最大允许值。
        CSR_min, CSR_max : float
            混合煤炭的 CSR 的最小和最大允许值。
        M10_min, M10_max : float
            混合煤炭的 M10 的最小和最大允许值。
        M25_min, M25_max : float
            混合煤炭的 M25 的最小和最大允许值。
        """
        name = 'MyProblem'  # 问题名称
        M = 1  # 目标维度（单目标优化）
        maxormins = [1]  # 优化方向，1 表示最小化
        self.Dim = inputDim  # 决策变量维度
        varTypes = [0] * self.Dim  # 决策变量类型（0 表示连续变量）

        # 初始化父类 ea.Problem
        ea.Problem.__init__(self, name, M, maxormins, self.Dim, varTypes, lb, ub, lbin, ubin)

        # 初始化特性值和约束参数
        self.price = price
        self.CRI_range = CRI_range
        self.CSR_range = CSR_range
        self.M10_range = M10_range
        self.M25_range = M25_range

        self.CRI_min = CRI_min
        self.CRI_max = CRI_max
        self.CSR_min = CSR_min
        self.CSR_max = CSR_max
        self.M10_min = M10_min
        self.M10_max = M10_max
        self.M25_min = M25_min
        self.M25_max = M25_max

    def aimFunc(self, pop):
        """
        计算种群的目标函数值和约束条件。

        参数：
        ----------
        pop : Population
            包含多个个体的种群对象，每个个体表示一个煤炭配比方案。
        
        更新：
        ----------
        - `pop.ObjV`：更新为每个个体的目标值（即配比的总成本）。
        - `pop.CV`：更新为每个个体的约束值（违反约束的程度）。
        """
        Vars = pop.Phen  # 提取种群的决策变量
        var_array = [Vars[:, [i]] for i in range(self.Dim)]  # 将每一列变量提取为单独数组

        # 目标函数：配比成本的加权和
        pop.ObjV = sum(self.price[i] * var_array[i] for i in range(len(self.price)))

        # 约束条件
        # 1. 配比比例的总和必须为 1
        proportion_formula_1 = np.abs(sum(var_array) - 1)

        # 2. CRI 值范围约束
        proportion_formula_2 = sum(var_array[i] * self.CRI_range[i] for i in range(len(var_array))) - self.CRI_min
        proportion_formula_2 = -proportion_formula_2
        proportion_formula_3 = proportion_formula_2 - self.CRI_max

        # 3. CSR 值范围约束
        proportion_formula_4 = sum(var_array[i] * self.CSR_range[i] for i in range(len(var_array))) - self.CSR_min
        proportion_formula_4 = -proportion_formula_4
        proportion_formula_5 = proportion_formula_4 - self.CSR_max

        # 4. M10 值范围约束
        proportion_formula_6 = sum(var_array[i] * self.M10_range[i] for i in range(len(var_array))) - self.M10_min
        proportion_formula_6 = -proportion_formula_6
        proportion_formula_7 = proportion_formula_6 - self.M10_max

        # 5. M25 值范围约束
        proportion_formula_8 = sum(var_array[i] * self.M25_range[i] for i in range(len(var_array))) - self.M25_min
        proportion_formula_8 = -proportion_formula_8
        proportion_formula_9 = proportion_formula_8 - self.M25_max

        # 将所有约束组合
        pop.CV = np.hstack([
            proportion_formula_1, proportion_formula_2, proportion_formula_3,
            proportion_formula_4, proportion_formula_5, proportion_formula_6,
            proportion_formula_7, proportion_formula_8, proportion_formula_9
        ])
