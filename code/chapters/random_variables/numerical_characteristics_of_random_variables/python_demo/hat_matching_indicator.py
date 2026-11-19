"""
文件名: hat_matching_indicator.py
功能: 模拟经典“帽子配对”问题，验证示性函数求和的期望常数定律

【这是什么？】
这段代码模拟了 N 个人随机拿取 N 顶帽子的过程。通过蒙特卡洛模拟，
统计“拿到自己原来帽子”的人数分布，并计算平均值。你会神奇地发现，
无论总人数 N 是 10 还是 10000，平均配对成功的人数永远趋近于 1。

【怎么用？】
你可以修改参数区的人数 N 和模拟总次数。运行后，程序会在控制台输出
理论期望与模拟平均值的对比，并弹出一张直方图，展示“拿对帽子人数”的
实际概率分布情况。
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体，防止图表显示方块
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
NUM_PEOPLE = 100          # 参与拿帽子的人数（你可以尝试改成 10，或者 5000）
NUM_SIMULATIONS = 50000   # 模拟的实验总次数（次数越大，结果越接近理论极限）
# ------------------------

def simulate_hat_matching(n, simulations):
    # 这里我们用 0 到 n-1 的数组代表每个人的正确帽子编号
    correct_hats = np.arange(n)
    
    # 记录每一次模拟中，拿到正确帽子的人数
    matches_record = np.zeros(simulations)
    
    print(f"开始进行 {simulations} 次模拟，总人数：{n} 人...")
    
    for i in range(simulations):
        # 核心随机过程：把帽子打乱，相当于每个人随机抽一顶
        drawn_hats = np.random.permutation(n)
        
        # 示性函数的代码实现：
        # drawn_hats == correct_hats 会生成一个布尔数组（True代表1，False代表0）
        # 这个数组里的每一个元素，就是一个示性函数 I_i（第 i 个人是否拿对了帽子）
        indicators = (drawn_hats == correct_hats)
        
        # 将所有示性函数相加，就得到了这一次实验中拿对帽子的总人数 X
        # 对应数学公式：X = I_1 + I_2 + ... + I_n
        total_matches_in_this_sim = np.sum(indicators)
        matches_record[i] = total_matches_in_this_sim
        
    return matches_record

# 运行模拟
results = simulate_hat_matching(NUM_PEOPLE, NUM_SIMULATIONS)

# 计算实际模拟出的期望值（算术平均）
simulated_expectation = np.mean(results)

# 理论期望计算：
# 每个示性函数 E[I_i] = 拿到自己帽子的概率 = 1/N
# E[X] = E[I_1] + E[I_2] + ... + E[I_n] = N * (1/N) = 1
theoretical_expectation = 1.0

print("-" * 30)
print(f"理论期望值 E[X]: {theoretical_expectation:.4f}")
print(f"模拟平均值:      {simulated_expectation:.4f}")
print("-" * 30)

# 绘制结果的直方图
# 统计 0人拿对、1人拿对、2人拿对... 的频率
max_matches = int(np.max(results))
bins = np.arange(-0.5, max_matches + 1.5, 1)

plt.figure(figsize=(8, 5))
plt.hist(results, bins=bins, density=True, alpha=0.7, color='#1F77B4', edgecolor='black')

# 标注期望线
plt.axvline(simulated_expectation, color='red', linestyle='dashed', linewidth=2, 
            label=f'模拟平均值 ({simulated_expectation:.2f})')
plt.axvline(theoretical_expectation, color='black', linestyle='solid', linewidth=1, 
            label=f'理论期望 ({theoretical_expectation})')

plt.title(f"{NUM_PEOPLE}人帽子配对问题：{NUM_SIMULATIONS}次模拟分布", fontsize=14)
plt.xlabel("拿对帽子的人数", fontsize=12)
plt.ylabel("概率频率", fontsize=12)
plt.xticks(range(max_matches + 1))
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()