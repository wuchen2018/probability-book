"""
文件名: p_hacking_demo.py
功能: 模拟“数据挖掘/P值操控”过程，展示为什么反复尝试直到显著（P-Hacking）会破坏统计结论。

【这是什么？】
这段代码带你体验一个“不诚实”的研究员是如何工作的：
哪怕面对一枚完全公平的硬币（原假设 H0 为真），只要我们允许自己“不满意就重做”，
最终一定能“凑”出一个 P < 0.05 的显著结果，从而得出错误的结论（犯第一类错误）。

【怎么用？】
直接运行代码。
1. 程序会模拟一个“执着”的研究员，不断抛硬币，直到 P值小于 0.05 为止。
2. 程序最后会画图展示：如果 10000 个研究员都做这个实验，会有多少人纯靠运气“中奖”。
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 显著性水平（你是多么容易感到“惊讶”？通常设为 0.05）
ALPHA = 0.05

# 每次实验抛硬币的次数（例如：每次抛10下）
N_TRIALS = 10

# 硬币的真实正面概率（0.5 代表完全公平，H0 为真）
# 你可以改成 0.5 以外的值，看看真正的作弊硬币表现如何
TRUE_PROBABILITY = 0.5

# P-Hacking 的最大尝试次数（为了凑出结果，你愿意试多少次？）
MAX_ATTEMPTS = 100

# --- 字体设置（为了支持中文显示） ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False

def simulate_one_experiment(n_trials, true_prob):
    """
    模拟一次抛硬币实验
    返回：正面次数，P值
    """
    # 1. 生成数据：模拟抛 n 次硬币的结果 (1=正面, 0=反面)
    # 这里的 random.binomial 模拟了现实世界的随机性
    outcomes = np.random.binomial(n=1, p=true_prob, size=n_trials)
    n_heads = np.sum(outcomes)
    
    # 2. 计算 P值：假设检验的核心
    # 这里的 binomtest 是在问：
    # "如果硬币是公平的(p=0.5)，出现当前正面次数(或更极端)的概率是多少？"
    # alternative='two-sided' 表示我们关心两端的极端（太多或太少都算异常）
    res = stats.binomtest(k=n_heads, n=n_trials, p=0.5, alternative='two-sided')
    
    return n_heads, res.pvalue

print(f"--- 开始模拟：寻找那个“幸运”的假阳性 ---")
print(f"设定：硬币是公平的，但我们要试到它“看起来不公平”为止。\n")

found_significant = False

# 开始“数据挖掘”循环
for i in range(1, MAX_ATTEMPTS + 1):
    heads, p_val = simulate_one_experiment(N_TRIALS, TRUE_PROBABILITY)
    
    # 打印部分过程（避免刷屏）
    if i <= 5 or p_val < ALPHA:
        status = "显著！(找到证据了)" if p_val < ALPHA else "不显著 (失败)"
        print(f"第 {i:3d} 次尝试: 正面 {heads} 次, P值 = {p_val:.4f} -> {status}")
    
    # 核心判断：如果 P值 < Alpha，立刻停止并宣布“成功”
    # 这就是 P-Hacking 的本质：只保留有利的结果
    if p_val < ALPHA:
        print(f"\n>>> 成功！在第 {i} 次尝试中，我们得到了 P < {ALPHA}。")
        print(f">>> 结论：我们可以写论文宣称“这枚硬币不公平”了。")
        print(f">>> 真相：硬币其实是公平的，我们只是犯了“第一类错误”。")
        found_significant = True
        break

if not found_significant:
    print(f"\n>>> 尝试了 {MAX_ATTEMPTS} 次都没凑出显著结果。看来运气实在太差了。")

print("\n" + "="*50 + "\n")

# --- 进阶视角：上帝视角看 Alpha ---
# 如果我们不作弊，而是诚实地做一次实验，到底有多大概率犯错？
print(f"--- 进阶模拟：上帝视角 ---")
print(f"模拟 10,000 个诚实的研究员，每人只做一次实验...")

n_researchers = 10000
all_p_values = []

for _ in range(n_researchers):
    _, p = simulate_one_experiment(N_TRIALS, TRUE_PROBABILITY)
    all_p_values.append(p)

all_p_values = np.array(all_p_values)
# 计算有多少人的 P值 小于 Alpha
false_positives = np.sum(all_p_values < ALPHA)
rate = false_positives / n_researchers

print(f"结果：有 {false_positives} 个研究员得出了“硬币不公平”的错误结论。")
print(f"犯错比例：{rate:.2%} (理论上应接近 {ALPHA:.0%})")
print(f"启示：这就是显著性水平(Alpha)的真实含义——我们不得不容忍的犯错配额。")

# 绘图
plt.figure(figsize=(10, 6))
plt.hist(all_p_values, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(ALPHA, color='red', linestyle='--', label=f'显著性水平 Alpha = {ALPHA}')
plt.title('H0为真（硬币公平）时，P值的分布直方图')
plt.xlabel('P值')
plt.ylabel('出现频次')
plt.legend()
plt.text(0.5, n_researchers*0.05, '注意：P值在 [0,1] 上是均匀分布的\n任何一次实验都有 5% 的概率落入左边的红线区', 
         ha='center', fontsize=12, color='darkblue')
plt.tight_layout()
plt.show()