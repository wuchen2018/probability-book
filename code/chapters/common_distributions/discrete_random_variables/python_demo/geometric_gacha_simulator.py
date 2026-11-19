# -*- coding: utf-8 -*-
"""
文件名: geometric_gacha_simulator.py
功能: 模拟“抽卡/掉落/面试”等等待过程，直观展示几何分布的“长尾风险”与“平均值陷阱”。

【这是什么？】
数学告诉我们要“相信期望值”，比如 1% 的概率平均 100 次能中。
但这段代码会模拟 10,000 个平行宇宙中的你。
你会亲眼看到：虽然平均值确实是 100，但大量的你会在第 1 次就成功，
而还有一部分倒霉的你，可能抽了 500 次还在等待。
这就是几何分布的“波动性”——平均值无法以此为保底。

【怎么用？】
1. 修改下方配置区的 PROBABILITY（成功率）。
2. 运行脚本。
3. 观察生成的直方图，重点看红线（平均值）右侧那条长长的“尾巴”。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 可调整参数配置区 ---
# 每次尝试成功的概率 (例如 0.01 代表 1% 的掉率/录取率)
PROBABILITY = 0.02

# 模拟的样本数量 (例如模拟 10,000 个人或者 10,000 次实验)
NUM_SIMULATIONS = 10000

# 判定为“极其倒霉”的倍数阈值 (例如 3.0 代表等待时间超过了平均值的 3 倍)
UNLUCKY_THRESHOLD_MULTIPLIER = 3.0

# -----------------------

def simulate_waiting_game():
    # 1. 计算理论上的数学期望 (Expected Value = 1/p)
    # 这是我们在做计划时预期的“平均成本”
    theoretical_mean = 1 / PROBABILITY
    
    print(f"--- 模拟开始 ---")
    print(f"设定成功率: {PROBABILITY:.2%}")
    print(f"理论平均等待次数: {theoretical_mean:.1f} 次")
    
    # 2. 生成模拟数据 (核心步骤)
    # np.random.geometric 模拟了 NUM_SIMULATIONS 个人，每个人直到成功为止所用的次数
    # 这对应了现实中成千上万次独立的“等待实验”
    waiting_times = np.random.geometric(p=PROBABILITY, size=NUM_SIMULATIONS)
    
    # 3. 统计分析
    # 大数定律告诉我们：只要样本够多，模拟的平均值会无限逼近理论值
    actual_mean = np.mean(waiting_times)
    max_wait = np.max(waiting_times)
    
    # 计算有多少人落入了“长尾”区域 (等待时间 > 3倍平均值)
    # 这部分展示了风险：明明平均只要 N 次，但总有人需要 3N 次以上
    unlucky_threshold = theoretical_mean * UNLUCKY_THRESHOLD_MULTIPLIER
    unlucky_count = np.sum(waiting_times > unlucky_threshold)
    unlucky_ratio = unlucky_count / NUM_SIMULATIONS
    
    print(f"--- 模拟结果 (样本数 {NUM_SIMULATIONS}) ---")
    print(f"实际模拟平均值: {actual_mean:.2f} 次 (验证了大数定律)")
    print(f"最倒霉的一位等待了: {max_wait} 次 (感受一下几何分布的方差)")
    print(f"超过 {unlucky_threshold:.0f} 次才成功的比例: {unlucky_ratio:.2%} (这是长尾风险)")

    # 4. 可视化绘图
    plt.figure(figsize=(10, 6))
    
    # 设置支持中文的字体 (根据系统调整，Windows通常为SimHei, Mac为Arial Unicode MS)
    # 为了保证代码通用性，这里优先尝试加载系统字体，若失败则回退到英文
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'PingFang SC']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        pass

    # 绘制直方图：展示等待次数的分布
    # bins='auto' 让程序自动决定柱子的宽度
    # density=True 将频数转化为概率密度，方便与理论曲线对比
    count, bins, ignored = plt.hist(waiting_times, bins=50, density=True, 
                                    alpha=0.6, color='#1F77B4', label='模拟实验分布')

    # 绘制理论概率曲线 (P(X=k) = p(1-p)^(k-1))
    # 这是一个离散分布，但为了视觉连贯，我们画成曲线展示趋势
    x_vals = np.linspace(1, max_wait, max_wait)
    y_vals = PROBABILITY * (1 - PROBABILITY)**(x_vals - 1)
    plt.plot(x_vals, y_vals, linewidth=2, color='r', linestyle='--', label='理论概率曲线')

    # 标记平均值
    plt.axvline(theoretical_mean, color='k', linestyle='dashed', linewidth=1.5)
    plt.text(theoretical_mean + max_wait*0.02, max(y_vals)*0.8, 
             f'理论平均值: {theoretical_mean:.0f}次', color='k')

    # 标记“最倒霉”的区域
    # 几何分布的特点：虽然平均值很小，但总有极少数数据落在非常靠右的地方
    plt.xlabel('获得首次成功所需的尝试次数')
    plt.ylabel('概率密度')
    plt.title(f'几何分布模拟：成功率 {PROBABILITY:.1%} 下的等待游戏')
    plt.legend()
    plt.grid(alpha=0.3)
    
    print("绘图完成，请查看弹出的窗口。")
    plt.show()

if __name__ == "__main__":
    simulate_waiting_game()