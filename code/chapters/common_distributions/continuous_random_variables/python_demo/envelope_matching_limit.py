"""
文件名: envelope_matching_limit.py
功能: 模拟信封配对问题并验证至少一封装对的概率收敛至 1-1/e

【这是什么？】
通过蒙特卡洛模拟（暴力投骰子），重现将 n 封信随机装入 n 个信封的过程。
随着信件数量 n 的增加，程序会计算“至少有一封信装对”的实际发生频率，并将其与理论极限值（1 - 1/e）进行对比。

【怎么用？】
直接运行脚本。程序会在终端输出不同信件数量下的模拟概率，并自动弹出一张折线图。
图表中，蓝线代表模拟的实际概率，红线代表理论极限。你会直观地看到蓝线是如何迅速逼近并死死贴住红线的。
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# --- 可调整参数配置区 ---
# 测试的信封数量列表（比如测试 2封、3封、5封...一直到 50封）
N_VALUES = [2, 3, 4, 5, 10, 20, 30, 40, 50]

# 每个 n 下进行的独立模拟试验次数（试验次数越大，频率越接近真实概率）
NUM_TRIALS = 50000 

# ------------------------

def simulate_envelope_matching(n, trials):
    """
    核心模拟引擎：执行批量装信试验
    """
    # 【数学对应】：生成真实信件的编号，设为 [0, 1, 2, ..., n-1]
    # 我们将其视作信封的标准正确位置
    correct_positions = np.arange(n)
    
    # 【数学对应】：模拟闭眼乱塞。
    # 生成 trials 个 0 到 n-1 的随机排列。这里利用 argsort 实现高效的批量随机打乱
    # 每一行代表一次完整的试验（一种随机装信的结果）
    random_assignments = np.random.rand(trials, n).argsort(axis=1)
    
    # 【数学对应】：检查随机装信的结果是否与正确位置一致。
    # 结果是一个布尔型矩阵，True 表示信 i 装入了信封 i（即 X_i = 1）
    matches = (random_assignments == correct_positions)
    
    # 【数学对应】：计算每次试验中的总装对数量 S_n = X_1 + X_2 + ... + X_n
    # 按行求和，得到每次试验中碰巧装对的信件总数
    s_n = matches.sum(axis=1)
    
    # 【数学对应】：筛选出“至少一封装对”的事件 (S_n >= 1)
    at_least_one_match = (s_n >= 1)
    
    # 【数学对应】：利用大数定律，计算事件发生的相对频率，作为概率 P(S_n >= 1) 的近似值
    empirical_prob = at_least_one_match.mean()
    
    return empirical_prob

def main():
    # 存储不同 n 下的模拟概率结果
    empirical_probs = []
    
    print(f"开始模拟... (每次进行 {NUM_TRIALS} 轮装信试验)\n")
    print(f"{'信封数量 (n)':<15} | {'至少对一封的模拟概率':<25}")
    print("-" * 45)
    
    # 遍历不同的信件数量 n，进行批量模拟
    for n in N_VALUES:
        prob = simulate_envelope_matching(n, NUM_TRIALS)
        empirical_probs.append(prob)
        print(f"{n:<17} | {prob:.4f}")
        
    # 【数学对应】：计算理论极限值 1 - 1/e
    theoretical_limit = 1 - math.exp(-1)
    print("-" * 45)
    print(f"理论极限值 1 - 1/e : {theoretical_limit:.4f}\n")
    
    # --- 绘图部分 ---
    plt.figure(figsize=(10, 6))
    
    # 绘制模拟结果的折线图
    plt.plot(N_VALUES, empirical_probs, marker='o', linestyle='-', color='b', label='Empirical Probability (Simulation)')
    
    # 绘制理论极限的水平参考线
    plt.axhline(y=theoretical_limit, color='r', linestyle='--', label='Theoretical Limit (1 - 1/e)')
    
    plt.title('Probability of At Least One Envelope Matching', fontsize=14)
    plt.xlabel('Number of Envelopes (n)', fontsize=12)
    plt.ylabel('Probability P(S_n >= 1)', fontsize=12)
    plt.ylim(0.4, 0.8)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    
    # 显示图表
    plt.show()

if __name__ == "__main__":
    main()