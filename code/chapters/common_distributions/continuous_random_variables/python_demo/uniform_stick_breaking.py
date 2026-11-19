"""
文件名: uniform_stick_breaking.py
功能: 模拟“剪绳子”实验：验证均匀分布的极值（最大值/最小值）规律

【这是什么？】
这段代码通过计算机模拟“在 0 到 1 之间随机撒 n 个点”的过程。
它可以直观地展示：为什么点多了以后，最小值的平均位置会变成 1/(n+1)。
你会看到通过成千上万次实验统计出来的“真实分布”，和数学推导出的理论曲线完美重合。

【怎么用？】
直接运行即可。
你可以修改 N_POINTS (撒点的数量) 看分布形状如何变化。
程序会画出直方图，并在控制台输出理论值与模拟值的对比。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
N_POINTS = 3        # 每次撒点的数量 (即数学公式中的 n)
N_TRIALS = 50000    # 模拟实验的次数 (次数越多，柱状图越接近理论曲线)
# ---------------------

def run_simulation():
    # 设置中文字体，防止绘图乱码
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
    plt.rcParams['axes.unicode_minus'] = False

    print(f"开始模拟... 正在进行 {N_TRIALS} 次实验，每次撒 {N_POINTS} 个点。")
    
    # 1. 核心模拟：生成均匀分布随机数
    # 对应数学原理：X ~ U(0, 1)
    # data 的形状是 (N_TRIALS, N_POINTS)，每一行代表一次独立的实验（一次剪绳子）
    data = np.random.uniform(0, 1, size=(N_TRIALS, N_POINTS))
    
    # 2. 提取统计量
    # 对应数学概念：最小值统计量 L = min(X1, ..., Xn)
    min_vals = np.min(data, axis=1)
    
    # 对应数学概念：最大值统计量 M = max(X1, ..., Xn)
    max_vals = np.max(data, axis=1)
    
    # 3. 计算期望验证
    # 理论期望：E[L] = 1/(n+1)
    theo_mean_min = 1 / (N_POINTS + 1)
    # 模拟期望：对所有实验结果求算术平均 (大数定律)
    sim_mean_min = np.mean(min_vals)
    
    print(f"\n--- 结果验证 (n={N_POINTS}) ---")
    print(f"最小值的理论期望 (1/(n+1)): {theo_mean_min:.4f}")
    print(f"最小值的模拟均值 (实测数据): {sim_mean_min:.4f}")
    print(f"误差: {abs(theo_mean_min - sim_mean_min):.4f}")
    
    # 4. 绘图可视化
    plt.figure(figsize=(12, 5))
    
    # --- 子图1：最小值的分布 ---
    plt.subplot(1, 2, 1)
    # 画直方图 (频率分布)，这就代表了"真实发生"的概率
    plt.hist(min_vals, bins=50, density=True, alpha=0.6, color='#1F77B4', label='模拟实验数据')
    
    # 画理论曲线 (PDF)
    # 对应数学公式：f_min(x) = n * (1-x)^(n-1)
    # 解释：这是累积分布函数 F(x) = 1 - (1-x)^n 求导后的结果
    x = np.linspace(0, 1, 1000)
    pdf_min = N_POINTS * (1 - x)**(N_POINTS - 1)
    
    plt.plot(x, pdf_min, 'r-', lw=2, label='理论密度曲线')
    plt.title(f'最小值 (Min) 的分布 (n={N_POINTS})')
    plt.xlabel('数值')
    plt.ylabel('概率密度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # --- 子图2：最大值的分布 ---
    plt.subplot(1, 2, 2)
    # 画直方图
    plt.hist(max_vals, bins=50, density=True, alpha=0.6, color='#2CA02C', label='模拟实验数据')
    
    # 画理论曲线 (PDF)
    # 对应数学公式：f_max(x) = n * x^(n-1)
    # 解释：这是累积分布函数 F(x) = x^n 求导后的结果
    pdf_max = N_POINTS * x**(N_POINTS - 1)
    
    plt.plot(x, pdf_max, 'r-', lw=2, label='理论密度曲线')
    plt.title(f'最大值 (Max) 的分布 (n={N_POINTS})')
    plt.xlabel('数值')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()