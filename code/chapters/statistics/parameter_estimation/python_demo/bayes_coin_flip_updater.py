"""
文件名: bayes_coin_flip_updater.py
功能: 模拟抛硬币过程中的贝叶斯认知更新，直观展示“先验 + 数据 = 后验”

【这是什么？】
这段代码演示了贝叶斯估计的核心机制：
1. 你带着一个“成见”（先验分布）开始。
2. 你观察到了现实世界的“证据”（抛硬币数据）。
3. 数学公式自动融合两者，生成你的“新认知”（后验分布）。

【怎么用？】
直接运行即可。
你可以修改配置区的数值，比如把“抛掷次数”改大，看看“成见”是如何在铁一般的事实面前崩塌的；
或者修改“先验参数”，扮演一个极其固执的人（alpha/beta 很大），看看需要多少数据才能说服你。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# --- 可调整参数配置区 (Playground) ---
# 1. 上帝视角的真实情况
TRUE_P = 0.7        # 这枚硬币真实的正面概率（比如它被做了手脚）

# 2. 你的初始成见 (先验分布 Beta(α, β))
# 提示：α和β的值越大，代表你的成见越深（惯性越大）
PRIOR_ALPHA = 10    # 虚拟的正面次数（比如你觉得它很可能是均匀的）
PRIOR_BETA = 10     # 虚拟的反面次数

# 3. 实验设置
N_TOSSES = 10       # 打算抛多少次硬币
# ------------------------------------

def run_bayes_update():
    # 1. 生成数据 (模拟抛硬币)
    # 使用二项分布模拟现实世界：1代表正面，0代表反面
    outcomes = np.random.binomial(n=1, p=TRUE_P, size=N_TOSSES)
    heads = np.sum(outcomes)      # 实际观测到的正面次数
    tails = N_TOSSES - heads      # 实际观测到的反面次数
    
    print(f"【实验结果】抛了 {N_TOSSES} 次，正面 {heads} 次，反面 {tails} 次。")
    print(f"【数据暗示】仅看数据，频率学派会觉得 p = {heads/N_TOSSES:.2f}")

    # 2. 计算贝叶斯更新 (核心数学逻辑)
    # 根据共轭先验性质：后验参数 = 先验参数 + 观测数据
    # 这就是贝叶斯公式在 Beta 分布下的“加法魔法”
    post_alpha = PRIOR_ALPHA + heads
    post_beta = PRIOR_BETA + tails

    # 3. 准备绘图数据
    x = np.linspace(0, 1, 1000)
    
    # 计算三种分布的概率密度函数 (PDF)
    y_prior = beta.pdf(x, PRIOR_ALPHA, PRIOR_BETA)
    y_post = beta.pdf(x, post_alpha, post_beta)
    
    # 构造似然函数 (Likelihood)
    # 注意：为了让似然函数能在图上和概率分布一起显示，我们需要对其缩放
    # 这里我们画的是“归一化后的似然”，即假设先验是均匀分布时的后验
    # 这样可以直观对比：纯数据 vs 融合了成见的结果
    y_likelihood = beta.pdf(x, 1 + heads, 1 + tails)

    # 4. 绘图展示
    plt.figure(figsize=(10, 6))
    
    # 画先验
    plt.plot(x, y_prior, 'g--', lw=2, label=f'先验 (成见)\nBeta({PRIOR_ALPHA}, {PRIOR_BETA})')
    plt.fill_between(x, y_prior, color='green', alpha=0.1)
    
    # 画似然 (数据)
    plt.plot(x, y_likelihood, 'b:', lw=2, label=f'似然 (数据声音)\n{heads}正 {tails}反')
    
    # 画后验
    plt.plot(x, y_post, 'r-', lw=3, label=f'后验 (最终认知)\nBeta({post_alpha}, {post_beta})')
    plt.fill_between(x, y_post, color='red', alpha=0.2)
    
    # 标注真实值
    plt.axvline(TRUE_P, color='k', linestyle='--', alpha=0.5, label=f'真实真理 p={TRUE_P}')

    plt.title(f'贝叶斯更新演示：投掷 {N_TOSSES} 次后的认知变化')
    plt.xlabel('参数 p 的取值 (正面概率)')
    plt.ylabel('概率密度 (置信度)')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # 自动调整显示范围，聚焦有意义的区域
    plt.xlim(0, 1)
    plt.ylim(bottom=0)
    
    print("绘图完成，请查看弹出的窗口。")
    plt.show()

if __name__ == "__main__":
    run_bayes_update()