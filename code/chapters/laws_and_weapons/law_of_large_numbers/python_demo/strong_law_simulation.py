# -*- coding: utf-8 -*-
"""
文件名: strong_law_simulation.py
功能: 模拟强大数定律 (SLLN) 的收敛过程：从混沌到秩序

【这是什么？】
这段代码带你亲眼见证“频率”是如何随着试验次数的增加，顽固地收敛于“概率”的。
它模拟了多个平行的“掷硬币”实验（即多个平行宇宙），并记录下每一条时间线上的频率变化轨迹。

【怎么用？】
直接运行即可。你会看到一个动态生成的图表：
1. 几条彩色的线：代表不同的实验轨迹（平行宇宙），起初它们上蹿下跳（随机性），最后都会死死吸附在理论均值上（确定性）。
2. 你可以在下方的“参数配置区”修改硬币的概率或试验次数，看看规律是否依然成立。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 理论概率 (True Probability): 这里设为 0.5，代表一枚公平的硬币
# 你可以试着把它改成 0.1 (小概率事件) 或 0.9 (大概率事件)
TRUE_PROBABILITY = 0.5

# 试验次数 (N): 模拟抛掷多少次硬币
# 建议至少设置在 1000 以上，才能看到明显的收敛效果
NUM_TRIALS = 2000

# 平行宇宙数量 (M): 同时模拟几组实验
# 设为 5 组，方便对比不同轨迹的“殊途同归”
NUM_UNIVERSES = 5

# --- 绘图与字体设置 (防止中文乱码) ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def run_simulation():
    """执行模拟并绘图"""
    
    # 创建画布
    plt.figure(figsize=(12, 6))
    
    # 绘制理论概率基准线 (The Target)
    # 这就是强大数定律中，样本均值最终要收敛到的那个常数 μ
    plt.axhline(y=TRUE_PROBABILITY, color='black', linestyle='--', linewidth=2, label=f'理论概率 μ={TRUE_PROBABILITY}')
    
    # 生成 x 轴数据：代表试验次数 n (从 1 到 NUM_TRIALS)
    n_steps = np.arange(1, NUM_TRIALS + 1)
    
    print(f"开始模拟 {NUM_UNIVERSES} 个平行宇宙，每个宇宙抛掷 {NUM_TRIALS} 次...")

    # 循环模拟每一个“平行宇宙”
    for i in range(NUM_UNIVERSES):
        # 1. 模拟数据生成 (Data Generation)
        # np.random.binomial(1, p, n) 模拟 n 次伯努利试验 (0或1)
        # 结果类似于: [0, 1, 1, 0, 1, ...]
        flips = np.random.binomial(1, TRUE_PROBABILITY, NUM_TRIALS)
        
        # 2. 计算累积和 (Cumulative Sum, S_n)
        # 对应数学公式: S_n = X_1 + X_2 + ... + X_n
        cumulative_heads = np.cumsum(flips)
        
        # 3. 计算实时样本均值 (Sample Mean, X_bar_n)
        # 对应数学公式: X_bar_n = S_n / n
        current_means = cumulative_heads / n_steps
        
        # 4. 绘制轨迹
        # alpha设置透明度，linewidth设置线宽
        plt.plot(n_steps, current_means, alpha=0.7, linewidth=1.5, label=f'平行宇宙 #{i+1}')

    # --- 图表美化 ---
    plt.title(f'强大数定律模拟：{NUM_UNIVERSES} 条独立轨迹的收敛过程', fontsize=14)
    plt.xlabel('试验次数 n (时间)', fontsize=12)
    plt.ylabel('正面出现的频率 (样本均值)', fontsize=12)
    plt.ylim(0, 1) # 频率必然在 0 到 1 之间
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # 添加文字说明
    plt.text(NUM_TRIALS * 0.5, TRUE_PROBABILITY + 0.1, 
             "随着 n 增大，随机性被“稀释”，\n所有轨迹必然收敛于理论值", 
             ha='center', color='darkred', fontsize=10)

    # 显示图表
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()