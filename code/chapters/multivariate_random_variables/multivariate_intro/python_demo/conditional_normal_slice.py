"""
文件名: conditional_normal_slice.py
功能: 模拟二元正态分布的“切片”过程，验证条件分布的性质

【这是什么？】
这段代码通过生成大量随机数据，模拟二元正态分布 (X, Y)。
然后，它演示了我们在理论中学到的核心概念：
1. "条件"就是"切片"：我们在 Y 的某个特定值附近切一刀（选取一个小区间）。
2. "切片"后的形状：验证在切片内的 X 数据，是否真的服从我们推导出的单变量正态分布。
3. "线性回归"的起源：观察条件期望（切片的中心）是如何随 Y 变化的。

【怎么用？】
直接运行即可。你会看到两个图：
图1：整体散点图，红线标出了我们切片的位置。
图2：切片内部数据的直方图（模拟结果）与理论上的正态分布曲线（数学推导）的对比。
建议尝试修改 rho（相关系数），观察它如何影响切片的“宽窄”（即条件方差）。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 可调整参数配置区 (建议修改这里来观察变化) ---
N_SAMPLES = 50000       # 模拟样本点的总数量 (样本越多，直方图越接近理论曲线)
RHO = 0.8               # 相关系数 (-1 到 1 之间)。0.8 表示强正相关
SLICE_Y = 1.0           # 我们要在 Y 等于多少的地方切一刀？
EPSILON = 0.05          # 切片的厚度。因为在连续分布中 P(Y=y)=0，我们必须取 [y-ε, y+ε]

# 设定 X 和 Y 的基础参数 (标准正态分布参数，可不改)
MU_X, SIGMA_X = 0, 1
MU_Y, SIGMA_Y = 0, 1
# -----------------------------------------------

def run_simulation():
    # 1. 准备数据：生成二元正态分布的随机样本
    # 协方差矩阵：[[Var(X), Cov(X,Y)], [Cov(Y,X), Var(Y)]]
    # Cov(X,Y) = rho * sigma_x * sigma_y
    cov_xy = RHO * SIGMA_X * SIGMA_Y
    mean = [MU_X, MU_Y]
    cov_matrix = [[SIGMA_X**2, cov_xy], 
                  [cov_xy, SIGMA_Y**2]]
    
    print(f"正在生成 {N_SAMPLES} 个随机样本... 相关系数 rho={RHO}")
    # 生成数据，每一行是一个 (x, y) 点
    data = np.random.multivariate_normal(mean, cov_matrix, N_SAMPLES)
    X_samples = data[:, 0]
    Y_samples = data[:, 1]

    # 2. 执行“切片”操作 (模拟条件概率)
    # 在数学上是给定 Y=y，在计算机模拟中我们需要取一个微小的区间 |Y - y| < epsilon
    # 这对应了理论中 "epsilon -> 0" 的极限思想的前身
    condition_indices = np.abs(Y_samples - SLICE_Y) < EPSILON
    X_given_Y_samples = X_samples[condition_indices]
    
    print(f"在 Y={SLICE_Y} 附近 (±{EPSILON}) 截获了 {len(X_given_Y_samples)} 个样本点")

    # 3. 计算理论上的条件分布参数
    # 公式：E[X|Y=y] = mu_x + rho * (sigma_x/sigma_y) * (y - mu_y)
    # 公式：Var(X|Y=y) = sigma_x^2 * (1 - rho^2)
    theoretical_mean = MU_X + RHO * (SIGMA_X / SIGMA_Y) * (SLICE_Y - MU_Y)
    theoretical_var = (SIGMA_X**2) * (1 - RHO**2)
    theoretical_std = np.sqrt(theoretical_var)
    
    print(f"理论推导 -> 条件均值: {theoretical_mean:.4f}, 条件标准差: {theoretical_std:.4f}")
    print(f"模拟统计 -> 样本均值: {np.mean(X_given_Y_samples):.4f}, 样本标准差: {np.std(X_given_Y_samples):.4f}")

    # 4. 绘图可视化
    plt.figure(figsize=(12, 5))
    
    # 子图1：整体视角的散点图
    plt.subplot(1, 2, 1)
    # 为了绘图速度，如果点太多，只画前 2000 个背景点
    plt.scatter(X_samples[:2000], Y_samples[:2000], alpha=0.1, color='gray', label='整体分布 (背景)')
    # 高亮显示切片内的点
    plt.scatter(X_given_Y_samples, Y_samples[condition_indices], alpha=0.5, color='red', s=10, label=f'切片数据 (Y ≈ {SLICE_Y})')
    plt.axhline(SLICE_Y, color='blue', linestyle='--', label='切刀位置')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'二元正态分布与切片位置 (rho={RHO})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 子图2：切片内 X 的分布 vs 理论正态分布
    plt.subplot(1, 2, 2)
    
    # 绘制直方图 (模拟结果)
    count, bins, ignored = plt.hist(X_given_Y_samples, bins=30, density=True, 
                                    alpha=0.6, color='red', label='模拟切片直方图')
    
    # 绘制理论曲线 (数学推导)
    x_axis = np.linspace(theoretical_mean - 4*theoretical_std, theoretical_mean + 4*theoretical_std, 100)
    plt.plot(x_axis, norm.pdf(x_axis, theoretical_mean, theoretical_std), 
             color='black', linewidth=2, linestyle='--', label='理论条件分布 N(μ_cond, σ_cond)')
    
    plt.xlabel(f'X | Y={SLICE_Y}')
    plt.ylabel('Density')
    plt.title('验证：切片后 X 的分布是否仍为正态？')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()