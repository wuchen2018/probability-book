"""
文件名：1_entropy_vs_variance_demo.py
功能：直观对比“方差”与“信息熵”的区别
说明：
    很多初学者会把“波动大（方差大）”误认为是“不确定性高（熵高）”。
    这个脚本通过三个极端的例子，让你亲眼看到这两个指标是如何“打架”的。
    
    我们构建了三个场景：
    1. 【彩票场景】：要么归零，要么中大奖。波动极大，但几乎确定会输（熵很低）。
    2. 【硬币场景】：输赢都在毫厘之间。波动极小，但完全猜不到结果（熵很高）。
    3. 【完美骰子】：波动适中，但结果完全随机（熵最高）。
    
作者：大白话概率论
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 设置中文字体，确保绘图时不乱码 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def calculate_entropy(probs):
    """
    计算香农熵 (单位：比特)
    公式：H(X) = - sum(p * log2(p))
    """
    # 过滤掉概率为0的项，因为 log2(0) 无意义（数学上定义为0）
    probs = np.array(probs)
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

def calculate_variance(values, probs):
    """
    计算方差
    公式：Var(X) = E[(X - mu)^2]
    衡量数值偏离平均值的程度（波动幅度）
    """
    values = np.array(values)
    probs = np.array(probs)
    
    # 1. 先算期望（平均值）
    mean = np.sum(values * probs)
    
    # 2. 再算方差：(数值 - 平均值)的平方，再加权平均
    variance = np.sum(probs * (values - mean)**2)
    return variance

def plot_distribution(ax, values, probs, title, color):
    """
    绘制单个分布的柱状图，并在图上标记熵和方差
    """
    # 绘制柱状图
    ax.bar(values, probs, width=2.0, color=color, alpha=0.7, edgecolor='black')
    
    # 计算指标
    ent = calculate_entropy(probs)
    var = calculate_variance(values, probs)
    
    # 设置图形属性
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('数值 (比如金额)', fontsize=12)
    ax.set_ylabel('概率', fontsize=12)
    ax.set_ylim(0, 1.1)
    
    # 在图上显示核心指标（这就是我们要对比的“成绩单”）
    info_text = (
        f"熵 (不确定性): {ent:.2f} bits\n"
        f"方差 (波动幅度): {var:.2f}"
    )
    # 用红框把指标圈出来，醒目一点
    ax.text(0.95, 0.95, info_text, transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# --- 主程序开始 ---
if __name__ == "__main__":
    print("正在启动模拟实验...请稍候窗口弹出...")

    # 创建画布：1行2列
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('终极对决：方差 vs 信息熵', fontsize=18)

    # === 场景 A：彩票 (高风险，低悬念) ===
    # 99% 的概率输掉 (0元)，1% 的概率中大奖 (100元)
    # 这是一个典型的“黑天鹅”分布
    values_a = [0, 100]
    probs_a = [0.99, 0.01]
    
    plot_distribution(ax1, values_a, probs_a, 
                     title="场景A：买彩票\n(波动极大，但结果基本已注定)", 
                     color='tab:red')

    # === 场景 B：均匀分布 (低风险，高悬念) ===
    # 48, 49, 50, 51, 52 这5个数，出现的概率完全相等
    # 数值这就这几个，波动很小，但你完全猜不到下一个是哪个
    values_b = [48, 49, 50, 51, 52]
    probs_b = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    plot_distribution(ax2, values_b, probs_b, 
                     title="场景B：完全随机\n(波动很小，但完全猜不到)", 
                     color='tab:blue')

    print("-" * 50)
    print("实验结论解读：")
    print(f"场景A（彩票）：方差高达 {calculate_variance(values_a, probs_a):.1f}，但熵只有 {calculate_entropy(probs_a):.2f} bits。")
    print("  -> 理由：虽然一旦发生就惊天动地（方差大），但因为大概率不发生，所以其实很好猜（熵低）。")
    print("-" * 50)
    print(f"场景B（随机）：方差只有 {calculate_variance(values_b, probs_b):.1f}，但熵高达 {calculate_entropy(probs_b):.2f} bits。")
    print("  -> 理由：虽然数值都在50附近（方差小），但每个数机会均等，根本猜不准（熵高）。")
    print("-" * 50)
    
    plt.tight_layout()
    plt.show()