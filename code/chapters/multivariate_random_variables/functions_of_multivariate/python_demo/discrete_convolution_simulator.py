# -*- coding: utf-8 -*-
"""
文件名: discrete_convolution_simulator.py
功能: 模拟离散型随机变量“求和”后的分布变化（卷积演示）

【这是什么？】
这段代码演示了当你把多个独立的随机变量（比如骰子）加在一起时，它们的概率分布会发生什么神奇的变化。
它直观地展示了“卷积”运算的几何意义：随着加的次数变多，原本形状各异的分布，是如何一步步变成“钟形曲线”（正态分布）的。

【怎么用？】
1. 在“可调整参数配置区”修改初始分布（比如把骰子改成只有三面的，或者灌铅的）。
2. 修改“叠加次数”，看看加多少次后分布会变得对称。
3. 运行代码，观察生成的对比图。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# --- 可调整参数配置区 ---

# 1. 定义初始随机变量 X 的分布律 (Probability Mass Function)
# 这里模拟一个标准的6面均匀骰子：点数 1~6，概率都是 1/6
# 数组索引代表 (点数-1)，值代表概率
# 你可以试着把它改成不均匀的，例如: [0.1, 0.1, 0.1, 0.1, 0.1, 0.5] (灌铅骰子)
initial_probs = np.array([1/6, 1/6, 1/6, 1/6, 1/6, 1/6])

# 初始分布对应的点数起始值（例如骰子最小是1）
start_value = 1

# 2. 定义我们要叠加多少次
# list中每个数字代表：我们要看 "X1 + ... + Xn" 的分布
# 建议保留 1 (原始), 2 (两个的和), 3 (三个的和), 以及一个较大的数 (如 10)
stages_to_plot = [1, 2, 3, 5, 10]

# --------------------------

def plot_distribution(ax, probs, start_val, stage_n):
    """
    绘制某一阶段的分布图
    """
    # 计算 x 轴的取值范围
    # 如果 X1 最小是 1，那么 X1+...+Xn 最小就是 n * 1
    # 数组长度就是可能的取值个数
    x_values = np.arange(start_val * stage_n, start_val * stage_n + len(probs))
    
    # 绘制柱状图
    ax.bar(x_values, probs, width=0.8, color='#1F77B4', alpha=0.7, edgecolor='black')
    
    # 设置标题和标签
    ax.set_title(f"n = {stage_n} (叠加 {stage_n} 次)", fontsize=10)
    ax.set_ylabel("概率 P", fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # 如果柱子太多，就不显示所有x轴刻度了，免得挤在一起
    if len(probs) < 20:
        ax.set_xticks(x_values)

def main():
    # 设置绘图风格
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 准备画布：根据我们要画几个阶段，动态生成子图
    num_plots = len(stages_to_plot)
    fig, axes = plt.subplots(num_plots, 1, figsize=(8, 3 * num_plots), constrained_layout=True)
    
    # 确保 axes 是可迭代的（如果只有一个图，matplotlib返回的是对象不是数组）
    if num_plots == 1:
        axes = [axes]

    # 初始化当前分布
    # current_probs 存储的是 P(Sum = k) 的所有概率值
    current_probs = initial_probs.copy()
    
    # 记录当前的叠加次数（从 n=1 开始）
    current_n = 1
    
    # 遍历我们想要展示的每一个阶段
    # 注意：stages_to_plot 必须是递增的
    plot_idx = 0
    max_stage = max(stages_to_plot)
    
    # 循环演化直到达到设定的最大叠加次数
    # 这里的逻辑是：一步步做卷积，如果是我们想看的阶段，就画图
    for n in range(1, max_stage + 1):
        
        # 如果当前 n 在我们要画的列表里
        if n in stages_to_plot:
            plot_distribution(axes[plot_idx], current_probs, start_value, n)
            plot_idx += 1
        
        # --- 核心数学步骤：卷积 (Convolution) ---
        # 这一步对应数学公式：P(Z = k) = Σ P(X=i) * P(Y=k-i)
        # 在代码中，利用 numpy.convolve 可以极其快速地完成这个“多项式乘法”
        # 每次循环，相当于把当前的“和分布”再加一个新的“初始变量”
        if n < max_stage:
            current_probs = np.convolve(current_probs, initial_probs)

    # 添加总标题
    # 配置中文字体，防止乱码（根据系统不同可能需要调整，这里尝试使用通用设置）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans'] 
    plt.rcParams['axes.unicode_minus'] = False 
    
    fig.suptitle('从“卷积”到“正态分布”的演化过程\n(观察形状如何变宽、变平滑、变对称)', fontsize=14, y=1.02)
    
    print(f"绘图完成。请观察弹出的窗口。")
    print(f"注意观察 n=1 (平顶) 到 n={max_stage} (钟形) 的显著变化。")
    plt.show()

if __name__ == "__main__":
    main()