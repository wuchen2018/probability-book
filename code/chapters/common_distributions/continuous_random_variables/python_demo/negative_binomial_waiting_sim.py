"""
文件名: negative_binomial_waiting_sim.py
功能: 模拟“直到第r次成功”的等待过程，并对比理论概率分布

【这是什么？】
这段代码模拟了一个经典的概率场景：假设每次尝试成功的概率固定（比如抛硬币或抽卡），
我们要统计“为了凑齐 r 次成功，到底需要尝试多少次”。
通过成千上万次的模拟，它能帮你直观地看到负二项分布的“右偏”特性（也就是那个长长的尾巴），
验证为什么平均等待次数会比你想象的要多。

【怎么用？】
直接运行即可。
1. 控制台会输出模拟的平均尝试次数与理论值的对比。
2. 会弹出一张图表，展示实际模拟的分布柱状图与理论概率曲线的重合程度。
你可以尝试修改 r 的值（比如改成 10），看看为了多凑几次成功，分布的形状会发生什么剧烈变化。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nbinom

# --- 可调整参数配置区 ---
TARGET_SUCCESSES_R = 3      # 目标：我们需要凑齐多少次成功（r）
PROB_SUCCESS_P = 0.5        # 概率：单次尝试成功的概率（p，比如硬币是0.5）
NUM_SIMULATIONS = 10000     # 实验次数：我们模拟多少轮这个游戏（样本量越大越精准）

# 绘图设置（支持中文显示）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

def run_simulation():
    """执行蒙特卡洛模拟"""
    print(f"--- 开始模拟：目标是凑齐 {TARGET_SUCCESSES_R} 次成功，单次概率 {PROB_SUCCESS_P} ---")
    
    # 用来记录每一轮实验“总共尝试了多少次”
    trials_records = []

    # --- 核心模拟循环 ---
    # 我们不使用现成的分布函数，而是用最原始的“抛硬币”逻辑来模拟，
    # 这样你能看清概率过程的本质。
    for _ in range(NUM_SIMULATIONS):
        success_count = 0  # 当前累计成功次数
        trial_count = 0    # 当前累计尝试次数
        
        # 只要没凑够 r 次成功，就一直试下去！
        while success_count < TARGET_SUCCESSES_R:
            trial_count += 1
            # 生成一个 0 到 1 之间的随机数，如果小于 p 则视为成功
            if np.random.random() < PROB_SUCCESS_P:
                success_count += 1
        
        # 记录这一轮为了达成目标，总共花了多少次
        trials_records.append(trial_count)

    # 转换为 numpy 数组方便计算
    trials_records = np.array(trials_records)

    # --- 结果分析 ---
    # 1. 计算模拟的平均值
    sim_mean = np.mean(trials_records)
    # 2. 计算理论期望值 E(X) = r / p
    # 数学原理：每凑齐1个成功平均需要 1/p 次，凑齐 r 个就需要 r/p 次
    theory_mean = TARGET_SUCCESSES_R / PROB_SUCCESS_P

    print(f"理论平均等待次数: {theory_mean:.2f}")
    print(f"模拟平均等待次数: {sim_mean:.2f}")
    print(f"误差: {abs(sim_mean - theory_mean):.4f}")

    # --- 可视化对比 ---
    plt.figure(figsize=(10, 6))

    # 1. 绘制模拟数据的直方图（柱状图）
    # bins 设置为从 r 开始到最大值，保证每个整数都有一个柱子
    max_k = np.max(trials_records)
    bins = np.arange(TARGET_SUCCESSES_R, max_k + 2) - 0.5
    
    plt.hist(trials_records, bins=bins, density=True, alpha=0.6, color='skyblue', label='模拟实验频率')

    # 2. 绘制理论概率曲线（红色线条）
    # 注意：scipy 的 nbinom 定义是“失败次数”，而我们统计的是“总次数 k”
    # 所以传入 nbinom.pmf 的参数应该是 k - r (即失败次数)
    k_values = np.arange(TARGET_SUCCESSES_R, max_k + 1)
    # pmf: Probability Mass Function (概率质量函数)
    theory_probs = nbinom.pmf(k_values - TARGET_SUCCESSES_R, TARGET_SUCCESSES_R, PROB_SUCCESS_P)
    
    plt.plot(k_values, theory_probs, 'r-o', linewidth=2, label='理论概率分布 (负二项)')

    # 图表修饰
    plt.title(f'负二项分布模拟：目标 r={TARGET_SUCCESSES_R}, 成功率 p={PROB_SUCCESS_P}')
    plt.xlabel('达成目标所需的总试验次数 (k)')
    plt.ylabel('概率 / 频率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 标记期望值
    plt.axvline(theory_mean, color='green', linestyle='--', label=f'期望值 E(X)={theory_mean}')
    plt.text(theory_mean + 0.5, max(theory_probs)/2, '理论平均值', color='green')

    print("绘图完成，请查看弹出的窗口。")
    plt.show()

if __name__ == "__main__":
    run_simulation()