"""
文件名: random_variable_mapping_demo.py
功能: 演示同一随机试验下，不同“随机变量（映射规则）”如何产生不同的数值分布

【这是什么？】
随机变量本质上是一个测量函数，负责把原始的物理结果（样本点）映射为实数。
这段代码通过模拟抛掷两颗骰子的过程，直观地展示了：当我们对同一个物理样本空间
应用不同的“测量规则”（例如求和、求最大值、求差）时，同一个随机现象是如何
在实数轴上展现出完全不同的概率分布面貌的。

【怎么用？】
直接运行本脚本。程序将模拟抛掷骰子，并在终端打印出不同映射规则下的统计频率，
同时弹出一张图表，对比展示这三个不同随机变量的值域范围和概率分布形状。
"""

import numpy as np
import matplotlib.pyplot as plt

# 为了在图表中正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
NUM_TRIALS = 100000  # 模拟独立重复试验的次数（大数定律保证其频率逼近概率）
DICE_SIDES = 6       # 骰子的面数
# ------------------------

def main():
    # 1. 构造样本空间与执行随机试验
    # 这里我们生成两个形状为 (NUM_TRIALS,) 的数组，代表十万次独立试验的原始物理结果
    # 每一个配对 (dice1[i], dice2[i]) 就是一个具体的样本点 ω
    dice1 = np.random.randint(1, DICE_SIDES + 1, size=NUM_TRIALS)
    dice2 = np.random.randint(1, DICE_SIDES + 1, size=NUM_TRIALS)
    
    # 2. 定义随机变量（映射规则）
    # 随机变量是映射 X: Ω -> R。我们对刚才生成的原始样本点应用三种不同的数学函数
    
    # 随机变量 S: 记录两颗骰子的点数之和 S(ω) = i + j
    S = dice1 + dice2
    
    # 随机变量 M: 记录两颗骰子中较大的点数 M(ω) = max(i, j)
    M = np.maximum(dice1, dice2)
    
    # 随机变量 D: 记录两颗骰子点数的绝对差 D(ω) = |i - j|
    D = np.abs(dice1 - dice2)

    # 3. 统计与可视化：从样本空间过渡到实数轴上的概率分布
    # 下面的代码用于计算这几个随机变量在各自值域上取值的频率（以此逼近真实概率）
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    variables = [
        (S, "随机变量 S (点数之和)", "#1F77B4"),
        (M, "随机变量 M (最大点数)", "#FF7F0E"),
        (D, "随机变量 D (点数之差)", "#2CA02C")
    ]
    
    for ax, (data, title, color) in zip(axes, variables):
        # 统计每个实数取值出现的次数，并除以总试验次数，得到频率（映射后的概率测度）
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / NUM_TRIALS
        
        # 在实数轴上绘制分布
        ax.bar(values, probabilities, color=color, alpha=0.8, edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel("映射后的实数取值 (x)")
        ax.set_ylabel("P(X = x) 逼近值")
        ax.set_xticks(range(min(values), max(values) + 1))
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.suptitle(f"同一组物理样本点，在 {NUM_TRIALS} 次试验下被三个随机变量映射后的不同面貌", y=1.05)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()