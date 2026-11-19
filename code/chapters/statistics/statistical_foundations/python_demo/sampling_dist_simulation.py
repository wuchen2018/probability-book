"""
文件名: sampling_dist_simulation.py
功能: 通过蒙特卡洛模拟，从标准正态分布“合成”出三大抽样分布（Chi2, t, F）

【这是什么？】
统计学教科书上那些复杂的概率密度函数（PDF）公式，往往让人觉得是天书。
但本质上，它们都是由简单的“标准正态分布”变出来的。
这段代码就像一个“数字炼金术”实验室：它不使用现成的生成函数，而是从零开始，
只用“加减乘除”和“正态随机数”，就能通过暴力模拟重现出教科书上的三大完美曲线。

【怎么用？】
直接运行即可。
程序会生成三个图表，分别展示：
1. 多个正态变量平方和 -> 变成卡方分布
2. 正态变量除以卡方变量 -> 变成 t 分布
3. 两个卡方变量相比 -> 变成 F 分布
你可以修改下方的参数（如自由度），看看曲线形状会发生什么神奇的变化。
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# --- 可调整参数配置区 ---
N_SIMULATIONS = 100000  # 模拟次数（炼金术的原料数量，越多越平滑，建议 10000 以上）

# 1. 卡方分布的自由度配置
DF_CHI2 = 5             # 尝试修改这个数字（如 2, 10, 30），观察分布是否趋向正态

# 2. t 分布的自由度配置
DF_T = 3                # 自由度越小，尾巴越厚（极端值越多）；自由度很大时，应接近正态分布

# 3. F 分布的自由度配置
DF_F_NUM = 10           # 分子自由度
DF_F_DEN = 20           # 分母自由度

# 绘图设置
BINS = 100              # 直方图的柱子数量
COLOR_HIST = '#A0CBE8'  # 直方图颜色（模拟数据）
COLOR_LINE = '#FF9D9A'  # 理论曲线颜色（数学公式）

# -----------------------

def run_simulation():
    print(f"正在进行 {N_SIMULATIONS} 次蒙特卡洛模拟，请稍候...")
    
    plt.figure(figsize=(15, 10))
    plt.subplots_adjust(hspace=0.4)

    # ==========================================
    # 实验 1：从正态分布合成 Chi-square 分布
    # 数学原理：Chi2(k) = Z_1^2 + Z_2^2 + ... + Z_k^2
    # ==========================================
    ax1 = plt.subplot(3, 1, 1)
    
    # 1. 生成原料：生成 DF_CHI2 组标准正态随机数，每组有 N_SIMULATIONS 个
    # 对应数学：Z_1, Z_2, ... Z_k ~ N(0, 1)
    z_matrix = np.random.standard_normal((DF_CHI2, N_SIMULATIONS))
    
    # 2. 合成过程：先平方，再求和
    # 对应数学：Q = Σ(Z_i^2)
    simulated_chi2 = np.sum(z_matrix**2, axis=0)
    
    # 3. 绘制结果
    # 绘制模拟数据的直方图（代表现实中的抽样结果）
    ax1.hist(simulated_chi2, bins=BINS, density=True, color=COLOR_HIST, label='模拟数据 (Monte Carlo)', alpha=0.8)
    
    # 绘制理论曲线（代表上帝视角的数学真理）
    x = np.linspace(0, np.max(simulated_chi2), 500)
    y = stats.chi2.pdf(x, DF_CHI2)
    ax1.plot(x, y, color=COLOR_LINE, linewidth=3, label=f'理论曲线 $\chi^2({DF_CHI2})$')
    
    ax1.set_title(f'实验1: {DF_CHI2} 个标准正态变量的“平方和” = 卡方分布', fontsize=12)
    ax1.legend()

    # ==========================================
    # 实验 2：从正态分布和卡方分布合成 t 分布
    # 数学原理：T = Z / sqrt(V / k)，其中 V ~ Chi2(k)
    # ==========================================
    ax2 = plt.subplot(3, 1, 2)
    
    # 1. 生成原料：
    # 一个标准正态变量 (分子)
    z_numerator = np.random.standard_normal(N_SIMULATIONS)
    # 一组独立的卡方变量 (分母所需的原料)，利用刚才的逻辑生成
    # 注意：这里需要重新生成，确保分子分母独立
    chi2_denominator = np.sum(np.random.standard_normal((DF_T, N_SIMULATIONS))**2, axis=0)
    
    # 2. 合成过程：严格按照 t 分布定义公式计算
    # 对应数学：T = Z / sqrt(Chi2 / df)
    simulated_t = z_numerator / np.sqrt(chi2_denominator / DF_T)
    
    # 3. 绘制结果
    # 为了看清细节，限制一下 X 轴范围（t分布容易产生极端大值）
    limit = 6
    simulated_t_clipped = simulated_t[(simulated_t > -limit) & (simulated_t < limit)]
    
    ax2.hist(simulated_t_clipped, bins=BINS, density=True, color=COLOR_HIST, label='模拟数据', alpha=0.8)
    
    x = np.linspace(-limit, limit, 500)
    y = stats.t.pdf(x, DF_T)
    ax2.plot(x, y, color=COLOR_LINE, linewidth=3, label=f'理论曲线 $t({DF_T})$')
    
    # 对比标准正态分布（虚线），展示“胖尾”特征
    y_norm = stats.norm.pdf(x, 0, 1)
    ax2.plot(x, y_norm, 'k--', linewidth=1, alpha=0.5, label='标准正态分布 (对比)')
    
    ax2.set_title(f'实验2: t 分布 (注意对比虚线的“胖尾”)', fontsize=12)
    ax2.legend()

    # ==========================================
    # 实验 3：从两个卡方分布合成 F 分布
    # 数学原理：F = (U/d1) / (V/d2)
    # ==========================================
    ax3 = plt.subplot(3, 1, 3)
    
    # 1. 生成原料：两个独立的卡方变量
    chi2_num = np.sum(np.random.standard_normal((DF_F_NUM, N_SIMULATIONS))**2, axis=0)
    chi2_den = np.sum(np.random.standard_normal((DF_F_DEN, N_SIMULATIONS))**2, axis=0)
    
    # 2. 合成过程：计算方差比率
    # 对应数学：F = (Chi2_1 / df1) / (Chi2_2 / df2)
    simulated_f = (chi2_num / DF_F_NUM) / (chi2_den / DF_F_DEN)
    
    # 3. 绘制结果
    f_limit = 5 # 限制显示范围
    simulated_f_clipped = simulated_f[simulated_f < f_limit]
    
    ax3.hist(simulated_f_clipped, bins=BINS, density=True, color=COLOR_HIST, label='模拟数据', alpha=0.8)
    
    x = np.linspace(0, f_limit, 500)
    y = stats.f.pdf(x, DF_F_NUM, DF_F_DEN)
    ax3.plot(x, y, color=COLOR_LINE, linewidth=3, label=f'理论曲线 $F({DF_F_NUM}, {DF_F_DEN})$')
    
    ax3.set_title(f'实验3: 两个卡方分布之比 = F 分布', fontsize=12)
    ax3.legend()

    plt.show()

if __name__ == "__main__":
    run_simulation()