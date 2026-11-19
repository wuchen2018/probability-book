"""
文件名: binomial_coin_toss_simulation.py
功能: 模拟二项分布的形成过程（大规模抛硬币实验）

【这是什么？】
数学课本告诉你“二项分布描述了n次独立重复实验中成功的次数”。
这就好比让一万个人（NUM_EXPERIMENTS），每个人都去抛10次硬币（N），
然后统计他们每个人抛出正面的次数。
这段代码就是那个不知疲倦的“虚拟裁判”，它会瞬间完成这几十万次投掷，
并把结果画出来，让你亲眼看看“随机中的确定性”长什么样。

【怎么用？】
1. 直接运行代码，你会看到一张对比图：
   - 蓝色柱状图是“实际模拟”的结果（现实）。
   - 红色虚线是“数学公式”算出的理论值（理想）。
2. 尝试修改“参数配置区”里的 P（把0.5改成0.1或0.9），
   重新运行，观察分布的形状是如何发生“倾斜”的。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# --- 可调整参数配置区 ---
# N : 每个人做多少次实验？（例如：抛 10 次硬币）
# 对应二项分布 B(n, p) 中的 n
N = 10  

# P : 单次实验成功的概率是多少？（例如：硬币正面朝上的概率是 0.5）
# 对应二项分布 B(n, p) 中的 p
P = 0.5 

# NUM_EXPERIMENTS : 我们找多少个人来做这个实验？
# 样本越多，模拟结果越接近理论曲线（大数定律）
NUM_EXPERIMENTS = 10000 

# --- 模拟实验开始 ---

print(f"正在进行模拟：{NUM_EXPERIMENTS} 位虚拟实验员，每人抛 {N} 次硬币，正面概率 {P}...")

# 核心模拟步骤：
# np.random.binomial(n, p, size=size) 
# 这行代码的意思是：让 size 个人，每个人都做 n 次伯努利实验，
# 并返回每个人成功的次数。
# 比如：[5, 4, 6, 5, ...] 代表第一个人中了5次，第二个人中了4次...
simulated_results = np.random.binomial(n=N, p=P, size=NUM_EXPERIMENTS)

# --- 理论计算开始 ---

# 生成所有可能的成功次数（从 0 次到 N 次）
k_values = np.arange(0, N + 1)

# 利用二项分布公式 P(X=k) = C(n,k) * p^k * (1-p)^(n-k) 计算理论概率
# binom.pmf 是 Probability Mass Function（概率质量函数）
theoretical_probs = binom.pmf(k_values, N, P)

# --- 绘图对比 ---
plt.figure(figsize=(10, 6))

# 1. 绘制模拟结果（直方图）
# density=True 表示将纵轴转化为“概率密度/频率”，以便和理论概率对比
# alpha=0.6 让颜色半透明，美观一点
plt.hist(simulated_results, bins=np.arange(-0.5, N + 1.5, 1), 
         density=True, color='skyblue', edgecolor='white', alpha=0.8, 
         label=f'模拟结果 (实验次数={NUM_EXPERIMENTS})')

# 2. 绘制理论曲线（折线图/散点图）
# 'ro--' 表示：红色(red)、圆点(o)、虚线(--)
plt.plot(k_values, theoretical_probs, 'ro--', linewidth=2, markersize=8, 
         label=f'理论概率 B(n={N}, p={P})')

# 设置图表细节
plt.title(f'二项分布：模拟 vs 理论 (n={N}, p={P})', fontsize=14)
plt.xlabel('成功次数 (k)', fontsize=12)
plt.ylabel('概率 P(X=k)', fontsize=12)
plt.xticks(k_values) # 强制显示所有整数刻度
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 展示结果
print("模拟完成！请查看弹出的图像。")
print(f"理论期望值 E[X] = n*p = {N * P}")
print(f"模拟平均值 Mean = {np.mean(simulated_results):.4f}")
plt.show()