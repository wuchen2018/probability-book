"""
文件名: continuous_pdf_integration_demo.py
功能: 可视化概率密度函数(PDF)的面积积分与实际随机事件频率的等价关系

【这是什么？】
连续型随机变量的概率无法通过“单点求和”来计算，必须通过求概率密度函数在某一段区间上的积分（即面积）来获得。这段代码利用标准正态分布，在数学理论（微积分）与实际统计（蒙特卡洛模拟）之间建立直观的联系。

【怎么用？】
直接运行脚本。程序将弹出一张对比图，并在控制台输出数学积分计算出的“理论概率”与通过海量随机实验统计出的“实际频率”。建议修改参数区中的样本数量或目标区间，观察大数定律下频率向概率面积收敛的奇妙过程。
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# ---------------------------------------------------------
# # --- 可调整参数配置区 ---
# ---------------------------------------------------------
# 1. 模拟实验的抛撒次数（建议尝试 1000, 10000, 1000000）
NUM_SAMPLES = 100000 

# 2. 直方图的切片数量（切得越细，越接近连续的“微元”）
BIN_COUNT = 100 

# 3. 想要计算概率的目标区间 [a, b]，即 P(a < X < b)
TARGET_RANGE = (-1.0, 1.0) 
# ---------------------------------------------------------

# 设置中文字体，防止控制台或图表出现乱码（优先尝试黑体）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 步骤 1：理论准备（微积分视角）
    # 创建连续的 x 轴坐标点，用于绘制理论上的概率密度函数（PDF）曲线
    x_theoretical = np.linspace(-4, 4, 1000)
    
    # 获取标准正态分布 N(0,1) 在这些 x 点上的概率密度值 f(x)
    # 注意：这里的 y_theoretical 是密度（浓度），而不是概率。它的值域可以大于1（虽然标准正态最高约0.4）。
    y_theoretical = stats.norm.pdf(x_theoretical, loc=0, scale=1)

    # 步骤 2：实验模拟（统计学视角）
    # 生成海量的符合标准正态分布的随机数，模拟现实中收集到的连续型数据
    experiment_data = np.random.normal(loc=0, scale=1, size=NUM_SAMPLES)

    # 步骤 3：数据验证与输出
    # 数学理论值计算：利用累积分布函数(CDF)计算区间内的面积。F(b) - F(a) = \int_a^b f(x)dx
    a, b = TARGET_RANGE
    theoretical_prob = stats.norm.cdf(b) - stats.norm.cdf(a)
    
    # 实际统计值计算：数一数有多少个随机数正好落在了 [a, b] 区间内，除以总数得到频率
    count_in_range = np.sum((experiment_data >= a) & (experiment_data <= b))
    empirical_freq = count_in_range / NUM_SAMPLES

    print(f"=== 连续型变量：概率面积与实际频率对比 ===")
    print(f"目标区间: P({a} < X < {b})")
    print(f"理论概率 (微积分面积): {theoretical_prob:.4%}")
    print(f"实际频率 ({NUM_SAMPLES}次实验): {empirical_freq:.4%}")
    print(f"绝对误差: {abs(theoretical_prob - empirical_freq):.4%}\n")

    # 步骤 4：绘图可视化
    plt.figure(figsize=(10, 6))

    # 绘制实验结果直方图
    # 核心数学对应：density=True 参数极其关键！
    # 它强行把原本统计个数的 Y 轴，除以了“总样本数 * 区间宽度”。
    # 这样直方图的总面积才会被强制归一化为 1，从而真正与理论的“概率密度”处于同一量纲。
    plt.hist(experiment_data, bins=BIN_COUNT, density=True, alpha=0.5, color='gray', edgecolor='white', label='实际数据分布 (归一化直方图)')

    # 绘制理论上的概率密度曲线 f(x)
    plt.plot(x_theoretical, y_theoretical, color='red', linewidth=2.5, label='理论概率密度函数 (PDF)')

    # 填充目标区间 [a, b] 的积分面积
    # 这部分面积在数学上严格等于 P(a < X < b)
    x_fill = np.linspace(a, b, 200)
    y_fill = stats.norm.pdf(x_fill, loc=0, scale=1)
    plt.fill_between(x_fill, 0, y_fill, color='blue', alpha=0.3, label=f'目标区间积分面积 ({theoretical_prob:.1%})')

    plt.title("微积分的曲线面积 vs 海量随机事件的统计结果", fontsize=14)
    plt.xlabel("随机变量 X 的取值", fontsize=12)
    plt.ylabel("概率密度 f(x)", fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.show()

if __name__ == "__main__":
    main()