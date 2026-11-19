# -*- coding: utf-8 -*-
"""
文件名: gamma_simulation_lab.py
功能: 模拟“累积等待时间”过程，验证伽马分布的形成机制

【这是什么？】
这段代码不仅仅是画出伽马分布的曲线，而是真实地模拟了“等待 k 个事件”的过程。
它通过生成成千上万组独立的指数分布随机数，将它们加起来，看看最终的总时间是否真的服从伽马分布。
这也是中心极限定理（CLT）的一次微观预演：你会看到随着 k 增大，分布形状如何变得越来越像钟形曲线。

【怎么用？】
1. 直接运行代码，观察控制台输出的统计数据和弹出的对比图。
2. 尝试修改“可调整参数配置区”中的 k 值（比如从 3 改为 50），观察分布形状的剧烈变化。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, norm

# ==========================================
# --- 可调整参数配置区 (建议修改这里来观察变化) ---
# ==========================================

# 形状参数 k：我们要等待的事件次数（必须是整数）
# 建议尝试：k=1 (退化为指数分布), k=5 (典型伽马), k=100 (趋近正态分布)
k_events = 5

# 率参数 lambda：事件发生的速率（每单位时间发生的次数）
# 例如：lambda=0.5 意味着平均每2分钟发生一次
lambda_rate = 0.5

# 模拟次数：我们要重复做多少次“等待k个事件”的实验？
# 数量越多，直方图越平滑，越接近理论曲线
num_simulations = 10000

# ==========================================
# --- 核心模拟逻辑 ---
# ==========================================

print(f"--- 开始模拟 ---")
print(f"目标：模拟等待 {k_events} 个事件的总时间")
print(f"速率：lambda = {lambda_rate}")
print(f"实验次数：{num_simulations} 次")

# 1. 生成基础数据：指数分布等待时间
# 我们需要生成 (num_simulations, k_events) 这么多的数据
# 每一行代表一次完整的实验（包含了 k 次独立的等待）
# scale 参数在 numpy 中是 1/lambda
wait_times_matrix = np.random.exponential(
    scale=1.0/lambda_rate, 
    size=(num_simulations, k_events)
)

# 2. 计算总时间：将 k 次等待时间相加
# 对应数学公式：T = X1 + X2 + ... + Xk
# axis=1 表示把每一行的 k 个数据加起来
total_times = np.sum(wait_times_matrix, axis=1)

# ==========================================
# --- 结果可视化与理论对比 ---
# ==========================================

# 设置画布风格
plt.figure(figsize=(10, 6), dpi=100)
plt.style.use('bmh') # 使用一种干净的背景风格

# A. 绘制实验数据的直方图 (Histogram)
#这是我们通过“笨办法”模拟出来的真实分布
count, bins, ignored = plt.hist(
    total_times, 
    bins=50, 
    density=True, 
    alpha=0.6, 
    color='#1F77B4', 
    edgecolor='white',
    label='模拟实验数据 (直方图)'
)

# B. 绘制理论伽马分布曲线 (PDF)
# 这是数学公式计算出的“完美形态”
# linspace 生成平滑的 x 轴坐标
x_axis = np.linspace(0, max(bins), 500)
# scipy 的 gamma 函数参数说明：a是形状参数(k), scale是尺度参数(1/lambda)
theoretical_pdf = gamma.pdf(x_axis, a=k_events, scale=1.0/lambda_rate)

plt.plot(
    x_axis, 
    theoretical_pdf, 
    linewidth=2.5, 
    color='#D62728', 
    label=f'理论伽马分布 PDF (k={k_events})'
)

# C. (可选) 如果 k 很大，展示正态分布近似
# 对应中心极限定理：当 k 很大时，Gamma(k, lambda) ≈ Normal(mean=k/lambda, var=k/lambda^2)
if k_events >= 10:
    mu = k_events / lambda_rate
    sigma = np.sqrt(k_events / (lambda_rate**2))
    normal_pdf = norm.pdf(x_axis, loc=mu, scale=sigma)
    plt.plot(
        x_axis, 
        normal_pdf, 
        'k--', 
        linewidth=1.5, 
        alpha=0.7,
        label='正态近似 (中心极限定理)'
    )

# --- 图表装饰 ---
plt.title(f'伽马分布模拟：等待 {k_events} 个独立事件的总时间', fontsize=12)
plt.xlabel('总等待时间 T', fontsize=10)
plt.ylabel('概率密度', fontsize=10)
plt.legend()
plt.grid(True, alpha=0.3)

# --- 打印统计数据对比 ---
theory_mean = k_events / lambda_rate
theory_var = k_events / (lambda_rate**2)
sim_mean = np.mean(total_times)
sim_var = np.var(total_times)

print(f"\n--- 结果验证 ---")
print(f"理论期望 E(T) = {theory_mean:.2f}  vs  模拟均值 = {sim_mean:.2f}")
print(f"理论方差 Var(T)= {theory_var:.2f}  vs  模拟方差 = {sim_var:.2f}")

plt.show()