"""
文件名: beta_bayesian_coin_toss.py
功能: 模拟贝叶斯更新过程：从先验信念出发，通过观测硬币抛掷数据，逐步修正为后验信念。

【这是什么？】
这段代码演示了贝叶斯统计的核心思想：
“信念（后验） = 旧信念（先验） + 新证据（数据）”
你可以设定一个“上帝视角的真实概率”（比如硬币的真实偏差），然后看看需要多少次实验，
才能把你最初设定错误（或无知）的信念拉回到真相附近。

【怎么用？】
1. 修改下方【可调整参数配置区】的数值。
2. 运行脚本。
3. 观察生成的图像：
   - 虚线是你最初的猜想（先验）。
   - 蓝线是看过数据后的修正猜想（后验）。
   - 竖线是上帝视角的真理。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- 可调整参数配置区 ---
# 1. 上帝视角：硬币真实的正面概率 (0到1之间)
# 试着把它改成 0.3 或 0.8，看看贝塔分布能不能找到它
TRUE_P = 0.65  

# 2. 实验数据：我们要抛多少次硬币？
# 试着对比 N=10 (数据少，信念动摇) 和 N=1000 (数据多，铁证如山) 的区别
N_TRIALS = 50  

# 3. 你的先入之见：初始的 Alpha 和 Beta
# Beta(1, 1) = 完全无知（平坦）
# Beta(10, 10) = 觉得应该是公平的，但不太确定
# Beta(100, 1) = 顽固地认为一定是正面（偏见极重）
PRIOR_ALPHA = 2  
PRIOR_BETA = 2   

# ------------------------------------------------------------------

def run_bayesian_update():
    # 1. 设置画图风格
    # 使用简洁的样式，避免视觉干扰
    plt.style.use('bmh')
    fig, ax = plt.subplots(figsize=(10, 6))

    # 2. 生成模拟数据 (这是你在现实中观测到的结果)
    # np.random.binomial 模拟了 N 次伯努利试验
    # 结果是一个数组，其中 1 代表正面，0 代表反面
    data = np.random.binomial(n=1, p=TRUE_P, size=N_TRIALS)
    
    # 统计观测到的成功（正面）和失败（反面）次数
    observed_heads = np.sum(data)         # 成功的次数 k
    observed_tails = N_TRIALS - observed_heads # 失败的次数 n-k
    
    print(f"【实验报告】")
    print(f"真实概率 (上帝视角): {TRUE_P}")
    print(f"观测数据: 投掷 {N_TRIALS} 次，发现 {observed_heads} 次正面，{observed_tails} 次反面")

    # 3. 执行贝叶斯更新 (核心数学步骤)
    # 根据共轭性原理：后验参数 = 先验参数 + 观测计数
    # 这行代码对应数学公式：alpha_new = alpha + k
    posterior_alpha = PRIOR_ALPHA + observed_heads
    # 这行代码对应数学公式：beta_new = beta + (n - k)
    posterior_beta = PRIOR_BETA + observed_tails

    # 4. 准备绘图数据
    # 创建一个从 0 到 1 的 x 轴，用于绘制概率密度曲线
    x = np.linspace(0, 1, 1000)
    
    # 计算 先验分布 的密度值 (pdf)
    y_prior = stats.beta.pdf(x, PRIOR_ALPHA, PRIOR_BETA)
    
    # 计算 后验分布 的密度值 (pdf)
    y_posterior = stats.beta.pdf(x, posterior_alpha, posterior_beta)

    # 5. 绘制图形
    # 绘制上帝视角的真理线
    ax.axvline(TRUE_P, color='black', linestyle='-', alpha=0.5, label='Truth (Unknown to you)')
    
    # 绘制先验信念 (虚线)
    ax.plot(x, y_prior, 'g--', lw=2, alpha=0.6, label=f'Prior: Beta({PRIOR_ALPHA}, {PRIOR_BETA})')
    ax.fill_between(x, y_prior, color='green', alpha=0.1)

    # 绘制后验信念 (实线 - 你的最终结论)
    ax.plot(x, y_posterior, 'b-', lw=3, label=f'Posterior: Beta({posterior_alpha}, {posterior_beta})')
    ax.fill_between(x, y_posterior, color='blue', alpha=0.2)

    # 添加图表信息
    ax.set_title(f'Bayesian Update: Belief Change after {N_TRIALS} Coin Flips', fontsize=14)
    ax.set_xlabel('Probability of Heads ($p$)', fontsize=12)
    ax.set_ylabel('Density (Belief Strength)', fontsize=12)
    ax.legend(loc='upper left')
    ax.set_xlim(0, 1)
    
    # 去掉不必要的边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    print(f"【更新结果】")
    print(f"先验信念: Beta({PRIOR_ALPHA}, {PRIOR_BETA})")
    print(f"后验信念: Beta({posterior_alpha}, {posterior_beta})")
    
    # 计算并打印后验期望 (Mean = alpha / (alpha + beta))
    posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)
    print(f"你的最终猜测 (后验期望): {posterior_mean:.4f} (距离真相差 {abs(posterior_mean - TRUE_P):.4f})")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_bayesian_update()