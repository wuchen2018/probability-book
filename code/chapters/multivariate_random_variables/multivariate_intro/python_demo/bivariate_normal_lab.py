# -*- coding: utf-8 -*-
"""
文件名: bivariate_normal_lab.py
功能: 模拟二元正态分布，展示相关系数如何控制数据的“形状”

【这是什么？】
这段代码是二元正态分布的“上帝视角”模拟器。
它能让你亲手设定两个变量（比如身高X和体重Y）的平均值、波动程度，以及它们之间的“纠缠程度”（相关系数）。
运行后，你会看到成千上万个随机样本点构成的“星云”，以及对应的概率密度等高线。

【怎么用？】
1. 修改下方【参数配置区】的数值（特别是 correlation_rho）。
2. 运行代码。
3. 观察：当 rho 接近 0 时，散点像一团圆圆的雾；当 rho 接近 1 时，散点如何被“挤压”成一条细线。
   同时请注意顶部和右侧的直方图（边缘分布），它们可能根本不会变！
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# --- 可调整参数配置区 (Config Section) ---

# 1. 定义 X (例如：身高) 的参数
mu_x = 170      # X 的均值 (期望)
sigma_x = 10    # X 的标准差 (波动幅度)

# 2. 定义 Y (例如：体重) 的参数
mu_y = 60       # Y 的均值
sigma_y = 5     # Y 的标准差

# 3. 定义 X 和 Y 的“关系” (最关键的参数！)
# 相关系数 rho，取值范围必须在 -1 到 1 之间
# 0 表示无关（圆），0.9 表示强正相关（细长椭圆），-0.9 表示强负相关
correlation_rho = 0.8  

# 4. 实验设置
sample_size = 5000  # 模拟生成的样本数量（点越多，形状越清晰）

# ------------------------------------------------

def run_simulation():
    print(f"正在生成 {sample_size} 个样本...")
    print(f"设定参数: X~N({mu_x}, {sigma_x}^2), Y~N({mu_y}, {sigma_y}^2)")
    print(f"相关系数 rho: {correlation_rho}")

    # --- 第一步：构建协方差矩阵 (Covariance Matrix) ---
    # 协方差矩阵是描述多维正态分布“形状”的 DNA。
    # 矩阵结构：
    # [  Var(X)      Cov(X,Y) ]
    # [  Cov(Y,X)    Var(Y)   ]
    # 其中 Cov(X,Y) = rho * sigma_x * sigma_y
    cov_xy = correlation_rho * sigma_x * sigma_y
    
    # 组合成 2x2 矩阵
    cov_matrix = [
        [sigma_x**2,  cov_xy     ],
        [cov_xy,      sigma_y**2 ]
    ]

    # --- 第二步：上帝掷骰子 (生成随机样本) ---
    # 利用 numpy 的多元正态分布生成器，根据我们设定的“DNA”生成数据
    rng = np.random.default_rng()
    data = rng.multivariate_normal([mu_x, mu_y], cov_matrix, sample_size)
    
    # 分离出 X 和 Y 的数据
    x_data = data[:, 0]
    y_data = data[:, 1]

    # --- 第三步：可视化 (绘制联合分布与边缘分布) ---
    # 我们使用 GridSpec 来分别画出主图（散点）和侧边图（直方图）
    fig = plt.figure(figsize=(8, 8))
    gs = GridSpec(4, 4)

    # 1. 主图：联合分布 (散点图 + 等高线)
    ax_joint = fig.add_subplot(gs[1:4, 0:3])
    
    # 绘制散点：每一个点代表一次模拟结果
    ax_joint.scatter(x_data, y_data, s=2, alpha=0.4, color='#1F77B4', label='随机样本')
    
    # 绘制理论等高线 (展示数学上的完美形状)
    # 生成网格点
    x_grid = np.linspace(mu_x - 3*sigma_x, mu_x + 3*sigma_x, 100)
    y_grid = np.linspace(mu_y - 3*sigma_y, mu_y + 3*sigma_y, 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    
    # 二元正态分布密度公式 (对应书中繁琐的指数公式)
    # 为了代码可读性，这里手动实现公式，而不是调用库
    z_score_x = (X - mu_x) / sigma_x
    z_score_y = (Y - mu_y) / sigma_y
    # 指数部分
    z = (z_score_x**2 - 2*correlation_rho*z_score_x*z_score_y + z_score_y**2)
    # 密度函数
    pdf = np.exp(-z / (2 * (1 - correlation_rho**2)))
    
    # 画出椭圆等高线
    ax_joint.contour(X, Y, pdf, levels=4, colors='black', alpha=0.6, linewidths=1.5)
    ax_joint.set_xlabel('Variable X')
    ax_joint.set_ylabel('Variable Y')
    ax_joint.grid(True, linestyle=':', alpha=0.6)
    
    # 2. 顶部图：X 的边缘分布 (直方图)
    # 这就是"投影"到 X 轴上的影子
    ax_marg_x = fig.add_subplot(gs[0, 0:3], sharex=ax_joint)
    ax_marg_x.hist(x_data, bins=50, color='gray', alpha=0.7, density=True)
    ax_marg_x.set_title(f'Joint Distribution Simulation (rho={correlation_rho})')
    ax_marg_x.axis('off') # 隐藏坐标轴，只看形状

    # 3. 右侧图：Y 的边缘分布 (直方图)
    # 这就是"投影"到 Y 轴上的影子
    ax_marg_y = fig.add_subplot(gs[1:4, 3], sharey=ax_joint)
    ax_marg_y.hist(y_data, bins=50, orientation='horizontal', color='gray', alpha=0.7, density=True)
    ax_marg_y.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_simulation()