"""
文件名: hypergeo_vs_binomial_simulation.py
功能: 模拟“无放回抽样”与“有放回抽样”的概率分布差异

【这是什么？】
这段代码通过可视化的方式，让你亲眼看到“超几何分布”（无放回）和“二项分布”（有放回）在不同条件下的区别。
你会发现，当总体数量 N 较小时，两者差异巨大；但当 N 变得非常大时，两者竟然神奇地重合了。

【怎么用？】
1. 调整下方的【可调整参数配置区】，特别是修改 total_N（总体总数）。
2. 运行代码，观察生成的图表。
3. 尝试将 total_N 改为 20（小池塘）和 2000（太平洋），对比图表的形状变化。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom, binom

# --- 可调整参数配置区 (在这里修改数值来做实验) ---

# 1. 总体设置
total_N = 30       # 总体中的球总数 (尝试改为 20 或 2000)
red_balls_K = 10   # 总体中红球的个数 (感兴趣的个体数)

# 2. 抽样设置
sample_n = 5       # 我们一次性抓取的球数量 (样本量)

# 3. 绘图美化
show_diff = True   # 是否在图上标注两者概率的差值

# --- 核心逻辑与计算 ---

# 计算红球在总体中的比例 (对应二项分布中的概率 p)
# 在二项分布（有放回）中，这个概率是恒定不变的。
p_prob = red_balls_K / total_N 

# 定义横坐标：可能的红球数量 k (从 0 到 n)
# 显然，我们最多只能抽到 n 个红球，最少 0 个。
k_values = np.arange(0, sample_n + 1)

# 计算 A：超几何分布的概率 (Hypergeometric Probability)
# 对应数学公式：C(K, k) * C(N-K, n-k) / C(N, n)
# 这是“严格的现实”，考虑了无放回带来的概率变化。
prob_hyper = hypergeom.pmf(k_values, total_N, red_balls_K, sample_n)

# 计算 B：二项分布的概率 (Binomial Probability)
# 对应数学公式：C(n, k) * p^k * (1-p)^(n-k)
# 这是“理想的简化”，假设每次抽取概率都不变。
prob_binom = binom.pmf(k_values, sample_n, p_prob)

# --- 结果可视化 ---

# 设置中文字体 (兼容性设置，防止中文乱码)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False 

plt.figure(figsize=(10, 6), dpi=100)

# 1. 绘制超几何分布 (用柱状图表示)
bars = plt.bar(k_values, prob_hyper, width=0.4, label='超几何分布 (无放回/真实情况)', 
               color='#1f77b4', alpha=0.8, zorder=2)

# 2. 绘制二项分布 (用红色虚线+圆点表示)
plt.plot(k_values, prob_binom, color='#d62728', linestyle='--', marker='o', 
         linewidth=2, markersize=8, label='二项分布 (有放回/近似模型)', zorder=3)

# 3. (可选) 标注差异
if show_diff:
    for k, h_p, b_p in zip(k_values, prob_hyper, prob_binom):
        # 计算绝对误差
        diff = abs(h_p - b_p)
        # 只标注差异比较明显的地方 (大于 1%)
        if diff > 0.01:
            plt.text(k, max(h_p, b_p) + 0.02, f'误差\n{diff:.1%}', 
                     ha='center', va='bottom', fontsize=9, color='gray')

# 图表装饰
plt.title(f'总体 N={total_N} 时，两种分布的对比', fontsize=14)
plt.xlabel('抽到的红球数量 (k)', fontsize=12)
plt.ylabel('概率 (Probability)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.ylim(0, max(max(prob_hyper), max(prob_binom)) * 1.2) # 让顶部留出空间

# 在图表下方添加说明
info_text = (f"实验参数：\n总体 N={total_N}, 红球 K={red_balls_K}\n抽样 n={sample_n}\n"
             f"红球占比 p={p_prob:.2%}\n\n"
             "观察：\n当 N 较小时，红色虚线与蓝色柱子错位明显（不能近似）；\n"
             "当 N 很大时，两者将几乎完全重合（可以近似）。")
plt.text(sample_n * 0.75, max(prob_hyper)*0.5, info_text, 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'), fontsize=10)

plt.tight_layout()
plt.show()

print(f"模拟结束。当前总体 N = {total_N}。")
print("建议修改代码顶部的 total_N 参数，分别尝试 20 和 2000，查看图形变化。")