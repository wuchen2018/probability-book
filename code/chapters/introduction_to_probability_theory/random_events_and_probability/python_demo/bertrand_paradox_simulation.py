"""
文件名: bertrand_paradox_simulation.py
功能: 蒙特卡洛模拟贝特朗悖论的三种随机发牌规则

【这是什么？】
计算机无法理解抽象的“几何概型”，但极其擅长“暴力扔飞镖”。这段代码通过产生上百万次的随机数，用频率去逼近概率。它揭示了数学上的核心机密：对“随机”这个词的物理动作定义不同（选端点、选距离、选面积），会导致样本空间彻底改变，最终跑出来的概率截然不同。

【怎么用？】
直接运行此脚本。程序会瞬间完成三百万次模拟实验，并在控制台打印出三种随机生成策略下，弦长大于圆内接等边三角形边长的实际概率。你可以尝试修改 N_SIMULATIONS 的大小，观察大数定律下频率是如何死死咬住理论值的。
"""

import numpy as np

# --- 可调整参数配置区 ---
N_SIMULATIONS = 1_000_000  # 模拟次数（抛硬币/扔飞镖的次数），建议保持在百万级别以观察收敛
R = 1.0                    # 圆的半径
TARGET_LENGTH = R * np.sqrt(3) # 目标阈值：圆内接等边三角形的边长 (\sqrt{3} * R)

def simulate_method_1():
    # ==========================================
    # 策略一：端点随机 (理论概率：1/3)
    # ==========================================
    # 物理动作：固定弦的一个端点在圆周上，随机在圆周上选另一个端点。
    # 数学本质：样本空间是 [0, 2π) 的一维均匀分布（角度）。
    
    # 1. 产生 N 个 [0, 2π) 的均匀随机角度，代表动点与固定点之间的圆心角
    angles = np.random.uniform(0, 2 * np.pi, N_SIMULATIONS)
    
    # 2. 根据余弦定理（或直接用半角公式），计算弦长。
    # 弦长公式：L = 2 * R * sin(θ/2)
    chord_lengths = 2 * R * np.sin(angles / 2)
    
    # 3. 统计“有效事件”发生的次数：弦长是否大于阈值
    success_count = np.sum(chord_lengths > TARGET_LENGTH)
    return success_count / N_SIMULATIONS

def simulate_method_2():
    # ==========================================
    # 策略二：弦心距随机 (理论概率：1/2)
    # ==========================================
    # 物理动作：在半径上随机取一个点，作垂直于该半径的弦。
    # 数学本质：样本空间是 [0, R) 的一维均匀分布（线段长度）。
    
    # 1. 产生 N 个 [0, R) 的均匀随机数，代表弦心距 d
    distances = np.random.uniform(0, R, N_SIMULATIONS)
    
    # 2. 根据勾股定理计算弦长。
    # 半弦长^2 + 弦心距^2 = 半径^2  => 弦长 = 2 * sqrt(R^2 - d^2)
    chord_lengths = 2 * np.sqrt(R**2 - distances**2)
    
    # 3. 统计有效次数
    success_count = np.sum(chord_lengths > TARGET_LENGTH)
    return success_count / N_SIMULATIONS

def simulate_method_3():
    # ==========================================
    # 策略三：中点随机 (理论概率：1/4)
    # ==========================================
    # 物理动作：在圆盘的二维面积内，像扔飞镖一样随机扎一个点，作为弦的中点。
    # 数学本质：样本空间是面积为 πR^2 的二维均匀分布。
    
    # 注意：要在二维圆盘内实现“面积均匀”，极坐标下的半径 r 不能是均匀分布的！
    # 如果 r 均匀，圆心附近点会异常密集。正确的做法是让 r^2 均匀分布。
    # 1. 产生 N 个 [0, R^2) 的均匀随机数，代表中点到圆心距离的平方 (d^2)
    d_squared = np.random.uniform(0, R**2, N_SIMULATIONS)
    
    # 2. 依然利用勾股定理计算弦长：弦长 = 2 * sqrt(R^2 - d^2)
    chord_lengths = 2 * np.sqrt(R**2 - d_squared)
    
    # 3. 统计有效次数
    success_count = np.sum(chord_lengths > TARGET_LENGTH)
    return success_count / N_SIMULATIONS

if __name__ == "__main__":
    print(f"正在进行蒙特卡洛模拟，每次实验抛掷 {N_SIMULATIONS:,} 次...\n")
    
    prob_1 = simulate_method_1()
    print(f"策略一 (端点随机)   | 模拟值: {prob_1:.5f} | 理论值: {1/3:.5f} (1/3)")
    
    prob_2 = simulate_method_2()
    print(f"策略二 (弦心距随机) | 模拟值: {prob_2:.5f} | 理论值: {1/2:.5f} (1/2)")
    
    prob_3 = simulate_method_3()
    print(f"策略三 (中点随机)   | 模拟值: {prob_3:.5f} | 理论值: {1/4:.5f} (1/4)")
    
    print("\n结论：不存在绝对的“随机”。你在代码里调用 random 时的物理定义，决定了最终的概率宇宙。")