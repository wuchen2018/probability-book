"""
文件名: uncorrelated_but_dependent_sim.py
功能: 验证存在确定的非线性关系时，线性相关系数可能为0

【这是什么？】
这段代码通过蒙特卡洛模拟，生成一对具有绝对函数关系（如 Y = X^2）的随机变量。
它通过计算海量样本的协方差和皮尔逊相关系数，以此验证“不相关仅仅代表没有直线关系，绝不代表独立”这一核心数学事实。

【怎么用？】
直接运行脚本。控制台会输出实际模拟计算出的协方差和相关系数。
同时会弹出一张散点图，直观展示即使数据呈现完美的对称曲线规律，其线性相关系数依然极其逼近于 0。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
SAMPLE_SIZE = 100000        # 模拟的样本数量（你可以尝试改为 100 或 1000000 观察大数定律的效果）
X_MIN = -1.0                # 均匀分布的下界
X_MAX = 1.0                 # 均匀分布的上界
POWER_EXPONENT = 2          # 多项式的次数（可以尝试修改为 4，或者改成绝对值函数测试）

# 为了兼容中文显示，尝试加载系统常见中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False 

def main():
    # 1. 生成随机变量 X 的样本
    # 对应数学概念：X ~ U(a, b)，这里是在指定区间内进行均匀抽样
    x = np.random.uniform(X_MIN, X_MAX, SAMPLE_SIZE)
    
    # 2. 生成随机变量 Y 的样本
    # 对应数学概念：构建确定性的非线性依赖关系 Y = X^2
    # 注意：此时给定一个 X，Y 的值是 100% 确定的，它们绝对不独立
    y = np.power(x, POWER_EXPONENT)
    
    # 3. 计算样本协方差 (Covariance)
    # 对应数学公式：Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
    # np.cov 返回的是协方差矩阵，索引 [0, 1] 即为 X 和 Y 的协方差
    cov_matrix = np.cov(x, y)
    covariance = cov_matrix[0, 1]
    
    # 4. 计算皮尔逊线性相关系数 (Pearson Correlation Coefficient)
    # 对应数学公式：rho = Cov(X, Y) / (Std(X) * Std(Y))
    # 它是将协方差进行了标准化，去除了量纲的影响，范围被压缩到 [-1, 1] 之间
    corr_matrix = np.corrcoef(x, y)
    correlation = corr_matrix[0, 1]
    
    # --- 打印数值结果 ---
    print(f"--- 模拟结果 (样本量: {SAMPLE_SIZE}) ---")
    print(f"X 和 Y 的协方差: {covariance:.6f}")
    print(f"X 和 Y 的线性相关系数: {correlation:.6f}")
    print("结论：相关系数极度逼近于 0，但变量之间存在绝对的函数依赖。")
    
    # --- 可视化 ---
    # 抽取少量样本用于绘图（海量散点会糊成一团，失去直观性）
    plot_samples = min(SAMPLE_SIZE, 500)
    x_plot = x[:plot_samples]
    y_plot = y[:plot_samples]
    
    plt.figure(figsize=(7, 5))
    # 绘制散点，展示联合分布的真实几何形态
    plt.scatter(x_plot, y_plot, alpha=0.6, edgecolors='w', label=f'散点 (Y = X^{POWER_EXPONENT})')
    
    # 利用最小二乘法拟合一条直线，展示“线性相关系数为0”的几何意义
    # np.polyfit(..., 1) 对应寻找一条 y = kx + b 的最优拟合直线
    k, b = np.polyfit(x_plot, y_plot, 1)
    plt.plot(x_plot, k * x_plot + b, color='red', linewidth=2, 
             label=f'最佳线性拟合线 (斜率k ≈ {k:.4f})')
    
    plt.title(f"非线性依赖与线性相关系数\n(样本量: {SAMPLE_SIZE}, 相关系数 $\\rho \\approx {correlation:.4f}$)")
    plt.xlabel("随机变量 X")
    plt.ylabel("随机变量 Y")
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    main()