"""
文件名: kl_divergence_asymmetry.py
功能: 可视化 KL 散度的“非对称性”与“距离爆炸”现象

【这是什么？】
这段代码演示了当你把两个分布的位置调换时（D(P||Q) vs D(Q||P)），计算出的差异值完全不同。
它特别展示了当一个分布认为某事“不可能发生”（概率为0），而另一个分布认为“可能发生”时，
差异值是如何爆炸式增长到无穷大的——这就是为什么在机器学习中，我们极度恐惧概率为 0 的预测。

【怎么用？】
直接运行即可。你会看到两条曲线：
1. 蓝色曲线：以 P 为基准 (P||Q)。
2. 橙色曲线：以 Q 为基准 (Q||P)。
请注意观察当 Q 的概率接近 0 或 1 时，哪条曲线飞上了天，哪条曲线还很淡定。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 设定“真理”硬币 P 的正面概率 (建议设为 0.8 或 0.2 这种偏激的值，效果更明显)
P_HEADS_PROB = 0.8

# 设定“模仿者”硬币 Q 的测试范围 (从 0.001 到 0.999，避免直接计算 log(0))
Q_range = np.linspace(0.001, 0.999, 500)

# -----------------------

def calculate_binary_kl(p, q):
    """
    计算二项分布的 KL 散度
    p, q: 正面朝上的概率
    对应公式: P(正)*log(P(正)/Q(正)) + P(反)*log(P(反)/Q(反))
    """
    # 计算反面概率
    p_tails = 1 - p
    q_tails = 1 - q
    
    # 对应 KL 散度公式的第一项：正面项
    # term_heads = P(x) * log2( P(x) / Q(x) )
    term_heads = p * np.log2(p / q)
    
    # 对应 KL 散度公式的第二项：反面项
    term_tails = p_tails * np.log2(p_tails / q_tails)
    
    return term_heads + term_tails

def main():
    # 1. 计算两种方向的散度
    # 情况 A: D(P || Q) —— P 是老板，P 说这件事很重要，Q 必须重视
    kl_p_div_q = calculate_binary_kl(P_HEADS_PROB, Q_range)
    
    # 情况 B: D(Q || P) —— Q 是老板，Q 说这件事很重要，P 没做到
    # 注意这里参数顺序换了，第一个参数变成了 Q_range
    kl_q_div_p = calculate_binary_kl(Q_range, P_HEADS_PROB)

    # 2. 绘图设置
    plt.figure(figsize=(10, 6), dpi=120)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] # 保证中文显示
    plt.rcParams['axes.unicode_minus'] = False

    # 绘制曲线
    plt.plot(Q_range, kl_p_div_q, label=f'D(P || Q): 以 P={P_HEADS_PROB} 为基准', linewidth=3, color='#1f77b4')
    plt.plot(Q_range, kl_q_div_p, label=f'D(Q || P): 以 Q 为基准', linewidth=3, color='#ff7f0e', linestyle='--')

    # 标记 P 的位置 (差异为 0 的点)
    plt.axvline(P_HEADS_PROB, color='gray', linestyle=':', alpha=0.6)
    plt.text(P_HEADS_PROB, 0.2, ' P 的位置 (差异为0)', rotation=90, verticalalignment='bottom')

    # 装饰图表
    plt.title(f"KL 散度的不对称性演示 (真理 P={P_HEADS_PROB})", fontsize=14)
    plt.xlabel("Q 预测的正面概率", fontsize=12)
    plt.ylabel("KL 散度 (比特)", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 限制 y 轴范围，防止无穷大拉伸整个画面
    plt.ylim(0, 3) 

    print(f"当前设定的真理 P(正面) = {P_HEADS_PROB}")
    print("绘图完成！请观察图像两侧边缘的曲线行为。")
    plt.show()

if __name__ == "__main__":
    main()