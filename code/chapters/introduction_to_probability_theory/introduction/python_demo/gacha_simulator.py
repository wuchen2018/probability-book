"""
文件名: gacha_simulator.py
功能: 模拟稀有事件的连续独立重复试验（无保底机制抽卡）

【这是什么？】
将枯燥的乘法公式转化为十万个平行宇宙的真实模拟。通过让海量虚拟个体同时进行多次独立的随机尝试，直观展现独立事件概率的指数衰减，以及“二项分布”在现实中的残酷威力。

【怎么用？】
直接运行代码。你可以随意调整顶部的“单次成功率”和“尝试次数”，程序会利用蒙特卡洛方法打印出多少人“颗粒无收”，并画出一张直方图，让你亲眼看到好运与厄运在人群中的客观分布。
"""

import numpy as np
import matplotlib.pyplot as plt

# 为了确保读者在不同操作系统下运行不出现中文乱码，配置通用字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
P_SUCCESS = 0.01      # 单次尝试成功的概率（例如：1%）
NUM_TRIES = 100       # 每个个体连续尝试的次数（例如：连抽100次）
NUM_PLAYERS = 100000  # 模拟的总人数/平行宇宙数量（默认十万人）


def run_simulation():
    print(f"--- 正在开启 {NUM_PLAYERS} 个平行宇宙的模拟 ---")
    print(f"单次成功率: {P_SUCCESS*100}% | 尝试次数: {NUM_TRIES}")
    
    # 【数学对应：独立重复试验与二项分布】
    # np.random.binomial 本质上是在计算二项分布 B(n, p)。
    # n = NUM_TRIES, p = P_SUCCESS
    # 这里不需要用 for 循环跑十万次，矩阵运算一次性抛出十万组硬币。
    # 结果数组 results 中的每一个数字，代表一个玩家在 NUM_TRIES 次尝试中，总共成功的次数。
    results = np.random.binomial(n=NUM_TRIES, p=P_SUCCESS, size=NUM_PLAYERS)
    
    # 【数学对应：极端事件的概率统计】
    # 筛选出成功次数严格为 0 的玩家群体，也就是体验了纯粹“厄运”的样本。
    unlucky_players = np.sum(results == 0)
    
    # 【数学对应：频率学派的视角】
    # 用实际发生的大样本频率（unlucky_players / NUM_PLAYERS），去逼近理论概率。
    # 理论上的公式是：(1 - P_SUCCESS) 的 NUM_TRIES 次方。
    actual_zero_prob = unlucky_players / NUM_PLAYERS
    theoretical_zero_prob = (1 - P_SUCCESS) ** NUM_TRIES
    
    print("\n--- 模拟结果揭晓 ---")
    print(f"在这 {NUM_PLAYERS} 人中，一张都没抽到的“倒霉蛋”有：{unlucky_players} 人")
    print(f"实际出现的“颗粒无收”频率: {actual_zero_prob * 100:.2f}%")
    print(f"纯数学公式算出的理论概率: {theoretical_zero_prob * 100:.2f}%")
    print("（你会发现，当样本量足够大时，现实的统计频率死死地咬合着理论数学公式。）")

    # --- 绘制直方图，将分布视觉化 ---
    plt.figure(figsize=(10, 6))
    
    # 【数学对应：概率密度/质量函数的具象化】
    # bins 划分了成功次数的区间，density=True 表示将频数转化为频率，即纵轴代表概率。
    max_hits = max(results)
    bins = np.arange(-0.5, max_hits + 1.5, 1)
    
    plt.hist(results, bins=bins, color='#1F77B4', edgecolor='black', alpha=0.7, density=True)
    
    # 标出平均期望线：n * p
    expected_value = NUM_TRIES * P_SUCCESS
    plt.axvline(x=expected_value, color='red', linestyle='--', linewidth=2, 
                label=f'数学期望 (均值) = {expected_value:.1f}')
    
    plt.title(f'十万人模拟结果：单次成功率 {P_SUCCESS*100}%，连续尝试 {NUM_TRIES} 次', fontsize=14)
    plt.xlabel('累计成功次数', fontsize=12)
    plt.ylabel('出现该结果的人数占比 (频率)', fontsize=12)
    plt.xticks(range(0, max_hits + 1))
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    run_simulation()