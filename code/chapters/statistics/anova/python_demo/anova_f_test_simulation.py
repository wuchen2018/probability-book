"""
文件名: anova_f_test_simulation.py
功能: 模拟单因素方差分析（ANOVA）并直观展示 F 分布的来源

【这是什么？】
方差分析的核心在于判断：我们看到的“组间差异”究竟是真实的效应，还是随机的运气？
这个脚本不仅会帮你计算 F 值，还会进行一个“思想实验”：
它会把所有数据打乱重组 5000 次，看看在“完全没有区别”的假设下，
纯靠运气能产生多大的 F 值。这就是 F 分布的物理意义。

【怎么用？】
1. 直接运行脚本，你将看到一张直方图（模拟出的随机 F 值）和一条红线（你实际数据的 F 值）。
2. 尝试修改配置区的 `GROUP_MEANS`，把它们改成完全一样（如 [20, 20, 20]），
   看看红线会跑道哪里？P 值会变成多少？
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# --- 可调整参数配置区 (Playground) ---
# 1. 设定三组数据的真实均值（想模拟“无效”情况，就设成全等，如 [20, 20, 20]）
GROUP_MEANS = [21.0, 26.0, 19.0] 

# 2. 每组的样本数量
SAMPLES_PER_GROUP = 4

# 3. 数据的波动程度（噪音大小，标准差）
NOISE_STD = 2.0

# 4. 模拟实验的次数（用来画背景直方图）
SIMULATION_ROUNDS = 5000

# ---------------------------------------------------------

def calculate_f_statistic(groups):
    """
    手动计算 F 统计量，为了展示数学原理
    groups: 一个包含多个数组的列表，每个数组是一组数据
    """
    # 展平所有数据，计算总均值 (Grand Mean)
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    
    # 获取组数 (k) 和 总样本数 (N)
    k = len(groups)
    N = len(all_data)
    
    # --- 步骤 1: 计算组间平方和 (SSA) ---
    # 数学含义：看每个组的均值偏离总均值有多远
    ssa = 0
    for group in groups:
        group_mean = np.mean(group)
        n_i = len(group)
        ssa += n_i * (group_mean - grand_mean)**2
        
    # --- 步骤 2: 计算组内平方和 (SSE) ---
    # 数学含义：看每个数据点偏离自己组的均值有多远（纯噪音）
    sse = 0
    for group in groups:
        group_mean = np.mean(group)
        sse += np.sum((group - group_mean)**2)
        
    # --- 步骤 3: 计算自由度 ---
    df_a = k - 1      # 组间自由度
    df_e = N - k      # 组内自由度
    
    # --- 步骤 4: 计算均方 (MSA & MSE) ---
    # 数学含义：将平方和标准化，变成“平均变异强度”
    msa = ssa / df_a  # 信号强度
    mse = sse / df_e  # 噪音强度
    
    # --- 步骤 5: 计算 F 值 ---
    # 数学含义：信号是噪音的多少倍？
    # 防止除以0
    if mse == 0: return 0
    f_value = msa / mse
    
    return f_value, df_a, df_e

def run_simulation():
    # 1. 生成模拟数据
    # 我们用正态分布生成数据，模拟田里的庄稼产量
    np.random.seed(42) # 固定随机种子，保证每次运行结果一致
    groups = []
    for mean in GROUP_MEANS:
        # loc=均值, scale=标准差, size=数量
        group_data = np.random.normal(loc=mean, scale=NOISE_STD, size=SAMPLES_PER_GROUP)
        groups.append(group_data)
    
    print(f"--- 生成数据 ---")
    for i, g in enumerate(groups):
        print(f"组 {i+1} (均值={np.mean(g):.2f}): {np.round(g, 1)}")

    # 2. 计算实际数据的 F 值
    obs_f, df_a, df_e = calculate_f_statistic(groups)
    print(f"\n[实际计算结果] F值 = {obs_f:.2f}")

    # 3. 开始蒙特卡洛模拟 (Permutation Test)
    # 核心思想：假设 H0 成立（组间没区别），那我们把所有数据混在一起洗牌，
    # 重新随机分组，看看算出来的 F 值通常是多大。
    print(f"\n正在进行 {SIMULATION_ROUNDS} 次随机洗牌模拟，请稍候...")
    
    simulated_fs = []
    all_data_flat = np.concatenate(groups)
    
    for _ in range(SIMULATION_ROUNDS):
        # 洗牌：打乱所有数据的顺序
        np.random.shuffle(all_data_flat)
        
        # 重新切分：按原来的样本量切分成新组
        # 这里使用了 numpy 的 split 技巧
        new_groups = np.split(all_data_flat, np.cumsum([len(g) for g in groups])[:-1])
        
        # 计算这个“虚假”组的 F 值
        sim_f, _, _ = calculate_f_statistic(new_groups)
        simulated_fs.append(sim_f)
        
    simulated_fs = np.array(simulated_fs)

    # 4. 计算 P 值
    # 数学含义：在纯随机的情况下，出现比我们实际 F 值更大的概率是多少？
    p_value = np.sum(simulated_fs >= obs_f) / SIMULATION_ROUNDS
    print(f"[模拟 P 值] p = {p_value:.4f}")
    if p_value < 0.05:
        print("结论：拒绝零假设，组间差异显著（这是一个极小概率事件）。")
    else:
        print("结论：无法拒绝零假设，这点差异很可能只是运气。")

    # 5. 可视化
    plt.figure(figsize=(10, 6))
    
    # 绘制模拟 F 值的直方图
    plt.hist(simulated_fs, bins=50, density=True, alpha=0.6, color='gray', label='H0成立时的随机F分布')
    
    # 绘制理论 F 分布曲线 (对比用)
    x = np.linspace(0, max(simulated_fs.max(), obs_f + 2), 1000)
    y = stats.f.pdf(x, df_a, df_e)
    plt.plot(x, y, 'k--', linewidth=2, label=f'理论 F({df_a}, {df_e}) 分布')
    
    # 绘制实际观测到的 F 值
    plt.axvline(obs_f, color='#D62728', linestyle='-', linewidth=2.5, label=f'你的实际 F值={obs_f:.2f}')
    
    plt.title(f'方差分析模拟：实际 F 值在“随机世界”中的位置 (p={p_value:.4f})')
    plt.xlabel('F 统计量')
    plt.ylabel('概率密度')
    plt.legend()
    plt.grid(alpha=0.3)
    
    # 如果 F 值太大，图会很难看，限制一下显示范围
    # 但要保证能看到红线
    plt.xlim(0, max(10, obs_f + 2))
    
    plt.show()

if __name__ == "__main__":
    run_simulation()