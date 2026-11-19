"""
文件名: wealth_distribution_simulation.py
功能: 模拟“乘法增长”与“贫困底线”如何共同制造出贫富悬殊的幂律分布。

【这是什么？】
这段代码演示了一个残酷的社会实验：
如果是“加法游戏”（每人每天随机赚/赔1块钱），财富会服从正态分布（大家差不多）。
但如果是“乘法游戏”（每人每天随机赚/赔10%），且每个人都有最低生存底线，
最终就会诞生“幂律分布”：绝大多数人挣扎在底线附近，而极少数人掌握绝大部分财富。

【怎么用？】
直接运行即可。程序会弹出两个窗口：
1. 普通坐标图：你会看到一个巨大的“L”型，这就是贫富分化的直观样子。
2. 双对数坐标图：你会看到数据点神奇地排成了一条直线，这是幂律分布的铁证。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 (你可以随意修改这些数字来观察世界) ---

# 1. 模拟的人数 (建议 1000 - 10000)
NUM_PEOPLE = 5000

# 2. 初始财富值 (也是贫困底线，跌破此线会触发“低保”或被新移民替代)
MIN_WEALTH = 10.0

# 3. 模拟的轮数 (时间越久，贫富分化越明显)
STEPS = 5000

# 4. 每一轮的波动幅度 (0.1 代表 10% 的盈亏)
VOLATILITY = 0.1 

# ---------------------------------------------------------

def run_simulation():
    # 初始化：所有人最开始都只有最低财富
    wealth = np.full(NUM_PEOPLE, MIN_WEALTH)
    
    print(f"正在模拟 {NUM_PEOPLE} 个人的财富演化，请稍候...")
    
    for t in range(STEPS):
        # --- 核心数学逻辑 1：乘法增长 (Multiplicative Process) ---
        # 现实中的财富不是线性累加的，而是按比例增值的（如投资回报、复利）。
        # 这里模拟每人每轮随机 盈/亏 VOLATILITY 的比例。
        # np.random.uniform(-1, 1) 生成 -1 到 1 之间的随机数
        fluctuation = 1 + VOLATILITY * np.random.uniform(-1, 1, NUM_PEOPLE)
        wealth = wealth * fluctuation
        
        # --- 核心数学逻辑 2：反射壁 (Reflective Barrier) ---
        # 对应现实中的“生存底线”或“新入场的穷人”。
        # 如果没有这个底线，乘法过程最终会变成对数正态分布。
        # 加上这个底线后，数学上证明了它会收敛为幂律分布 (Kesten Process)。
        wealth[wealth < MIN_WEALTH] = MIN_WEALTH

    return wealth

def plot_results(wealth):
    # 设置绘图风格
    plt.style.use('ggplot')
    
    # 尝试设置中文字体（为了让你的图表显示中文，这里做了兼容性处理）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建两个子图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- 图 1：普通坐标下的直方图 ---
    # 这是我们肉眼看到的“真实世界”：极度不平等
    ax1.hist(wealth, bins=50, color='#3498db', alpha=0.8, edgecolor='black')
    ax1.set_title("图1：普通视角（贫富悬殊）")
    ax1.set_xlabel("财富金额")
    ax1.set_ylabel("人数")
    ax1.text(0.5, 0.5, "绝大多数人\n挤在左边", transform=ax1.transAxes, fontsize=12, color='red')

    # --- 图 2：双对数坐标下的分布 (Log-Log Plot) ---
    # 这是数学家看到的“规律世界”：一条直线
    # 我们不直接画 hist，而是画“互补累积分布函数 (CCDF)”
    # 因为 hist 在双对数下噪音太大，CCDF 才是验证幂律的标准方法
    
    # 1. 对数据排序
    sorted_wealth = np.sort(wealth)
    # 2. 计算排名比例 (y轴)
    # y = 1.0 意味着是第1名(最穷)，y -> 0 意味着是最后一名(最富)
    # 这里计算的是 P(X >= x)，即有多少比例的人财富大于 x
    y_vals = 1.0 - np.arange(len(sorted_wealth)) / len(sorted_wealth)
    
    ax2.loglog(sorted_wealth, y_vals, marker='.', linestyle='none', color='#e74c3c', alpha=0.3)
    ax2.set_title("图2：上帝视角（双对数坐标）")
    ax2.set_xlabel("财富金额 (对数刻度)")
    ax2.set_ylabel("财富大于该金额的人数比例 (对数刻度)")
    
    # 画一条辅助线，说明如果是完美的幂律，应该长什么样
    # 幂律公式：P(x) ~ x^(-alpha)
    # 在双对数图上，y = -alpha * x + b，即一条斜率为负的直线
    ax2.text(0.6, 0.6, "近似一条直线\n证明了幂律的存在", transform=ax2.transAxes, fontsize=12, color='black')

    print("绘图完成。请观察弹出的窗口。")
    print(f"最高财富: {np.max(wealth):.2f}")
    print(f"前 1% 的人掌握了 {np.sum(np.sort(wealth)[-int(NUM_PEOPLE*0.01):]) / np.sum(wealth) * 100:.2f}% 的总财富")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    final_wealth = run_simulation()
    plot_results(final_wealth)