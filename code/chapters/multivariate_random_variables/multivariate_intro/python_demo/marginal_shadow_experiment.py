"""
文件名: marginal_shadow_experiment.py
功能: 模拟联合分布到边际分布的“投影”过程，演示相关性是如何在边际化中丢失的。

【这是什么？】
这段代码通过生成两组随机数据（一组独立，一组高度相关），展示了“联合分布”与“边际分布”的关系。
它直观地演示了核心数学概念：边际分布仅仅是联合分布在某个坐标轴上的“影子”或“投影”。
你将看到，即使两组数据的内部结构（联合分布）天差地别，它们的影子（边际分布）却可以完全一样。

【怎么用？】
直接运行即可。
程序会弹出一个对比图：
1. 左边是两个独立的变量。
2. 右边是两个高度纠缠（相关）的变量。
请注意观察：虽然中间的散点图形状完全不同，但上方和右侧的直方图（影子）是否惊人地相似？
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# --- 可调整参数配置区 ---
# 样本数量：样本越多，直方图越接近理论的光滑曲线
N_SAMPLES = 5000  

# 相关系数：控制右侧图中 X 和 Y 的纠缠程度 (范围 -1 到 1)
# 尝试改为 0.9 (极度正相关) 或 -0.8 (负相关) 看看影子的变化
CORRELATION = 0.8  

# 直方图的柱子数量：决定了“影子”的精细程度
BIN_COUNT = 40    

# 随机种子：保证每次运行结果一致（可以注释掉以获得随机结果）
np.random.seed(42) 

def generate_data(corr_coeff, n):
    """
    生成二元正态分布数据。
    这里对应数学上的：从联合密度函数 f(x,y) 中进行采样。
    """
    mean = [0, 0] # X和Y的均值都是0
    # 协方差矩阵：对角线是方差(1)，非对角线是协方差(即相关系数，因为方差为1)
    cov = [[1, corr_coeff], 
           [corr_coeff, 1]] 
    return np.random.multivariate_normal(mean, cov, n)

def plot_joint_marginal(ax_main, ax_top, ax_right, data, title):
    """
    绘制联合分布（散点）和边际分布（直方图）
    """
    x, y = data[:, 0], data[:, 1]
    
    # 1. 绘制中心散点图 -> 对应“联合分布”
    # 每一个点代表一次实验结果 (x, y)，所有点的集合构成了联合分布的形状
    ax_main.scatter(x, y, alpha=0.3, s=2, color='#1F77B4')
    ax_main.set_xlim(-4, 4)
    ax_main.set_ylim(-4, 4)
    ax_main.text(0, -3.5, title, ha='center', fontweight='bold')
    ax_main.grid(True, linestyle=':', alpha=0.6)

    # 2. 绘制上方直方图 -> 对应 X 的“边际分布”
    # 数学含义：这就是对 Y 进行“积分”或“求和”的过程。
    # 我们不再关心 Y 具体是多少，只是把所有落在 X 区间内的点堆起来。
    ax_top.hist(x, bins=BIN_COUNT, color='#1F77B4', alpha=0.7, density=True)
    ax_top.set_xlim(-4, 4)
    ax_top.axis('off') # 隐藏坐标轴，更像“影子”
    ax_top.set_title("Marginal X (Shadow)", fontsize=10, color='#555555')

    # 3. 绘制右侧直方图 -> 对应 Y 的“边际分布”
    # 数学含义：同理，这是对 X 进行“积分”的过程。
    # orientation='horizontal' 让直方图横过来，模拟光照到右墙上的影子。
    ax_right.hist(y, bins=BIN_COUNT, orientation='horizontal', color='#1F77B4', alpha=0.7, density=True)
    ax_right.set_ylim(-4, 4)
    ax_right.axis('off')
    ax_right.text(0.1, 0, "Marginal Y", rotation=270, va='center', fontsize=10, color='#555555')

def run_experiment():
    # 生成两组数据
    # 第一组：独立 (相关系数 = 0)
    data_independent = generate_data(0, N_SAMPLES)
    # 第二组：相关 (相关系数 = CORRELATION)
    data_correlated = generate_data(CORRELATION, N_SAMPLES)

    # 设置画布布局
    fig = plt.figure(figsize=(12, 6))
    
    # 使用 GridSpec 将画布分为左右两部分，每部分再细分为中间、上、右
    gs = GridSpec(4, 8, figure=fig, wspace=0.6, hspace=0.6)

    # --- 左图：独立情况 ---
    ax_joint_1 = fig.add_subplot(gs[1:4, 0:3])
    ax_marg_x_1 = fig.add_subplot(gs[0, 0:3], sharex=ax_joint_1)
    ax_marg_y_1 = fig.add_subplot(gs[1:4, 3], sharey=ax_joint_1)
    
    plot_joint_marginal(ax_joint_1, ax_marg_x_1, ax_marg_y_1, 
                        data_independent, f"Independent (Corr=0)")

    # --- 右图：相关情况 ---
    ax_joint_2 = fig.add_subplot(gs[1:4, 4:7])
    ax_marg_x_2 = fig.add_subplot(gs[0, 4:7], sharex=ax_joint_2)
    ax_marg_y_2 = fig.add_subplot(gs[1:4, 7], sharey=ax_joint_2)

    plot_joint_marginal(ax_joint_2, ax_marg_x_2, ax_marg_y_2, 
                        data_correlated, f"Correlated (Corr={CORRELATION})")

    plt.suptitle(f"The Illusion of Shadows: Same Marginals, Different Joints\n(N={N_SAMPLES})", fontsize=14)
    plt.show()

if __name__ == "__main__":
    run_experiment()