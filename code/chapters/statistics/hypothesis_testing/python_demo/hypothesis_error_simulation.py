"""
文件名: hypothesis_error_simulation.py
功能: 模拟假设检验中的第一类错误（弃真）与第二类错误（取伪）

【这是什么？】
在现实世界中，当我们做一个统计决策（比如“拒绝原假设”）时，我们永远不知道自己是不是真的犯了错，因为上帝视角的“真值”是不可知的。
但在这个代码实验室里，我们拥有上帝视角。我们可以设定“原假设为真”或“原假设为假”的客观事实，然后进行成千上万次模拟抽样，
亲眼看看在不同的样本量（n）和显著性水平（alpha）下，我们的检验策略到底有多大概率会“冤枉好人”（第一类错误）或“放过坏人”（第二类错误）。

【怎么用？】
1. 直接运行代码，你会看到控制台输出模拟的错误率，并弹出一张包含两个正态分布的图示。
2. 尝试修改【可调整参数配置区】中的 `SAMPLE_SIZE`（样本量），观察当样本量变大时，图中的重叠区域（错误概率）是如何缩小的。
3. 尝试修改 `ALPHA`（显著性水平），观察它是如何像跷跷板一样，按下一头的错误率，翘起另一头的。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 可调整参数配置区 ---
# 1. 实验设定
MU_H0 = 100        # 原假设认为的均值 (H0: mu = 100)
SIGMA = 10         # 总体的标准差 (假设已知)

# 2. 上帝视角的真实设定 (用于制造第二类错误)
MU_TRUE = 98       # 现实中的真实均值 (H1: mu != 100, 实际上确实有偏差)

# 3. 检验策略设定
SAMPLE_SIZE = 30   # 样本量 (n)：抽取多少个样本来算均值
ALPHA = 0.05       # 显著性水平 (alpha)：我们要控制的第一类错误率上限

# 4. 模拟规模
N_SIMULATIONS = 10000 # 模拟实验的次数 (次数越多，结果越接近理论值)

# ---------------------------------------------------------

def simulate_hypothesis_test():
    # 1. 计算标准误 (Standard Error)
    # 根据中心极限定理，样本均值的标准差 = 总体标准差 / sqrt(n)
    se = SIGMA / np.sqrt(SAMPLE_SIZE)
    
    # 2. 确定拒绝域的临界值 (Critical Values)
    # 在双侧检验中，我们在 H0 分布的两端各切掉 alpha/2 的面积
    # norm.ppf 是累积概率函数的反函数，用于找横坐标
    z_critical = norm.ppf(1 - ALPHA / 2) 
    
    # 计算具体的均值临界线： mu_0 +/- z * se
    critical_high = MU_H0 + z_critical * se
    critical_low  = MU_H0 - z_critical * se

    print(f"--- 理论计算参数 ---")
    print(f"原假设均值: {MU_H0}, 真实均值: {MU_TRUE}")
    print(f"样本量: {SAMPLE_SIZE}, 标准误: {se:.2f}")
    print(f"拒绝域临界值: < {critical_low:.2f} 或 > {critical_high:.2f}")
    print(f"-" * 30)

    # --- 场景 A：模拟原假设为真 (H0 is True) ---
    # 现实：mu = 100 (MU_H0)
    # 目的：看我们会误判拒绝多少次 (第一类错误)
    
    # 生成 N_SIMULATIONS 组样本均值，服从 N(MU_H0, se)
    sample_means_h0_true = np.random.normal(MU_H0, se, N_SIMULATIONS)
    
    # 判断：有多少样本均值落在了拒绝域里？
    reject_h0_count = np.sum(
        (sample_means_h0_true > critical_high) | 
        (sample_means_h0_true < critical_low)
    )
    type1_error_rate = reject_h0_count / N_SIMULATIONS
    
    # --- 场景 B：模拟原假设为假 (H1 is True) ---
    # 现实：mu = 98 (MU_TRUE)
    # 目的：看我们会误判接受多少次 (第二类错误)
    
    # 生成 N_SIMULATIONS 组样本均值，服从 N(MU_TRUE, se)
    # 注意：这里的数据生成中心是 MU_TRUE，因为这是客观事实
    sample_means_h1_true = np.random.normal(MU_TRUE, se, N_SIMULATIONS)
    
    # 判断：有多少样本均值落在了接受域里？(即没有被拒绝)
    # 接受域：critical_low < x < critical_high
    accept_h0_count = np.sum(
        (sample_means_h1_true <= critical_high) & 
        (sample_means_h1_true >= critical_low)
    )
    type2_error_rate = accept_h0_count / N_SIMULATIONS

    # --- 输出结果 ---
    print(f"【模拟结果】")
    print(f"1. 当原假设为真时 (H0 True):")
    print(f"   我们在 {N_SIMULATIONS} 次实验中，错误地拒绝了 {reject_h0_count} 次。")
    print(f"   模拟的第一类错误率 (Type I Error) = {type1_error_rate:.4f} (理论值应接近 {ALPHA})")
    
    print(f"\n2. 当原假设为假时 (H1 True, Truth={MU_TRUE}):")
    print(f"   我们在 {N_SIMULATIONS} 次实验中，错误地接受了 {accept_h0_count} 次。")
    print(f"   模拟的第二类错误率 (Type II Error/Beta) = {type2_error_rate:.4f}")
    print(f"   检验功效 (Power = 1 - Beta) = {1 - type2_error_rate:.4f}")

    # --- 可视化绘图 ---
    plot_distributions(se, critical_low, critical_high)

def plot_distributions(se, low, high):
    """绘制 H0 和 H1 的分布对比图"""
    plt.figure(figsize=(10, 6))
    
    # 生成用于绘图的 x 轴坐标
    x = np.linspace(min(MU_H0, MU_TRUE) - 4*se, max(MU_H0, MU_TRUE) + 4*se, 1000)
    
    # 1. 绘制 H0 分布 (原假设)
    y_h0 = norm.pdf(x, MU_H0, se)
    plt.plot(x, y_h0, label=f'H0 Distribution (Mean={MU_H0})', color='black', linestyle='--')
    
    # 2. 绘制 H1 分布 (真实情况)
    y_h1 = norm.pdf(x, MU_TRUE, se)
    plt.plot(x, y_h1, label=f'True Distribution (Mean={MU_TRUE})', color='#1f77b4', linewidth=2)
    
    # 3. 标记临界线
    plt.axvline(low, color='red', linestyle=':', label='Critical Values')
    plt.axvline(high, color='red', linestyle=':')
    
    # 4. 填充第二类错误区域 (Beta)
    # 即：H1 分布中，落在 H0 接受域内的部分
    x_beta = np.linspace(low, high, 500)
    y_beta = norm.pdf(x_beta, MU_TRUE, se)
    plt.fill_between(x_beta, y_beta, color='#1f77b4', alpha=0.3, label='Type II Error (Beta)')
    
    plt.title(f'Visualizing Type I & II Errors (n={SAMPLE_SIZE}, alpha={ALPHA})')
    plt.xlabel('Sample Mean')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    simulate_hypothesis_test()