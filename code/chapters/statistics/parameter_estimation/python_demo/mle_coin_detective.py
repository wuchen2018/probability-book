"""
文件名: mle_coin_detective.py
功能: 模拟抛硬币实验，并用最大似然估计（MLE）反推硬币的真实概率。

【这是什么？】
这段代码展示了 MLE 的核心逻辑：
1. "上帝视角"：我们设定一个真实的硬币概率（True P），产生一组随机数据。
2. "侦探视角"：假设我们不知道真实概率，仅凭这组数据，画出"似然函数"曲线。
3. 寻找真相：观察似然函数的最高点（MLE估计值）是否准确抓住了那个"上帝设定"的数值。

【怎么用？】
直接运行即可。程序会弹出一张图，展示似然函数的形状。
你可以修改下方的【可调整参数】，比如把样本量改小，看看"侦探"会不会看走眼。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# --- 可调整参数配置区 (Playground) ---
# 1. 上帝视角：设定硬币正面的真实概率 (0.0 到 1.0 之间)
TRUE_P = 0.65  

# 2. 实验规模：你想抛多少次硬币？(样本量越大，估计越准)
SAMPLE_SIZE = 20  

# 3. 绘图精度：计算似然函数时，我们把 0-1 切分成多少份？
RESOLUTION = 1000

# ---------------------------------------------------------

def run_mle_simulation():
    # ==========================================
    # 第一步：模拟现实 (生成数据)
    # ==========================================
    # 使用二项分布模拟抛硬币过程
    # np.random.binomial(n, p) 返回的是成功的次数 (即正面朝上的次数 k)
    heads_count = np.random.binomial(n=SAMPLE_SIZE, p=TRUE_P)
    
    # 计算样本均值 (频率学派的直觉)
    # 这也是伯努利分布下，通过数学推导出的 MLE 解析解： p_hat = k / n
    mle_estimate = heads_count / SAMPLE_SIZE

    print(f"--- 实验结果 ---")
    print(f"真实概率 (上帝设定): {TRUE_P}")
    print(f"抛掷次数 (N):       {SAMPLE_SIZE}")
    print(f"正面次数 (k):       {heads_count}")
    print(f"MLE估计值 (k/N):    {mle_estimate:.4f}")
    
    # ==========================================
    # 第二步：构造似然函数 (侦探推理)
    # ==========================================
    # 我们假设参数 p 可能是 0 到 1 之间的任意数值
    # np.linspace 生成一个从 0.001 到 0.999 的等差数列 (避开 0 和 1 以免对数报错)
    possible_p = np.linspace(0.001, 0.999, RESOLUTION)
    
    # 计算每个可能的 p 值对应的"似然度" (Likelihood)
    # L(p) = p^k * (1-p)^(n-k)
    # 这里的 binom.pmf 就是二项分布的概率质量函数，对应似然函数的核心部分
    likelihoods = binom.pmf(k=heads_count, n=SAMPLE_SIZE, p=possible_p)
    
    # 为了防止数值下溢 (Underflow)，通常工程上会计算"对数似然"
    # 但为了直观展示"山峰"形状，这里我们直接画原始似然值
    
    # ==========================================
    # 第三步：可视化 (寻找最高点)
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # 1. 画出似然函数曲线
    # 这条曲线展示了：在当前数据下，哪个 p 值看起来最"合理"
    plt.plot(possible_p, likelihoods, label='Likelihood Function $L(p)$', color='#1f77b4', linewidth=2)
    
    # 2. 标记 MLE 估计值 (最高点)
    # 对应的数学操作是：令 dL/dp = 0，解出驻点
    plt.axvline(x=mle_estimate, color='red', linestyle='--', alpha=0.6, label=f'MLE Estimate: {mle_estimate:.2f}')
    
    # 3. 标记真实值 (上帝视角)
    # 只有做模拟实验时我们才知道真实值，现实中这是不可知的
    plt.axvline(x=TRUE_P, color='green', linestyle=':', alpha=0.8, label=f'True Parameter: {TRUE_P}')
    
    # 图表装饰
    plt.title(f'Maximum Likelihood Estimation (Heads: {heads_count}/{SAMPLE_SIZE})', fontsize=14)
    plt.xlabel('Parameter $p$ (Probability of Heads)', fontsize=12)
    plt.ylabel('Likelihood (How plausible is this p?)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 填充最高点下方的区域，增加视觉重点
    plt.fill_between(possible_p, likelihoods, alpha=0.1, color='#1f77b4')
    
    plt.show()

if __name__ == "__main__":
    run_mle_simulation()