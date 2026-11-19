"""
文件名: visualize_confidence_interval_coverage.py
功能: 模拟置信区间的“捕鱼”过程，直观展示“95%置信水平”的频率学派含义。

【这是什么？】
这段代码带你体验“上帝视角”。我们设定一个真实的总体均值（真值），然后进行多次重复抽样。
你会看到：虽然真值（鱼）只有一条且固定不动，但每次计算出的区间（网）都在变化。
所谓的“95%置信水平”，不是指某一次撒网的成功率，而是指长期撒网的“平均命中率”。

【怎么用？】
直接运行即可。
程序会画出100个区间。你会发现，大部分区间（蓝色）都盖住了真值线，但总有几个倒霉的区间（红色）完全错过了真值。
你可以尝试修改下方的“置信水平”，看看如果要求99%的把握，区间会变宽多少？
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- 可调整参数配置区 (Config) ---
TRUE_MU = 170           # 上帝视角的真实均值 (例如：真实身高 170cm)
TRUE_SIGMA = 5          # 总体标准差 (假设已知)
SAMPLE_SIZE = 30        # 每次实验抽样的人数 (n)
EXPERIMENTS = 100       # 重复做多少次实验 (模拟“长期频率”)
CONFIDENCE_LEVEL = 0.95 # 置信水平 (0.95 代表 95%)

# --- 绘图风格设置 ---
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号

def simulate_confidence_intervals():
    # 1. 准备画布
    plt.figure(figsize=(10, 6))
    
    # 2. 绘制“真值线”
    # 在频率学派中，参数是固定的，所以它是一条不动的垂直线
    plt.axvline(TRUE_MU, color='green', linestyle='--', linewidth=2, label=f'真实均值 ({TRUE_MU})')
    
    # 3. 计算临界值 (Z-score)
    # 根据正态分布理论，找到对应置信水平的“分位数”
    # 例如 95% 对应 1.96, 99% 对应 2.576
    alpha = 1 - CONFIDENCE_LEVEL
    z_critical = stats.norm.ppf(1 - alpha/2) 
    
    # 理论上的标准误 (Standard Error)，这是“尺子”的精度
    std_error = TRUE_SIGMA / np.sqrt(SAMPLE_SIZE)
    
    # 统计有多少次成功捕捉
    capture_count = 0
    
    print(f"开始模拟 {EXPERIMENTS} 次抽样实验...")
    
    # 4. 循环模拟每一次实验
    for i in range(EXPERIMENTS):
        # 4.1 上帝视角生成数据：从正态分布中随机抽取 n 个人
        sample_data = np.random.normal(loc=TRUE_MU, scale=TRUE_SIGMA, size=SAMPLE_SIZE)
        
        # 4.2 计算样本均值 (点估计)
        x_bar = np.mean(sample_data)
        
        # 4.3 构造置信区间 (区间估计)
        # 公式：样本均值 ± 临界值 × 标准误
        interval_min = x_bar - z_critical * std_error
        interval_max = x_bar + z_critical * std_error
        
        # 4.4 判断：这次撒网捞到鱼了吗？
        # 如果真值在区间范围内，不仅算成功，颜色也标记为蓝色
        if interval_min <= TRUE_MU <= interval_max:
            capture_count += 1
            color = 'skyblue'  # 成功捕获的颜色
            line_style = '-'
        else:
            color = 'red'      # 失败（漏网）的颜色，高亮显示
            line_style = '-'
            # 在控制台打印失败的实验编号，方便观察
            # print(f"实验 #{i+1} 失败：区间 [{interval_min:.2f}, {interval_max:.2f}] 未包含真值")

        # 4.5 将这个区间画在图上
        # y轴仅仅代表实验的序号，没有数学含义
        plt.plot([interval_min, interval_max], [i, i], color=color, alpha=0.8, linewidth=1.5, linestyle=line_style)
        # 画出样本均值点
        plt.scatter(x_bar, i, color=color, s=10)

    # 5. 完善图表信息
    coverage_rate = capture_count / EXPERIMENTS
    title_text = (f"置信区间模拟 (n={SAMPLE_SIZE}, 重复{EXPERIMENTS}次)\n"
                  f"目标置信水平: {CONFIDENCE_LEVEL:.0%} | 实际命中率: {coverage_rate:.0%}")
    
    plt.title(title_text, fontsize=14)
    plt.xlabel("数值范围", fontsize=12)
    plt.ylabel("实验序号 (1~100)", fontsize=12)
    
    # 只显示图例中的“真值线”，避免区间线重复导致的图例混乱
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulate_confidence_intervals()