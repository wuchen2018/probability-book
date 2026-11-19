"""
文件名: cf_clt_convergence.py
功能: 可视化特征函数的收敛过程（验证中心极限定理）

【这是什么？】
中心极限定理告诉我们，无论原始分布长什么样，标准化后的和都会趋向正态分布。
本代码从“上帝视角”（特征函数层面）验证这一点：
它展示了随着样本量 n 的增加，原始分布的特征函数是如何一步步“变形”，
最终与标准正态分布的特征函数 (e^-t^2/2) 完美重合的。

【怎么用？】
直接运行即可。
你将看到一张动态图（或对比图），蓝线是计算出来的特征函数，红虚线是目标（正态分布）。
你可以修改 n_list 来观察不同样本量下的逼近程度。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 可调整参数配置区 ---
# 想要观察的样本量列表。建议从小的 n 开始，看它如何进化
N_LIST = [1, 2, 5, 10, 30]

# 特征函数自变量 t 的范围 (查看 [-range, +range] 区间)
T_RANGE = 5.0

# 绘图分辨率
POINTS = 1000

# 字体配置（防止中文乱码，若运行报错可注释掉中文字体设置）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False 

# --------------------------------------------------------

def get_exponential_cf_standardized(t, n):
    """
    计算指数分布(Exp(1))标准化和 Z_n 的特征函数值。
    
    数学推导：
    1. 设 X ~ Exp(1)，其特征函数为 phi_X(t) = 1 / (1 - it)
    2. 标准化和 Z_n = (Sum(X) - n) / sqrt(n)
    3. 根据线性变换性质，Z_n 的特征函数为：
       phi_Zn(t) = e^(-it*sqrt(n)) * [phi_X(t/sqrt(n))]^n
    """
    sqrt_n = np.sqrt(n)
    
    # 原始分布(指数分布)在缩放后的点 t/sqrt(n) 处的特征函数
    # 对应数学公式：phi_X(t/sqrt(n))
    phi_x_scaled = 1.0 / (1.0 - 1j * (t / sqrt_n))
    
    # 根据独立性，n个变量相加对应特征函数相乘（n次方）
    # 对应数学公式：[phi_X(...)]^n
    phi_sum = phi_x_scaled ** n
    
    # 平移项（减去均值 n 带来的相位旋转）
    # 对应数学公式：乘以 e^(-it*sqrt(n))
    shift_term = np.exp(-1j * t * sqrt_n)
    
    return shift_term * phi_sum

def target_normal_cf(t):
    """
    标准正态分布 N(0,1) 的特征函数。
    数学公式：e^(-t^2 / 2)
    这是我们要逼近的“终极目标”。
    """
    return np.exp(-0.5 * t**2)

def main():
    # 生成 t 的坐标轴
    t_values = np.linspace(-T_RANGE, T_RANGE, POINTS)
    
    # 计算目标（标准正态）的特征函数曲线
    # 注意：标准正态的特征函数是实数，但为了统一格式我们取实部
    target_y = target_normal_cf(t_values)

    plt.figure(figsize=(10, 6))
    
    # 绘制目标基准线
    plt.plot(t_values, target_y, 'r--', linewidth=3, label='目标：标准正态分布 $e^{-t^2/2}$')

    # 遍历不同的 n，看看特征函数长什么样
    colors = plt.cm.viridis(np.linspace(0, 1, len(N_LIST)))
    
    for i, n in enumerate(N_LIST):
        # 计算当前 n 下的特征函数
        cf_values = get_exponential_cf_standardized(t_values, n)
        
        # 我们只画“实部”。
        # 原因：特征函数包含分布的所有信息。对于对称的极限分布（正态），
        # 虚部最终会趋近于0。观察实部的收敛最直观。
        plt.plot(t_values, cf_values.real, color=colors[i], linewidth=1.5, 
                 label=f'当前样本量 n={n}')

    plt.title('特征函数的进化：从指数分布到正态分布', fontsize=14)
    plt.xlabel('t (频率域)', fontsize=12)
    plt.ylabel('特征函数的值 (实部)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print(f"绘图完成。请观察：当 n 增大时，曲线是否越来越像红色的虚线？")
    plt.show()

if __name__ == "__main__":
    main()