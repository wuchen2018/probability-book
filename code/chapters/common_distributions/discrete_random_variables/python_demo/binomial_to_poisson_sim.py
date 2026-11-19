# -*- coding: utf-8 -*-
"""
文件名: binomial_to_poisson_sim.py
功能: 模拟“二项分布趋向于泊松分布”的收敛过程

【这是什么？】
泊松分布在数学上被定义为二项分布的极限形式（当试验次数 n 趋向无穷大，成功概率 p 趋向于 0，且 np = λ 固定时）。
这段代码通过可视化的方式，让你直观地看到：随着我们将时间（或空间）切分得越来越细（n 增大），
二项分布的概率柱状图是如何一步步“变形”，最终完美贴合到泊松分布的理论曲线上的。

【怎么用？】
直接运行本脚本。
你会看到一张包含三个子图的对比图，分别展示了在 n=10, n=50, n=1000 时，
二项分布（蓝色柱子）与理论上的泊松分布（红色曲线）的重合程度。
你可以尝试修改配置区的 TARGET_LAMBDA 或 N_STEPS 来观察不同的收敛情况。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson

# --- 可调整参数配置区 ---

# 1. 核心参数：平均发生次数 (Lambda)
# 物理意义：假设单位时间内，我们期望发生的事件总数。例如：平均每小时接5个电话。
TARGET_LAMBDA = 5  

# 2. 实验设置：不同的切分粒度 (n)
# 物理意义：我们将这“一小时”切分成多少个微小的时间片。
# n 越小，说明切分越粗糙（例如每10分钟看一次），二项分布与泊松分布差异越大。
# n 越大，说明切分越精细（例如每毫秒看一次），两者越接近。
N_STEPS_LIST = [6, 20, 1000] 

# 3. 绘图范围
# X轴显示的事件次数范围 (0 到 MAX_K)
MAX_K = 15

# --- 绘图环境设置 (解决中文显示问题) ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'DejaVu Sans'] # 尝试加载常见中文字体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def run_simulation():
    # 创建画布，包含 3 行 1 列的子图
    fig, axes = plt.subplots(len(N_STEPS_LIST), 1, figsize=(8, 10), sharex=True)
    fig.suptitle(f'见证数学魔法：二项分布如何变成泊松分布\n(目标平均值 $\lambda={TARGET_LAMBDA}$)', fontsize=14)

    # 遍历我们设置的每一个 n (切分粒度)
    for i, n in enumerate(N_STEPS_LIST):
        ax = axes[i]
        
        # --- 核心数学逻辑 ---
        # 如果我们将总时间切分为 n 份，为了保持总期望为 λ，
        # 每一份时间片内发生事件的概率 p 必须满足： n * p = λ
        # 所以： p = λ / n
        p = TARGET_LAMBDA / n
        
        # 生成 X 轴坐标 (0, 1, 2, ..., MAX_K)
        x = np.arange(0, MAX_K + 1)
        
        # 1. 计算二项分布概率 (Binomial PMF)
        # 这是“现实”的模拟：有限次试验，每次概率为 p
        binom_probs = binom.pmf(x, n, p)
        
        # 2. 计算泊松分布概率 (Poisson PMF)
        # 这是“理想”的极限：直接用 λ 计算
        poisson_probs = poisson.pmf(x, TARGET_LAMBDA)
        
        # --- 绘图 ---
        # 绘制二项分布 (蓝色柱状图)
        ax.bar(x, binom_probs, alpha=0.6, color='#1f77b4', label=f'二项分布 (n={n}, p={p:.3f})', width=0.6)
        
        # 绘制泊松分布 (红色圆点虚线)
        # 我们用它作为“标准答案”来对比
        ax.plot(x, poisson_probs, 'ro--', alpha=0.8, linewidth=2, label=f'泊松分布理论值 ($\lambda={TARGET_LAMBDA}$)')
        
        # --- 图表美化与注释 ---
        ax.set_ylabel('概率', fontsize=10)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        
        # 添加评语，帮助理解
        if n <= TARGET_LAMBDA + 2:
            title_text = f"切分太粗 (n={n})：误差很大，形状都不太像"
        elif n < 100:
            title_text = f"切分适中 (n={n})：开始接近，但峰值处仍有偏差"
        else:
            title_text = f"切分极细 (n={n})：完美重合！这就是泊松分布的本质"
        
        ax.set_title(title_text, fontsize=11, color='#333333')

    axes[-1].set_xlabel('事件发生的次数 (k)', fontsize=12)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92) # 留出标题空间
    
    print(f"绘图完成。请观察弹出的窗口。")
    print(f"注意观察：当 n={N_STEPS_LIST[-1]} 时，蓝色柱子和红色虚线是如何完美重叠的。")
    plt.show()

if __name__ == "__main__":
    run_simulation()