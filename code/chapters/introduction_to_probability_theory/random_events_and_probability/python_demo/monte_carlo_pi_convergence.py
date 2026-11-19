"""
文件名: monte_carlo_pi_convergence.py
功能: 利用随机撒点（蒙特卡洛方法）估算圆周率，并动态展示估算值随实验次数增加的收敛过程。

【这是什么？】
几何概型与大数定律结合的经典应用。当我们在一个正方形内均匀、随机地生成点时，点落入内切圆的概率等于圆面积与正方形面积之比（π/4）。通过统计落入圆内点的频率，并乘以4，我们就能用纯粹的随机实验反向“测量”出真实的 π 值。

【怎么用？】
直接运行本脚本。程序会在后台执行海量的“虚拟撒豆子”实验，并绘制出一张折线图。你将直观地看到：在最初的几百次实验中，估算值会剧烈震荡；但随着样本量的指数级增加，这条震荡的曲线最终会被死死地钉在真实的 π 值附近。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 解决 matplotlib 中文显示问题 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Microsoft YaHei'] # 兼容 Windows/Mac
plt.rcParams['axes.unicode_minus'] = False # 正常显示负号

# --- 可调整参数配置区 ---
TOTAL_POINTS = 50000      # 实验总次数 N：即总共要在正方形里撒下多少个随机点
BATCH_SIZE = 100          # 绘图降采样率：每隔多少个点记录一次估算值（值越小，曲线细节越丰富，但画图越慢）
RANDOM_SEED = 42          # 随机种子：固定种子可以复现同样的折线走势，设为 None 则每次运行结果都不同
TARGET_PI = np.pi         # 宇宙真实的圆周率，作为我们验证的靶心

def simulate_monte_carlo_pi():
    # 设置随机数种子
    if RANDOM_SEED is not None:
        np.random.seed(RANDOM_SEED)

    print(f"正在往正方形中撒入 {TOTAL_POINTS} 个随机点，请稍候...")

    # 1. 构建样本空间与等可能分布
    # 几何概型的前提是“空间中任意位置等可能”。
    # 使用 uniform 均匀分布，模拟点在 X 轴 [-1, 1] 和 Y 轴 [-1, 1] 的方形区域内无偏好地落下。
    x = np.random.uniform(-1, 1, TOTAL_POINTS)
    y = np.random.uniform(-1, 1, TOTAL_POINTS)

    # 2. 定义目标事件与代数判定
    # 我们的目标事件 A 是“点落入半径为 1 的内切圆中”。
    # 根据解析几何，这等价于判断点的坐标是否满足 x^2 + y^2 <= 1^2。
    distance_squared = x**2 + y**2
    inside_circle_bool = distance_squared <= 1

    # 3. 统计累积频数
    # np.cumsum 会计算一个逐步累加的数组。
    # 这对应了数学中对“有利事件发生次数 M”的动态记录：第 n 次实验时，总共有几个点落在了圆内。
    cumulative_inside = np.cumsum(inside_circle_bool)

    # 4. 生成对应的实验总次数序列
    # 生成从 1 到 TOTAL_POINTS 的数组，代表分母 N（已经进行了多少次实验）。
    n_trials = np.arange(1, TOTAL_POINTS + 1)

    # 5. 核心计算：从频率推导常数
    # 频率 M/N 近似等于理论概率 P。
    # 因为理论概率 P = 圆面积 / 正方形面积 = (π*1^2) / (2*2) = π/4。
    # 移项得到：π ≈ 4 * (M / N)。这就实现了从随机频率到确定性常数的跨越。
    pi_estimates = 4 * cumulative_inside / n_trials

    # --- 以下为可视化呈现代码 ---
    # 提取用于画图的数据点（避免数据量过大导致画图卡顿）
    plot_trials = n_trials[::BATCH_SIZE]
    plot_estimates = pi_estimates[::BATCH_SIZE]

    plt.figure(figsize=(10, 6))
    
    # 绘制估算值的波动曲线
    plt.plot(plot_trials, plot_estimates, color='#1F77B4', alpha=0.9, linewidth=1.5, label='蒙特卡洛估算值')
    
    # 绘制真实的 π 值作为基准线
    plt.axhline(y=TARGET_PI, color='#D62728', linestyle='--', linewidth=2, label=f'真实 $\pi$ 值 ({TARGET_PI:.5f}...)')
    
    # 设置图表格式
    plt.title('蒙特卡洛方法估算 $\pi$ 值的收敛过程', fontsize=14)
    plt.xlabel('随机撒点数量 (N)', fontsize=12)
    plt.ylabel('$\pi$ 的估算值', fontsize=12)
    
    # 限制 Y 轴的显示范围，只聚焦于 3.0 到 3.3 之间，以便看清微小的震荡
    plt.ylim(3.0, 3.3)
    
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.legend(loc='upper right')
    
    print(f"模拟完成！最终经过 {TOTAL_POINTS} 次实验，估算出的 π 值为: {pi_estimates[-1]:.5f}")
    plt.show()

if __name__ == "__main__":
    simulate_monte_carlo_pi()