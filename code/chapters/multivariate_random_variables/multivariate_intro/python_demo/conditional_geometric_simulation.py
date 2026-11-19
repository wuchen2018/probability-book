"""
文件名: conditional_geometric_simulation.py
功能: 模拟两个独立的几何分布变量，验证在已知它们之和固定的条件下，其中一个变量服从均匀分布。

【这是什么？】
几何分布通常描述“直到成功为止的试验次数”，概率随着次数增加而指数衰减（起伏很大）。
但数学告诉我们一个反直觉的结论：如果你和朋友各自进行试验，已知你们两人总共用了 n 次才都成功（X+Y=n），
那么你的成功次数 X 在 1 到 n-1 之间是“众生平等”的，没有任何偏向。
这就好像两座陡峭的山峰，相撞之后竟然撞出了一块平地。这段代码将带你亲眼目睹这个“削峰填谷”的过程。

【怎么用？】
直接运行即可。程序会生成两张图：
1. 原始的几何分布（可以看出明显的下降趋势）。
2. 施加条件 X+Y=n 后的 X 分布（你会看到它神奇地变平了）。
尝试修改顶部的 n 值，观察均匀分布范围的变化。
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# --- 可调整参数配置区 ---
PROB_SUCCESS = 0.3      # 每次试验成功的概率 p (0 < p < 1)
CONDITION_SUM = 20      # 已知条件：两个变量之和 n (X + Y = n)
SAMPLE_SIZE = 500000    # 模拟的总样本数 (为了保证有足够的数据落在条件上，建议设大一点)
# ------------------------

def run_simulation():
    # 1. 模拟现实世界：生成大量的独立随机实验
    # 我们生成两组独立的几何分布数据，代表两个人各自“首次成功”所需的次数
    # numpy 的 geometric 返回的是 1, 2, 3... 符合定义
    x_samples = np.random.geometric(p=PROB_SUCCESS, size=SAMPLE_SIZE)
    y_samples = np.random.geometric(p=PROB_SUCCESS, size=SAMPLE_SIZE)

    print(f"模拟完成：生成了 {SAMPLE_SIZE} 对 (X, Y) 数据。")

    # 2. 施加条件：筛选出符合 X + Y = n 的那些世界
    # 这对应数学公式中的“条件概率”分母部分，我们只保留满足条件的样本
    condition_mask = (x_samples + y_samples) == CONDITION_SUM
    
    # 提取满足条件的 X 值
    # 这就是我们要研究的对象：P(X | X+Y=n)
    x_conditional = x_samples[condition_mask]
    
    count_matched = len(x_conditional)
    print(f"满足条件 X+Y={CONDITION_SUM} 的样本数：{count_matched}")
    
    if count_matched < 100:
        print("警告：满足条件的样本太少，直方图可能不准确。建议增加 SAMPLE_SIZE 或调整 n/p。")

    # --- 绘图验证 ---
    plt.figure(figsize=(10, 8))
    
    # 子图1：展示原始的几何分布 (无条件)
    # 这是一个参照组，让你看到 X 本来的样子
    plt.subplot(2, 1, 1)
    plt.hist(x_samples, bins=range(1, max(x_samples)+1), density=True, 
             alpha=0.6, color='gray', edgecolor='black', label='原始数据 (模拟)')
    plt.title(f'原始几何分布 (p={PROB_SUCCESS})：明显的指数衰减', fontsize=12)
    plt.xlabel('试验次数 X')
    plt.ylabel('频率')
    plt.xlim(0, CONDITION_SUM + 5) # 限制X轴范围方便对比
    plt.legend()

    # 子图2：展示条件分布 (有条件)
    # 这是见证奇迹的时刻：理论上它应该是一个矩形（均匀分布）
    plt.subplot(2, 1, 2)
    
    # 绘制模拟数据的直方图
    # bins 设置为从 1 到 n，因为 X+Y=n 且 Y>=1，所以 X 最大只能是 n-1
    bins_list = range(1, CONDITION_SUM + 1)
    plt.hist(x_conditional, bins=bins_list, density=True, 
             alpha=0.7, color='#1F77B4', edgecolor='black', label='条件分布 P(X | X+Y=n)')
    
    # 绘制理论上的均匀分布红线
    # 理论值：1 / (n-1)
    if CONDITION_SUM > 1:
        theoretical_prob = 1 / (CONDITION_SUM - 1)
        plt.hlines(theoretical_prob, 1, CONDITION_SUM-1, colors='red', linewidth=3, 
                   linestyles='--', label='理论值：均匀分布')

    plt.title(f'条件分布 (给定 X+Y={CONDITION_SUM})：削峰填谷，变为均匀分布', fontsize=12)
    plt.xlabel('试验次数 X')
    plt.ylabel('条件概率')
    plt.xlim(0, CONDITION_SUM + 5)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()