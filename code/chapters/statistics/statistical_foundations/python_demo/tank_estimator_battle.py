import numpy as np
import matplotlib.pyplot as plt

"""
文件名: tank_estimator_battle.py
功能: 模拟二战坦克问题，对比不同统计量推断总体数量N的效果

【这是什么？】
这是一个“算法角斗场”。我们在上帝视角设定了敌军坦克的真实总数（比如300辆）。
然后让计算机模拟“缴获5辆坦克”，并分别用三种不同的统计学方法去猜总数。
重复模拟一万次后，你会发现哪种方法是“神算子”，哪种方法是“猪队友”。

【怎么用？】
直接运行即可。程序会画出三张图，展示三种方法的估算分布。
你可以试着修改下方的 SAMPLE_SIZE（缴获数量），看看样本越多，猜测是否越准。
"""

# --- 可调整参数配置区 ---
TRUE_TOTAL_TANKS = 300   # 【上帝视角】敌军坦克的真实总数 (N)
SAMPLE_SIZE = 5          # 每次缴获的坦克数量 (n)，样本量越小越难猜
SIMULATION_TRIALS = 10000 # 模拟多少次战役（实验次数，越多越接近理论值）

# 设置绘图风格，确保中文显示正常
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120

def run_simulation():
    # 用于存储三种方法的猜测结果
    estimates_mean_based = [] # 方法A：基于均值
    estimates_max_raw = []    # 方法B：直接用最大值
    estimates_max_corrected = [] # 方法C：修正后的最大值（MVUE）

    print(f"--- 模拟开始：敌军共有 {TRUE_TOTAL_TANKS} 辆坦克，每次缴获 {SAMPLE_SIZE} 辆 ---")
    
    for _ in range(SIMULATION_TRIALS):
        # 1. 模拟战场缴获
        # 从 1 到 N 中随机抽取 n 个不重复的编号
        captured_tanks = np.random.choice(
            np.arange(1, TRUE_TOTAL_TANKS + 1), 
            size=SAMPLE_SIZE, 
            replace=False
        )
        
        # 2. 计算关键统计量
        sample_mean = np.mean(captured_tanks) # 样本均值
        sample_max = np.max(captured_tanks)   # 样本最大值 (充分统计量)
        
        # 3. 方法A：基于均值的朴素估计
        # 逻辑：如果坦克编号是均匀分布的，平均值应该在中间 (N/2)
        # 所以 N 大约等于 2 * 均值
        est_a = sample_mean * 2 - 1 
        estimates_mean_based.append(est_a)
        
        # 4. 方法B：直接用最大值
        # 逻辑：既然我看到了编号100，那总数至少是100。我就猜最大值。
        est_b = sample_max
        estimates_max_raw.append(est_b)
        
        # 5. 方法C：修正后的最大值 (最小方差无偏估计 MVUE)
        # 逻辑：最大值肯定比真实 N 小。
        # 统计学推导告诉我们，它平均会“缩水” (n)/(n+1)。
        # 所以我们要乘以 (n+1)/n 把这个水分“挤”回去。
        # (注：对于离散整数，公式稍微有点变化，这里使用经典的离散修正公式)
        est_c = sample_max * (1 + 1/SAMPLE_SIZE) - 1
        estimates_max_corrected.append(est_c)

    # --- 结果可视化 ---
    plt.figure(figsize=(12, 8))
    
    # 定义绘图辅助函数
    def plot_hist(data, ax, title, color):
        ax.hist(data, bins=50, color=color, alpha=0.7, edgecolor='white')
        ax.axvline(TRUE_TOTAL_TANKS, color='red', linestyle='--', linewidth=2, label='真实总数N')
        ax.axvline(np.mean(data), color='black', linestyle='-', linewidth=2, label='平均猜测值')
        ax.set_title(title, fontsize=14)
        ax.legend()
        ax.set_xlim(TRUE_TOTAL_TANKS * 0.5, TRUE_TOTAL_TANKS * 1.5) # 统一X轴范围方便对比
    
    # 绘制三个子图
    ax1 = plt.subplot(3, 1, 1)
    plot_hist(estimates_mean_based, ax1, 
              f"方法A：均值翻倍法 (平均猜测: {np.mean(estimates_mean_based):.1f})\n评价：波动极大，虽然也是无偏的，但太不靠谱", 
              'gray')
    
    ax2 = plt.subplot(3, 1, 2)
    plot_hist(estimates_max_raw, ax2, 
              f"方法B：朴素最大值法 (平均猜测: {np.mean(estimates_max_raw):.1f})\n评价：波动小，但系统性偏小（你看，永远在红线左边）", 
              'orange')
    
    ax3 = plt.subplot(3, 1, 3)
    plot_hist(estimates_max_corrected, ax3, 
              f"方法C：修正最大值法 (平均猜测: {np.mean(estimates_max_corrected):.1f})\n评价：准确击中红线！且波动很小，这就是数学的威力", 
              'green')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()