"""
文件名: law_of_large_numbers_vis.py
功能: 模拟并可视化大数定律（LLN）的收敛过程，直观展示“频率如何稳定于概率”。

【这是什么？】
这段代码演示了当你不断增加试验次数（n）时，样本均值（Sample Mean）是如何像被磁铁吸引一样，
逐渐收敛到总体期望（True Expectation）的。它同时也提供了一个“破坏者”模式（柯西分布），
让你亲眼看到当期望不存在时，大数定律是如何失效的。

【怎么用？】
直接运行即可。
1. 默认模式下，你会看到多条曲线从剧烈震荡最终汇聚成一条直线，这验证了辛钦大数定律。
2. 你可以在“参数配置区”修改 distribution_type 为 'cauchy'，观察数学规律崩塌的壮观景象。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 试验的总步数（即 n 的最大值，对应横坐标）
MAX_TRIALS = 2000

# 模拟的“平行宇宙”数量（即重复做多少组实验，对应图中线条的数量）
NUM_PATHS = 50

# 总体分布的类型
# 可选: 'normal' (正态分布，满足大数定律)
# 可选: 'cauchy' (柯西分布，期望不存在，破坏大数定律)
DISTRIBUTION_TYPE = 'normal' 

# 设定的总体期望（仅对 normal 有效，作为收敛的目标靶心）
TRUE_EXPECTATION = 0

# 绘图设置：线条透明度，为了看清重叠效果
LINE_ALPHA = 0.15

# --- 核心逻辑区 ---

def generate_data(dist_type, n_paths, n_trials):
    """
    根据指定分布生成随机数据。
    这里对应数学中的“独立同分布 (i.i.d.) 随机变量序列 X_1, X_2, ...”
    """
    if dist_type == 'normal':
        # 标准正态分布，期望 E(X) = 0
        return np.random.standard_normal((n_paths, n_trials))
    elif dist_type == 'cauchy':
        # 标准柯西分布，期望 E(X) 不存在（发散）
        return np.random.standard_cauchy((n_paths, n_trials))
    else:
        raise ValueError("不支持的分布类型，请检查配置区。")

def calculate_sample_means(data):
    """
    计算样本均值的序列。
    数学公式：Y_n = (X_1 + ... + X_n) / n
    """
    # axis=1 表示沿着时间轴（试验次数）进行累加
    # cumulative_sum 对应公式中的分子：\sum_{i=1}^n X_i
    cumulative_sum = np.cumsum(data, axis=1)
    
    # 生成对应的 n 序列：[1, 2, 3, ..., MAX_TRIALS]
    # trial_steps 对应公式中的分母：n
    trial_steps = np.arange(1, data.shape[1] + 1)
    
    # 利用广播机制直接相除，得到每一时刻的样本均值
    sample_means = cumulative_sum / trial_steps
    return sample_means, trial_steps

# --- 绘图执行区 ---

def main():
    print(f"正在模拟 {NUM_PATHS} 条路径，每条路径包含 {MAX_TRIALS} 次试验...")
    print(f"当前分布类型: {DISTRIBUTION_TYPE}")
    
    # 1. 生成原始随机数据
    raw_data = generate_data(DISTRIBUTION_TYPE, NUM_PATHS, MAX_TRIALS)
    
    # 2. 计算收敛路径（样本均值序列）
    means, steps = calculate_sample_means(raw_data)
    
    # 3. 创建画布
    plt.figure(figsize=(10, 6), dpi=100)
    
    # 4. 绘制每一条样本均值路径
    # 每一条线代表一个“观察者”在不同试验次数下看到的平均值
    for i in range(NUM_PATHS):
        plt.plot(steps, means[i], color='#1f77b4', alpha=LINE_ALPHA, linewidth=1)
    
    # 5. 绘制理论期望线（基准线）
    if DISTRIBUTION_TYPE == 'normal':
        plt.axhline(y=TRUE_EXPECTATION, color='red', linestyle='--', linewidth=2, label='总体期望 (E=0)')
        title_suffix = "大数定律生效：震荡逐渐消失"
    else:
        # 柯西分布没有期望，所以画一条线仅作参考，通常线会飞出天际
        plt.axhline(y=0, color='red', linestyle='--', linewidth=2, label='基准线 (非期望)')
        title_suffix = "大数定律失效：震荡永不停止"
        
    # 装饰图表
    plt.title(f"样本均值的收敛行为模拟\n({title_suffix})", fontsize=14)
    plt.xlabel("试验次数 n (Sample Size)", fontsize=12)
    plt.ylabel("样本均值 (Sample Mean)", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    # 针对柯西分布限制一下Y轴，否则图表可能会被极端值压缩得看不清
    if DISTRIBUTION_TYPE == 'cauchy':
        plt.ylim(-10, 10)
        plt.text(MAX_TRIALS/2, 8, "注意：柯西分布导致均值偶尔出现极端跳变", 
                 color='red', ha='center', backgroundcolor='white')
    
    plt.tight_layout()
    print("绘图完成。请观察弹出的窗口。")
    plt.show()

if __name__ == "__main__":
    main()