"""
文件名: ecdf_convergence_demo.py
功能: 演示经验分布函数(ECDF)如何随着样本量的增加，逐渐逼近总体的真实分布函数(CDF)。

【这是什么？】
我们在统计中只能看到“样本”，看不到“总体”。
这段代码模拟了开启“上帝视角”的过程：我们知道电池寿命服从正态分布（总体），
然后观察当我们抽取 10 个、50 个、1000 个电池时，
我们画出的“经验阶梯线”是不是越来越像那个光滑的“理论曲线”。

【怎么用？】
直接运行即可。你将看到三张图，分别代表小样本、中样本和大样本下的拟合情况。
尝试修改“配置区”里的参数，看看如果方差变大，需要多少样本才能看清真相？
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 可调整参数配置区 ---
TRUE_MU = 100       # 总体均值（例如：电池平均寿命 100 小时）
TRUE_SIGMA = 5      # 总体标准差（例如：波动范围）
SAMPLE_SIZES = [10, 50, 1000]  # 我们要模拟的三种抽样规模
RANDOM_SEED = 42    # 随机种子，保证每次运行结果一致（可以修改它看看不同的运气）

# -----------------------

def calculate_ecdf(data):
    """
    手动计算经验分布函数 (ECDF) 的坐标点。
    数学原理：F_n(x) = (小于等于 x 的样本个数) / n
    """
    n = len(data)
    x = np.sort(data) # 必须对观测值进行排序，这是计算累积频率的前提
    y = np.arange(1, n + 1) / n # 生成 1/n, 2/n, ..., 1 的累积概率序列
    return x, y

def run_simulation():
    # 设置绘图风格
    plt.style.use('bmh')
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    
    # 准备绘制“总体真值”的光滑曲线（用于对比的标尺）
    # 在 均值 ± 4倍标准差 的范围内生成理论曲线
    x_theory = np.linspace(TRUE_MU - 4*TRUE_SIGMA, TRUE_MU + 4*TRUE_SIGMA, 1000)
    y_theory = norm.cdf(x_theory, TRUE_MU, TRUE_SIGMA)

    print(f"开始模拟：总体分布为 N({TRUE_MU}, {TRUE_SIGMA}^2)")

    for i, n in enumerate(SAMPLE_SIZES):
        ax = axes[i]
        
        # 1. 上帝视角：从总体中“随机”抽取 n 个样本
        # 对应数学概念：X1, ..., Xn ~ i.i.d. N(mu, sigma^2)
        sample_data = np.random.normal(TRUE_MU, TRUE_SIGMA, n)
        
        # 2. 凡人视角：计算经验分布函数 (ECDF)
        # 对应数学概念：构造统计量 F_n(x)
        x_ecdf, y_ecdf = calculate_ecdf(sample_data)
        
        # 3. 绘制“总体”的理论曲线（虚线，代表我们想寻找的真理）
        ax.plot(x_theory, y_theory, 'r--', linewidth=2, label='总体真实分布 (CDF)', alpha=0.6)
        
        # 4. 绘制“样本”的经验曲线（阶梯实线，代表我们手中的数据）
        # 使用 step 函数绘制阶梯图，where='post' 表示在点之后跳跃
        ax.step(x_ecdf, y_ecdf, where='post', label=f'样本经验分布 (ECDF)\nn={n}', linewidth=2.5)
        
        # 装饰图表
        ax.set_title(f'样本量 n = {n}', fontsize=14)
        ax.set_xlabel('观测数值 (x)', fontsize=12)
        if i == 0:
            ax.set_ylabel('累积概率 F(x)', fontsize=12)
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)
        
        # 计算并展示一个简单的误差指标（最大垂直距离，即 KS 统计量的直观概念）
        # 这里的计算是简化的，仅用于教学展示差异
        # 选取几个关键点比较
        diffs = []
        for check_x in [TRUE_MU, TRUE_MU + TRUE_SIGMA]:
            # 理论概率
            prob_true = norm.cdf(check_x, TRUE_MU, TRUE_SIGMA)
            # 样本频率 (小于等于 check_x 的比例)
            prob_sample = np.mean(sample_data <= check_x)
            diffs.append(abs(prob_true - prob_sample))
        max_diff = max(diffs)
        
        print(f"样本量 n={n:4d} | 在关键点的最大误差约为: {max_diff:.4f}")

    plt.suptitle('大数定律的视觉化：随着 n 增大，阶梯线 (ECDF) 逐渐与光滑线 (CDF) 重合', fontsize=16, y=1.05)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_simulation()