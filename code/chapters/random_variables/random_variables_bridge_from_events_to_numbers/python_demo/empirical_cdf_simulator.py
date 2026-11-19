"""
文件名: empirical_cdf_simulator.py
功能: 模拟随机数据的经验分布函数 (ECDF) 并与理论分布函数进行对比

【这是什么？】
分布函数 F(x) = P(X <= x) 的概念非常抽象。这段代码通过计算机“扔骰子”生成真实的随机数，
然后像查户口一样统计“小于等于某个刻度 x 的数据占总数的比例”（这被称为经验分布函数）。
你会直观地看到：随着数据量的不断增加，现实中杂乱的统计阶梯，最终会完美贴合数学推导出的理论曲线。

【怎么用？】
直接运行脚本即可。强烈建议你修改下方配置区的“模拟数据量 (SAMPLE_SIZE)”。
先设为 10 看一眼粗糙的折线，再设为 10000，你会惊叹于现实世界向数学秩序靠拢的力量。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- 可调整参数配置区 ---
SAMPLE_SIZE = 50          # 模拟生成的随机数据个数（请尝试将其修改为 10，然后修改为 10000）
DISTRIBUTION_TYPE = 'norm' # 可选：'norm' (连续型：正态分布) 或 'binom' (离散型：二项分布)

# 二项分布专属参数（如果选了 'binom' 才生效）
BINOM_N = 10              # 实验次数
BINOM_P = 0.5             # 成功概率

# 图表外观配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Arial Unicode MS'] # 兼容多平台的中文显示
plt.rcParams['axes.unicode_minus'] = False
# ------------------------

def main():
    # ==========================================
    # 第一步：模拟现实世界，收集随机数据
    # ==========================================
    if DISTRIBUTION_TYPE == 'norm':
        # 生成标准正态分布的随机数
        # 这代表现实中收集到的独立样本（比如测量误差）
        data = np.random.randn(SAMPLE_SIZE)
    elif DISTRIBUTION_TYPE == 'binom':
        # 生成二项分布的随机数
        # 这代表现实中做了 SAMPLE_SIZE 次重复实验，每次实验包含 BINOM_N 次伯努利试验
        data = np.random.binomial(n=BINOM_N, p=BINOM_P, size=SAMPLE_SIZE)
    else:
        raise ValueError("不支持的分布类型，请检查配置区。")

    # ==========================================
    # 第二步：计算经验分布函数 (ECDF)
    # 核心数学思想：用频率近似概率，计算真实样本中 <= x 的比例
    # ==========================================
    # 将收集到的数据从小到大排好队。
    # 为什么要排队？因为分布函数是从左到右的“进度条”，我们需要顺着数轴依次推进。
    x_ecdf = np.sort(data)
    
    # 构造 Y 轴：计算累积频率。
    # 对于排好队的第 i 个数据（索引从 1 开始），说明总样本中有 i/N 的比例的数据小于等于它。
    # 这正是 F(x) = P(X <= x) 在现实统计中的直接体现。
    y_ecdf = np.arange(1, SAMPLE_SIZE + 1) / SAMPLE_SIZE

    # ==========================================
    # 第三步：获取理论上的分布函数 F(x)
    # 核心数学思想：完美的上帝视角，即微积分或严格组合数学算出的结果
    # ==========================================
    # 生成用于绘制平滑曲线的 X 轴刻度，稍微往左右延伸一点以展示全貌
    x_theory = np.linspace(data.min() - 1, data.max() + 1, 1000)
    
    if DISTRIBUTION_TYPE == 'norm':
        # 调用标准库计算正态分布的精确 CDF 值 (积分结果)
        y_theory = stats.norm.cdf(x_theory)
    elif DISTRIBUTION_TYPE == 'binom':
        # 调用标准库计算二项分布的精确 CDF 值 (累加求和结果)
        y_theory = stats.binom.cdf(x_theory, n=BINOM_N, p=BINOM_P)

    # ==========================================
    # 第四步：绘图对比（现实 vs 理论）
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # 画出现实的经验分布（阶梯图）
    # 为什么要用阶梯图（step）？因为每遇到一个样本点，进度条才会往上跳一格。
    plt.step(x_ecdf, y_ecdf, where='post', label=f'经验分布 (样本量 N={SAMPLE_SIZE})', 
             color='orange', linewidth=2, alpha=0.8)
    
    # 画出理论的分布函数
    plt.plot(x_theory, y_theory, label='理论分布函数 $F(x)$', 
             color='blue', linewidth=2, linestyle='--')

    # 添加辅助线与标记
    plt.axhline(0, color='black', linewidth=0.5, linestyle=':')
    plt.axhline(1, color='black', linewidth=0.5, linestyle=':')
    
    plt.title("分布函数的现实投射：经验分布 vs 理论分布", fontsize=14)
    plt.xlabel("随机变量的取值 x", fontsize=12)
    plt.ylabel("累积概率 P(X <= x)", fontsize=12)
    plt.ylim(-0.05, 1.05)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    main()