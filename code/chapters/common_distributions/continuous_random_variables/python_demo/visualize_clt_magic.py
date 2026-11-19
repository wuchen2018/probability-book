"""
文件名: visualize_clt_magic.py
功能: 模拟中心极限定理（CLT）的收敛过程，展示“秩序如何从混乱中涌现”

【这是什么？】
这段代码带你亲眼见证概率论中最神奇的魔法：
无论原始数据长得多么“奇怪”（比如完全平坦的均匀分布），
只要你把它们随机抽取并取平均值，这些“平均值”的分布就会不可阻挡地变成一口标准的“钟（正态分布）”。

【怎么用？】
1. 直接运行代码，你会看到两个图：原始分布的形状 vs 样本均值的形状。
2. 尝试修改【参数配置区】里的 `SAMPLE_SIZE`（比如改为 2, 5, 30），
   观察随着样本量增加，那个“钟”是如何变得越来越完美的。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 可调整参数配置区 (建议修改这里来观察变化) ---

# 1. 样本容量 (n)：每次实验我们抓取多少个数据来取平均？
# 尝试改为 1 (完全混乱), 2 (三角形状), 5 (有点像钟), 30 (完美的钟)
SAMPLE_SIZE = 30  

# 2. 实验次数：我们需要重复多少次实验来画出统计直方图？
# 次数越多，直方图越平滑，越接近理论曲线
NUM_EXPERIMENTS = 10000  

# 3. 原始分布的范围：这里我们使用均匀分布（即所有数出现的概率一样，长得像个矩形砖块）
LOW_BOUND = 0
HIGH_BOUND = 100

# ------------------------------------------------

def run_clt_simulation():
    # 设置绘图风格，支持中文显示（如果系统有对应字体，否则回退到默认）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False
    
    print(f"正在进行 {NUM_EXPERIMENTS} 次实验，每次抽取 {SAMPLE_SIZE} 个样本...")

    # Step 1: 生成“混乱”的原始数据
    # 创建一个矩阵：行数=实验次数，列数=每次抽取的样本数
    # 这里模拟的是均匀分布（Uniform Distribution），它的形状是平顶的，完全不像钟形
    raw_data = np.random.uniform(LOW_BOUND, HIGH_BOUND, (NUM_EXPERIMENTS, SAMPLE_SIZE))

    # Step 2: 见证奇迹的时刻——计算“样本均值”
    # 我们对每一行（每一次实验）的数据求平均值
    # 根据中心极限定理，虽然 raw_data 是均匀分布，但 sample_means 应该接近正态分布
    sample_means = np.mean(raw_data, axis=1)

    # Step 3: 计算理论上的正态分布参数（用于对比验证）
    # 原始均匀分布的均值 (mu)
    true_mu = 0.5 * (LOW_BOUND + HIGH_BOUND)
    # 原始均匀分布的方差 (sigma^2) = (b-a)^2 / 12
    true_variance = (HIGH_BOUND - LOW_BOUND)**2 / 12
    true_sigma = np.sqrt(true_variance)

    # 理论上，样本均值的标准差 (Standard Error) = 原始标准差 / sqrt(n)
    clt_sigma = true_sigma / np.sqrt(SAMPLE_SIZE)

    # --- 开始绘图 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 子图1：展示原始分布（一次抽样的样子）
    # 这里我们只画出前1000个数据点，展示原始数据的“平坦”特性
    ax1.hist(raw_data.flatten()[:10000], bins=30, density=True, color='#BDC3C7', edgecolor='white')
    ax1.set_title(f"原始世界：均匀分布 (n=1)\n(混乱、平坦、无中心)", fontsize=12)
    ax1.set_xlabel("数值")
    ax1.set_ylabel("概率密度")

    # 子图2：展示样本均值的分布（CLT的结果）
    # 绘制实验得到的均值直方图
    count, bins, ignored = ax2.hist(sample_means, bins=50, density=True, 
                                    color='#3498DB', alpha=0.8, label='实验模拟结果')
    
    # 绘制理论上的正态分布曲线（红色线条）
    # 观察直方图是否完美贴合这条红线
    x_axis = np.linspace(min(bins), max(bins), 100)
    pdf_curve = norm.pdf(x_axis, true_mu, clt_sigma)
    ax2.plot(x_axis, pdf_curve, linewidth=3, color='#E74C3C', label='理论正态曲线')

    ax2.set_title(f"新世界：样本均值的分布 (n={SAMPLE_SIZE})\n(秩序涌现，完美的钟形)", fontsize=12)
    ax2.set_xlabel("样本均值")
    ax2.legend()

    plt.tight_layout()
    print("绘图完成！请查看弹出的窗口。")
    plt.show()

if __name__ == "__main__":
    run_clt_simulation()