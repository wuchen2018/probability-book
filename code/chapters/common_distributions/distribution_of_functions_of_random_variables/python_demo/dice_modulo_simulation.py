"""
文件名: dice_modulo_simulation.py
功能: 模拟双骰子求和取余的游戏，验证概率分布的不均匀性

【这是什么？】
这段代码演示了离散随机变量变换的核心机制：概率的“重新分配”与“合并”。
我们模拟掷两个骰子，算出点数和，再对 4 取余数。
你会亲眼看到，原本均匀的骰子点数，经过这一系列数学变换（函数映射）后，
是如何因为“殊途同归”（不同的和对应同一个余数）而导致某些结果出现的概率显著高于其他结果的。

【怎么用？】
直接运行即可。
1. 控制台会输出理论计算概率与 100,000 次模拟结果的对比表格。
2. 程序会弹出一张柱状图，直观展示“模拟数据”是如何逼近“理论真值”的。
建议尝试修改配置区的 SIDES（面数）或 MODULUS（除数），看看规则改变后，游戏是否变得公平。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
TRIALS = 100000      # 模拟实验次数（建议至少 10000 次以保证精度）
SIDES = 6            # 骰子的面数（标准骰子为 6）
MODULUS = 4          # 取余数的除数（麻将规则通常为 4）
# ---------------------

def run_simulation():
    # 为了支持中文显示，设置字体（根据系统自动回退）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif'] 
    plt.rcParams['axes.unicode_minus'] = False 

    print(f"--- 开始模拟：掷 {TRIALS} 次双{SIDES}面骰子，对 {MODULUS} 取余 ---")
    
    # 1. 模拟过程：生成随机数据
    # numpy.random.randint(low, high) 生成的范围是 [low, high)，所以要写 SIDES + 1
    # 对应数学原理：生成两个独立的离散均匀分布 X1, X2
    dice1 = np.random.randint(1, SIDES + 1, size=TRIALS)
    dice2 = np.random.randint(1, SIDES + 1, size=TRIALS)
    
    # 对应数学原理：随机变量的函数变换 Z = g(X1, X2) = X1 + X2
    total_sum = dice1 + dice2
    
    # 对应数学原理：进一步变换 Y = h(Z) = Z mod M
    # 这就是核心的“多对一”映射：多个不同的点数和，会“坍缩”到同一个余数上
    remainders = total_sum % MODULUS

    # 2. 统计模拟频率
    # 统计每个余数出现了多少次
    sim_counts = np.bincount(remainders, minlength=MODULUS)
    # 计算频率（模拟概率） = 频数 / 总试验次数
    # 根据大数定律，当 N 足够大时，频率收敛于概率
    sim_probs = sim_counts / TRIALS

    # 3. 计算理论概率（穷举法）
    # 对应数学原理：通过遍历样本空间计算 P(Y=y) = Σ P(X=x)
    theory_counts = np.zeros(MODULUS)
    total_combinations = SIDES * SIDES # 样本空间大小
    
    # 遍历所有可能的 (d1, d2) 组合
    for d1 in range(1, SIDES + 1):
        for d2 in range(1, SIDES + 1):
            s = d1 + d2
            r = s % MODULUS
            # 对应数学原理：概率质量的合并 (Merging Probability Mass)
            # 每发现一种组合 (d1, d2) 映射到 r，就给 r 增加 1/total 的概率
            theory_counts[r] += 1
            
    theory_probs = theory_counts / total_combinations

    # 4. 输出对比结果到控制台
    print(f"{'余数':<10} {'理论概率':<15} {'模拟频率':<15} {'误差':<10}")
    print("-" * 55)
    for r in range(MODULUS):
        diff = abs(theory_probs[r] - sim_probs[r])
        print(f"{r:<12} {theory_probs[r]:.4f}          {sim_probs[r]:.4f}          {diff:.4f}")
        
    return sim_probs, theory_probs

def plot_results(sim_probs, theory_probs):
    """绘制对比图"""
    plt.figure(figsize=(10, 6))
    x = np.arange(MODULUS)
    
    # 绘制柱状图（模拟数据）
    plt.bar(x, sim_probs, alpha=0.6, color='#1f77b4', label=f'模拟结果 ({TRIALS}次)')
    
    # 绘制折线图（理论真值）
    # 红色虚线代表数学计算出的“完美分布”
    plt.plot(x, theory_probs, 'ro--', linewidth=2, markersize=8, label='数学理论值')
    
    # 图表装饰
    plt.title(f'双{SIDES}面骰子点数和对 {MODULUS} 取余的分布', fontsize=14)
    plt.xlabel('余数数值 (Result)', fontsize=12)
    plt.ylabel('出现概率 (Probability)', fontsize=12)
    plt.xticks(x)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 标注最高和最低概率
    max_idx = np.argmax(theory_probs)
    min_idx = np.argmin(theory_probs)
    
    plt.annotate(f'最有利 (P={theory_probs[max_idx]:.3f})', 
                 xy=(max_idx, theory_probs[max_idx]), 
                 xytext=(max_idx, theory_probs[max_idx]+0.02),
                 ha='center', color='red', fontweight='bold', arrowprops=dict(arrowstyle='->', color='red'))
                 
    plt.annotate(f'最不利 (P={theory_probs[min_idx]:.3f})', 
                 xy=(min_idx, theory_probs[min_idx]), 
                 xytext=(min_idx, theory_probs[min_idx]-0.02),
                 ha='center', color='green', fontweight='bold', arrowprops=dict(arrowstyle='->', color='green'))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    s_probs, t_probs = run_simulation()
    plot_results(s_probs, t_probs)