"""
文件名: distribution_profiler_demo.py
功能: 模拟并对比正态分布与偏态/厚尾分布的各项特征数差异

【这是什么？】
这段代码在计算机里凭空捏造了两组数据：一组是绝对对称、规规矩矩的“正态数据”，另一组是充满极端值、拖着长长尾巴的“偏态数据”。它计算了这两组数据的所有特征数（期望、方差、偏度、峰度、中位数等），并把它们画在一起。

【怎么用？】
直接运行脚本。控制台会输出两组数据的特征数对比报告，同时弹出一张可视化图表。你可以通过修改“参数配置区”里的数值，观察极端数据是如何把均值“拽”走，又是如何让峰度飙升的。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- 可调整参数配置区 ---
SAMPLE_SIZE = 100000       # 生成的样本数量（数据量越大，计算出的特征数越逼近理论真实值）
LOGNORMAL_SIGMA = 1.2      # 偏态分布的形状参数（你可以尝试调大到 2.0，看看偏度和峰度会怎样爆炸）
BINS = 100                 # 直方图的柱子数量

# 为了让中文正常显示，配置 matplotlib 字体
plt.rcParams['font.sans-serif'] = ['SimSun', 'SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False 

def analyze_and_plot(data, ax, title):
    # --- 数学特征数计算区 ---
    
    # 1. 一阶原点矩：期望（质心的位置）
    mean_val = np.mean(data)
    
    # 2. 分位数：中位数（概率的物理中点，不受极端值影响）
    median_val = np.median(data)
    
    # 3. 寻找众数（概率密度最高点，由于是连续数据，我们用核密度估计来寻找最高峰）
    kde = stats.gaussian_kde(data)
    x_range = np.linspace(min(data), max(data), 1000)
    mode_val = x_range[np.argmax(kde(x_range))]
    
    # 4. 二阶中心矩：方差与标准差（衡量偏离重心的绝对惯性）
    std_val = np.std(data, ddof=1) 
    
    # 5. 变异系数 CV：相对波动（标准差除以均值，消除量纲）
    cv_val = std_val / np.abs(mean_val)
    
    # 6. 标准化三阶中心矩：偏度（正值代表右尾长，负值代表左尾长）
    skewness_val = stats.skew(data)
    
    # 7. 标准化四阶中心矩：超额峰度（衡量尾部极端事件的发生概率，>0代表厚尾）
    # 注意：scipy.stats.kurtosis 默认计算的就是减去3之后的“超额峰度”(fisher=True)
    kurtosis_val = stats.kurtosis(data, fisher=True)

    # --- 打印体检报告 ---
    print(f"=== {title} ===")
    print(f"均值 (期望) : {mean_val:.2f}")
    print(f"中位数      : {median_val:.2f}")
    print(f"众数 (估计) : {mode_val:.2f}")
    print(f"标准差      : {std_val:.2f}")
    print(f"变异系数(CV): {cv_val:.2f}")
    print(f"偏度        : {skewness_val:.2f}")
    print(f"超额峰度    : {kurtosis_val:.2f}\n")

    # --- 绘图可视化区 ---
    # 截断极端的尾巴以便于画图（只展示99%的数据范围）
    clip_max = np.percentile(data, 99)
    plot_data = data[data <= clip_max]
    
    ax.hist(plot_data, bins=BINS, density=True, alpha=0.5, color='#1F77B4')
    ax.set_title(title)
    
    # 画出特征数的位置
    ax.axvline(mean_val, color='red', linestyle='-', lw=1.5, label=f'均值 (Mean)')
    ax.axvline(median_val, color='green', linestyle='--', lw=1.5, label=f'中位数 (Median)')
    ax.axvline(mode_val, color='black', linestyle=':', lw=1.5, label=f'众数 (Mode)')
    
    ax.legend()
    ax.set_yticks([]) # 隐藏不直观的密度y轴刻度

if __name__ == "__main__":
    print("正在生成数据并计算特征数，请稍候...\n")
    
    # 1. 生成标准的正态分布数据 (钟形曲线，极其对称)
    normal_data = np.random.normal(loc=100, scale=15, size=SAMPLE_SIZE)
    
    # 2. 生成对数正态分布数据 (典型的右偏、厚尾数据，常用于模拟财富、自然灾害损失等)
    # 我们故意将其缩放，使其众数与正态分布相近，以便对比尾巴的威力
    lognormal_data = np.random.lognormal(mean=np.log(100), sigma=LOGNORMAL_SIGMA, size=SAMPLE_SIZE)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    analyze_and_plot(normal_data, ax1, "理想世界：正态分布 (对称、薄尾)")
    analyze_and_plot(lognormal_data, ax2, "现实世界：偏态分布 (右偏、厚尾)")
    
    plt.tight_layout()
    plt.show()