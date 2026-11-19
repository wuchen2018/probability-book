"""
文件名: verify_memoryless_property.py
功能: 通过蒙特卡洛模拟，验证指数分布的“无记忆性”

【这是什么？】
直觉告诉我们：“用得越久，坏得越快”。但数学说：“对于指数分布，过去的时间不影响未来”。
这段代码模拟了数万个独立部件的寿命。我们将对比两组数据：
1. “全新组”：刚出厂的部件能用多久。
2. “老寿星组”：那些已经活过了 s 时间的部件，**剩下**还能活多久。
如果无记忆性成立，这两组数据的分布应该完全重合。

【怎么用？】
直接运行即可。你将看到上下两个分布图，它们共享同一个坐标轴。
你会直观地发现，经过截断的“剩余寿命”分布，竟然和全新的寿命分布一模一样！
你可以尝试修改 LAMBDA（故障率）或 ALREADY_WAITED（已经过去的时间），看看结论是否动摇。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# --- 设置中文字体，防止图表中的中文显示为方块 ---
# 兼容 Windows 和 Mac 的常见中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Arial Unicode MS', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# --- 可调整参数配置区 ---
LAMBDA = 0.5           # 故障率 (Rate)，即平均每单位时间发生 0.5 次
ALREADY_WAITED = 5.0   # 假设部件已经正常运行了多久 (s)
SAMPLE_SIZE = 100000   # 模拟样本数量 (建议至少 10万，数量越大，柱状图越平滑)
BINS = 60              # 直方图的柱子数量

def run_simulation():
    # 1. 理论计算
    # 指数分布的理论平均寿命是 1/lambda
    theoretical_mean = 1.0 / LAMBDA
    print(f"--- 理论预设 ---")
    print(f"故障率 (lambda): {LAMBDA}")
    print(f"理论平均寿命: {theoretical_mean:.4f}")
    print(f"我们关注的问题：已经活了 {ALREADY_WAITED} 单位时间的部件，平均还能活多久？\n")

    # 2. 生成“全新组”样本
    # 对应数学公式：X ~ Exp(lambda)
    fresh_lifetimes = np.random.exponential(scale=theoretical_mean, size=SAMPLE_SIZE)

    # 3. 筛选“老寿星组”样本
    # 只有那些寿命超过 ALREADY_WAITED 的部件，才有资格进入这一组
    # 对应数学中的条件概率前提：T > s
    survivors = fresh_lifetimes[fresh_lifetimes > ALREADY_WAITED]
    
    if len(survivors) < 100:
        print("警告：存活下来的样本太少，请增加 SAMPLE_SIZE 或减小 ALREADY_WAITED。")
        return

    # 4. 计算“剩余寿命”
    # 既然已经活了 s，我们只关心它**还能**活多久，所以要减去 s
    # 对应数学公式中的：T - s | T > s
    remaining_lifetimes = survivors - ALREADY_WAITED

    # 5. 统计结果对比
    fresh_mean = np.mean(fresh_lifetimes)
    remaining_mean = np.mean(remaining_lifetimes)

    print(f"--- 模拟结果 ---")
    print(f"全新部件的平均寿命: {fresh_mean:.4f}")
    print(f"筛选出的“老寿星”数量: {len(survivors)}")
    print(f"老寿星们的平均【剩余寿命】: {remaining_mean:.4f}")
    
    diff_percent = abs(fresh_mean - remaining_mean) / fresh_mean * 100
    print(f"两者均值差异: {diff_percent:.2f}%")
    
    if diff_percent < 1.0:
        print("结论：差异极小，无记忆性得到验证！(过去的苦难就像没发生过一样)")
    else:
        print("结论：存在差异，可能是样本量不足导致的随机误差。")

    # ==========================================
    # 6. 可视化对比 (采用上下分图，共享X轴和Y轴，直观对比形状)
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, sharey=True)
    fig.suptitle(f'指数分布“无记忆性”的视觉证明 ($\lambda={LAMBDA}$)', fontsize=16)

    # 理论曲线的数据点 (用于在直方图上叠加完美的理论线)
    x_vals = np.linspace(0, 20, 200)
    y_vals = LAMBDA * np.exp(-LAMBDA * x_vals)

    # 上图：“全新组”
    ax1.hist(fresh_lifetimes, bins=BINS, density=True, alpha=0.7, 
             color='#1f77b4', edgecolor='black', range=(0, 20), label='模拟数据 (全新组)')
    ax1.plot(x_vals, y_vals, color='red', linestyle='--', linewidth=2, label='理论数学曲线')
    ax1.set_title(f'全新出厂部件的寿命分布 (样本量: {SAMPLE_SIZE})', fontsize=12)
    ax1.set_ylabel('概率密度')
    ax1.legend()
    ax1.grid(True, alpha=0.3, linestyle=':')

    # 下图：“老寿星组”的剩余寿命
    ax2.hist(remaining_lifetimes, bins=BINS, density=True, alpha=0.7, 
             color='#ff7f0e', edgecolor='black', range=(0, 20), label=f'模拟数据 (已运行 {ALREADY_WAITED} 后的剩余寿命)')
    ax2.plot(x_vals, y_vals, color='red', linestyle='--', linewidth=2, label='理论数学曲线')
    ax2.set_title(f'“老寿星”部件的【剩余寿命】分布 (样本量: {len(survivors)})', fontsize=12)
    ax2.set_xlabel('时间')
    ax2.set_ylabel('概率密度')
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle=':')

    # 增加一个醒目的文本框
    text_str = "注意看：\n尽管下方的部件已经度过了漫长的岁月，\n但它们的【剩余寿命】分布形状\n和上方全新部件一模一样！"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax2.text(10, 0.3, text_str, fontsize=11, verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92) # 给主标题留出空间
    plt.show()

if __name__ == "__main__":
    run_simulation()