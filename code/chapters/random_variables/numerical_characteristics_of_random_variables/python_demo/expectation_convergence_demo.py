"""
文件名: expectation_convergence_demo.py
功能: 模拟随机事件的长期算术平均收敛于数学期望的过程

【这是什么？】
大数定律的直观可视化。它证明了虽然每一次随机试验的结果都无法绝对预测（单次充满剧烈的上下波动），
但当你把成千上万次独立试验的结果计算算术平均时，这个平均值会被一股无形的力量死死“钉”在一个确定的数字上——这个数字就是数学期望。

【怎么用？】
直接运行本脚本。程序会弹出一张动态折线图，展示随着实验次数从 1 增加到设定值，
原本剧烈震荡的“实时平均收益”是如何逐渐平息，最终完美贴合在理论期望值（红色虚线）上的。
强烈建议你修改配置区的“结果与概率”，观察收敛线将如何忠实地跟随你的数学设定而改变。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---

# 实验总次数 (N)：建议设置在 10000 到 100000 之间，体会“长期”的威力
NUM_TRIALS = 50000 

# 随机变量的所有可能取值 (样本空间)：比如赢10元、输5元
OUTCOMES = [10, -5]

# 对应取值的发生概率 (概率分布)：必须与 OUTCOMES 一一对应，且总和必须为 1.0
PROBABILITIES = [0.5, 0.5] 

# ------------------------

def setup_chinese_font():
    """配置 matplotlib 以支持中文显示，兼容 Windows 和 Mac"""
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Arial Unicode MS', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def main():
    setup_chinese_font()

    # 1. 理论计算阶段：按照定义 E(X) = Σ (x_i * p_i) 计算数学期望
    # 这里我们用向量点乘的方式，完美对应了“以概率为权重的加权平均”这一数学定义
    theoretical_expectation = np.dot(OUTCOMES, PROBABILITIES)
    print(f"理论数学期望 E(X) = {theoretical_expectation:.4f}")

    # 2. 蒙特卡洛模拟阶段：让计算机掷无数次虚拟骰子
    # np.random.choice 严格按照我们设定的概率分布 (p=PROBABILITIES)，生成长度为 NUM_TRIALS 的随机变量序列
    # 这一步代表了现实世界中发生的每一次真实且不可预测的独立事件
    random_events = np.random.choice(OUTCOMES, size=NUM_TRIALS, p=PROBABILITIES)

    # 3. 统计汇总阶段：计算“长期的算术平均”
    # np.cumsum 计算累积和，代表到第 n 次试验为止的总收益
    cumulative_sum = np.cumsum(random_events)
    # 构造一个从 1 到 N 的数组，代表当前的试验次数 n
    trials_count = np.arange(1, NUM_TRIALS + 1)
    # 将累积总和除以当前次数，得到 n 次试验下的实时算术平均值
    running_averages = cumulative_sum / trials_count

    # 4. 可视化阶段：将数学定理转化为视觉直觉
    plt.figure(figsize=(10, 6))
    
    # 绘制随着试验次数增加，算术平均值的游走轨迹
    # 你会看到在 n 较小时，轨迹极其狂野（小样本的随机性）
    plt.plot(trials_count, running_averages, color='#1F77B4', alpha=0.8, linewidth=1.5, label='实时算术平均值')
    
    # 绘制理论上的数学期望线（上帝视角的绝对中心）
    # 你会看到无论平均值前期如何挣扎，最终都会被“吸附”到这条线上（大数定律的必然性）
    plt.axhline(y=theoretical_expectation, color='#D62728', linestyle='--', linewidth=2, 
                label=f'理论数学期望 (E(X) = {theoretical_expectation})')

    # 图表细节修饰
    plt.title('频率稳定于概率，均值收敛于期望', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('独立重复试验次数 (n)', fontsize=12)
    plt.ylabel('平均结果', fontsize=12)
    
    # 使用对数坐标轴更能看清单次极度随机到长期极度稳定的演变过程
    plt.xscale('log') 
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    print("正在生成收敛图表，请在弹出的窗口中查看...")
    plt.show()

if __name__ == "__main__":
    main()