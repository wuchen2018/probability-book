"""
文件名: pgf_sum_simulator.py
功能: 验证“独立随机变量之和”的分布，等价于它们“概率生成函数(PGF)之积”。

【这是什么？】
这行代码演示了概率论中一个神奇的性质：
如果你想知道两个骰子（或者其他离散变量）加起来的总和分布是什么，
你不需要痛苦地罗列所有组合，只需要把它们的“概率多项式”乘起来。
这里我们将用蒙特卡洛模拟（暴力法）与 PGF 多项式乘法（理论法）进行正面PK。

【怎么用？】
直接运行。
程序会生成两个独立的随机变量 X（泊松分布）和 Y（二项分布）。
你会看到一张对比图：
1. 蓝色直方图：通过 10万次 模拟实验得到的真实数据分布。
2. 红色曲线：通过 PGF 多项式乘法计算出的理论概率。
请观察两者是否完美重合。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, binom

# --- 可调整参数配置区 ---
# 模拟实验的次数（越大越接近理论值）
N_SAMPLES = 100000

# 随机变量 X 的参数 (泊松分布)
LAMBDA_X = 4.0  # 平均发生次数

# 随机变量 Y 的参数 (二项分布)
N_TRIALS_Y = 10 # 试验总次数
P_SUCCESS_Y = 0.5 # 每次成功概率

# 为了数值计算方便，截断泊松分布的尾部（取概率忽略不计的上限）
MAX_RANGE = 30 
# ------------------------

def main():
    print(f"正在进行 {N_SAMPLES} 次随机试验...")
    print(f"变量 X ~ Poisson({LAMBDA_X})")
    print(f"变量 Y ~ Binomial({N_TRIALS_Y}, {P_SUCCESS_Y})")

    # ==========================================
    # 方法一：蒙特卡洛模拟 (暴力求解 Z = X + Y)
    # ==========================================
    
    # 1. 生成 X 的随机样本
    samples_x = poisson.rvs(mu=LAMBDA_X, size=N_SAMPLES)
    
    # 2. 生成 Y 的随机样本 (独立于 X)
    samples_y = binom.rvs(n=N_TRIALS_Y, p=P_SUCCESS_Y, size=N_SAMPLES)
    
    # 3. 计算和 Z
    # 对应数学含义：Z = X + Y
    samples_z = samples_x + samples_y

    # ==========================================
    # 方法二：利用 PGF 性质 (多项式乘法)
    # ==========================================
    
    # 1. 构建 X 的概率数组 (即 PGF 的系数)
    # PGF(s) = p0 + p1*s + p2*s^2 + ...
    # 这里的 domain_x 就是幂次 [0, 1, 2, ...]，probs_x 就是系数 [P(X=0), P(X=1), ...]
    domain_x = np.arange(MAX_RANGE)
    probs_x = poisson.pmf(domain_x, mu=LAMBDA_X)
    
    # 2. 构建 Y 的概率数组
    domain_y = np.arange(N_TRIALS_Y + 1)
    probs_y = binom.pmf(domain_y, n=N_TRIALS_Y, p=P_SUCCESS_Y)
    
    # 3. 核心步骤：多项式乘法 (卷积)
    # 对应数学原理：P_Z(s) = P_X(s) * P_Y(s)
    # 在计算机中，多项式系数的乘法 等价于 向量的卷积 (Convolution)
    probs_z_theoretical = np.convolve(probs_x, probs_y)
    
    # 生成理论分布对应的 x 轴 (0, 1, 2, ...)
    domain_z = np.arange(len(probs_z_theoretical))

    # ==========================================
    # 可视化对比
    # ==========================================
    plt.figure(figsize=(10, 6))

    # 绘制模拟结果 (蓝色直方图)
    # density=True 表示将频数转换为频率，以便与理论概率对比
    plt.hist(samples_z, bins=np.arange(samples_z.max()+2)-0.5, density=True, 
             alpha=0.6, color='skyblue', label='模拟实验 (Simulation)', edgecolor='white')

    # 绘制 PGF 理论结果 (红色连线/散点)
    plt.plot(domain_z, probs_z_theoretical, 'ro-', linewidth=2, label='PGF 卷积计算 (Theory)')

    plt.title(f'验证: 独立变量和的分布 = PGF多项式的乘积\n(Z = Poisson({LAMBDA_X}) + Binomial({N_TRIALS_Y}, {P_SUCCESS_Y}))')
    plt.xlabel('随机变量 Z 的取值 (k)')
    plt.ylabel('概率 P(Z=k)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 限制一下 X 轴范围，避免看后面概率为 0 的长尾巴
    plt.xlim(0, MAX_RANGE + N_TRIALS_Y)
    
    print("绘图完成！请查看弹出的窗口。")
    print("理论上，红线应该完美穿过蓝色柱状图的顶点。")
    plt.show()

if __name__ == "__main__":
    main()