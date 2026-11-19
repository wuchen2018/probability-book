"""
文件名: softmax_temperature_and_stability.py
功能: 演示 Softmax 函数的温度缩放效应与防止数值溢出的平移技巧

【这是什么？】
将任意实数（Logits）转换为概率分布的计算过程。包含了引入温度参数 T 来控制概率分布“软硬”程度的数学逻辑，以及利用平移不变性（减去最大值）来防止计算机浮点数溢出的工程实现。

【怎么用？】
直接运行该脚本。终端会输出未优化版本导致溢出的现象，以及优化后得到的正确概率。同时会弹出一张图表，直观展示不同温度 T 对同一个输入所产生的概率分布变化。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---

# 1. 模拟常规的原始分数
RAW_SCORES_NORMAL = np.array([2.5, 1.8, -0.3, 0.5])

# 2. 模拟极端的原始分数（用于测试计算机的数值极限）
RAW_SCORES_EXTREME = np.array([1000.0, 1001.0, 999.0, 998.0])

# 3. 想要观察的温度系数列表（建议尝试极小值如 0.01，或极大值如 100）
TEMPERATURES = [0.2, 1.0, 5.0]


def naive_softmax(x):
    # 这里直接套用基础的数学公式：e^x / sum(e^x)
    # 当输入值极大时，np.exp(x) 会超出 float64 的表示范围，导致溢出（Overflow）
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def stable_softmax(x, t=1.0):
    # 第一步：引入温度系数进行缩放
    # 对应数学公式中的 z_i / T。T越大，分数之间的绝对差距就被压缩得越小
    x_scaled = x / t
    
    # 第二步：寻找当前数组的最大值
    max_val = np.max(x_scaled)
    
    # 第三步：平移数据
    # 利用平移不变性：将整个分布向左平移，使得最大项变成 0
    # 这样取指数后，最大值为 e^0 = 1，其余所有项均在 (0, 1] 之间，彻底杜绝上溢出
    x_shifted = x_scaled - max_val
    
    # 第四步：取指数并归一化
    # 此时的分子和分母在数学上等价于原公式同时除以 e^(max_val)，结果保持绝对一致
    exp_x = np.exp(x_shifted)
    probabilities = exp_x / np.sum(exp_x)
    
    return probabilities

if __name__ == "__main__":
    # ==========================================
    # 实验一：见证数值溢出与数学平移的威力
    # ==========================================
    print("【实验一：数值稳定性测试】")
    print(f"输入极端分数: {RAW_SCORES_EXTREME}")
    
    # 尝试用天真版本的 Softmax 计算极端值
    # 注意：这里 numpy 默认会抛出 RuntimeWarning
    print("\n--- 使用基础公式 (可能产生 NaN 或 Inf) ---")
    naive_result = naive_softmax(RAW_SCORES_EXTREME)
    print(f"计算结果: {naive_result}")
    
    # 使用带有平移技巧的稳定版 Softmax 计算
    print("\n--- 使用减去最大值的稳定版公式 ---")
    stable_result = stable_softmax(RAW_SCORES_EXTREME, t=1.0)
    print(f"计算结果: {stable_result}")
    print("结论：数学的平移不变性完美化解了计算机的物理硬件限制。\n")

    # ==========================================
    # 实验二：观察温度系数对概率分布的塑造
    # ==========================================
    print("【实验二：温度系数(T)的作用，请查看弹出的图表】")
    
    # 设置中文字体以便在图表中正常显示
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(1, len(TEMPERATURES), figsize=(12, 4), sharey=True)
    categories = [f"类别{i+1}" for i in range(len(RAW_SCORES_NORMAL))]
    x_pos = np.arange(len(categories))
    
    for i, t in enumerate(TEMPERATURES):
        # 计算不同温度下的概率分布
        probs = stable_softmax(RAW_SCORES_NORMAL, t=t)
        
        ax = axes[i]
        bars = ax.bar(x_pos, probs, color='#1F77B4', alpha=0.8)
        ax.set_title(f"温度 T = {t}")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1.0)
        
        # 在柱子上标注具体概率数值
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
    axes[0].set_ylabel("概率 (Probability)")
    fig.suptitle(f"原始分数: {RAW_SCORES_NORMAL}", fontsize=12)
    plt.tight_layout()
    plt.show()