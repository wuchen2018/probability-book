# -*- coding: utf-8 -*-
"""
文件名: inverse_transform_magic.py
功能: 验证“逆变换采样法”——如何利用均匀分布生成指数分布

【这是什么？】
计算机通常只能生成 0 到 1 之间的均匀随机数（就像扔一把有无数个面的骰子）。
这段代码演示了如何利用一个简单的数学公式（对数变换），将这些“平平无奇”的均匀随机数，
“扭曲”成符合特定规律的指数分布随机数。这就好比把一块平整的橡皮泥（均匀分布），
捏成了滑梯的形状（指数分布）。

【怎么用？】
直接运行即可。
1. 程序会生成 N 个均匀分布的随机数。
2.通过公式 Y = -ln(U) / lambda 进行变换。
3. 画出变换后数据的直方图，并与理论上的指数分布曲线对比。
如果两者重合，说明我们的“造假”成功了！
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 想要生成的样本数量（样本越多，直方图越接近理论曲线）
N_SAMPLES = 100000

# 指数分布的参数 lambda（lambda越大，曲线下降越快，意味着事件发生得越频繁）
LAMBDA = 2.0

# 直方图的柱子数量（分得越细，细节越清楚，但如果样本太少会显得锯齿严重）
BINS = 100

# --- 核心代码区 ---

def run_simulation():
    # 1. 制造“原材料”：生成标准均匀分布 U ~ Uniform(0, 1)
    # 对应数学原理：F_Y(Y) 服从均匀分布。我们从这里反向出发。
    u_data = np.random.uniform(0, 1, N_SAMPLES)
    
    # 2. 施加“魔法”：使用逆变换公式进行映射
    # 数学推导回顾：
    # 指数分布 CDF: F(y) = 1 - e^(-lambda * y) = u
    # 反解 y: 1 - u = e^(-lambda * y)  --->  ln(1-u) = -lambda * y
    # y = -ln(1-u) / lambda
    # 或者是 y = -ln(u) / lambda （因为 1-u 和 u 在 (0,1) 上分布律是一样的）
    # 这里这行代码就是所谓“雅可比行列式”在计算机里的具体执行过程。
    y_data = -np.log(1 - u_data) / LAMBDA
    
    # --- 绘图验证区 ---
    
    # 设置字体以支持中文显示 (尝试加载通用中文字体)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

    plt.figure(figsize=(10, 6))
    
    # 绘制实验数据的直方图
    # density=True 表示将频数归一化为概率密度，这样才能和理论曲线对比
    plt.hist(y_data, bins=BINS, density=True, alpha=0.6, color='skyblue', label='模拟生成的随机数 (直方图)')
    
    # 绘制理论上的指数分布密度函数曲线 f(y) = lambda * e^(-lambda * y)
    # 生成平滑的横坐标点
    x_theory = np.linspace(0, np.max(y_data), 1000)
    y_theory = LAMBDA * np.exp(-LAMBDA * x_theory)
    
    plt.plot(x_theory, y_theory, 'r-', linewidth=2, label=f'理论上的指数分布曲线 ($\lambda$={LAMBDA})')
    
    # 添加图表信息
    plt.title(f'逆变换采样验证：从均匀分布到指数分布 (样本数={N_SAMPLES})')
    plt.xlabel('随机变量 Y 的取值')
    plt.ylabel('概率密度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print(f"模拟完成！")
    print(f"理论均值应该是: {1/LAMBDA:.4f}")
    print(f"模拟数据的实际均值: {np.mean(y_data):.4f}")
    print(f"差距: {abs(1/LAMBDA - np.mean(y_data)):.6f}")
    
    plt.show()

if __name__ == "__main__":
    run_simulation()