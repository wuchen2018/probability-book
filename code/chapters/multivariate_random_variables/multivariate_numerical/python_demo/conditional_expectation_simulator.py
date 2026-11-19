"""
文件名: conditional_expectation_simulator.py
功能: 模拟“条件期望是一个随机变量”这一核心概念，并验证重期望定律与方差分解公式。

【这是什么？】
这段代码通过生成大量模拟数据，构建了一个双层随机系统：
1. 先随机决定环境 Y（比如选哪个班级）。
2. 再在给定环境 Y 下生成具体数据 X（比如该班级某位同学的分数）。
通过这个过程，我们将直观地看到 E[X|Y] 如何作为一个随机变量在波动，并验证它是否满足 E[E[X|Y]] = E[X]。

【怎么用？】
直接运行即可。控制台会输出理论值与模拟值的对比（验证重期望定律），
还会弹出一张图，对比“原始数据 X”和“条件期望 E[X|Y]”的分布形态。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
N_SAMPLES = 10000       # 模拟样本总数（样本越多，验证结果越接近理论值）
GROUPS = [1, 2, 3]      # 假设变量 Y 有三种取值（例如三个不同的班级）
PROBS = [0.3, 0.5, 0.2] # Y 取这三个值的概率 P(Y=y)

# 定义 X|Y 的分布参数：每个组对应的 (均值, 标准差)
# 组1(Y=1): 均值10, 波动小; 组2(Y=2): 均值20, 波动大; 组3(Y=3): 均值30, 波动中
COND_PARAMS = {
    1: {'mu': 10, 'sigma': 2},
    2: {'mu': 20, 'sigma': 5},
    3: {'mu': 30, 'sigma': 2}
}

def run_simulation():
    # 1. 设置随机种子，保证每次运行结果可复现
    np.random.seed(42)

    # 2. 生成随机变量 Y (环境/条件)
    # 对应数学操作：按照边缘分布 P(Y) 进行采样
    y_samples = np.random.choice(GROUPS, size=N_SAMPLES, p=PROBS)

    # 3. 生成随机变量 X (观测值)
    # 对应数学操作：从条件分布 P(X|Y) 中采样
    x_samples = np.zeros(N_SAMPLES)
    
    # 4. 生成随机变量 E[X|Y] (条件期望)
    # 注意：这是一个随机变量，它的取值依赖于 Y。
    # 如果第 i 个样本的 Y 是 1，那么对应的 E[X|Y] 就是组 1 的理论均值 (10)。
    e_x_given_y_samples = np.zeros(N_SAMPLES)

    for i in range(N_SAMPLES):
        group = y_samples[i]
        mu = COND_PARAMS[group]['mu']
        sigma = COND_PARAMS[group]['sigma']
        
        # 模拟数据生成：X = E[X|Y] + 噪声
        x_samples[i] = np.random.normal(mu, sigma)
        
        # 记录条件期望值：这是我们在已知 Y 时对 X 的最佳猜测
        e_x_given_y_samples[i] = mu

    # --- 验证环节 ---

    # A. 验证重期望定律: E[X] = E[ E[X|Y] ]
    # 理论上的 E[X]
    theoretical_mean = sum(COND_PARAMS[g]['mu'] * p for g, p in zip(GROUPS, PROBS))
    
    # 模拟数据的 E[X] (所有样本的平均)
    sim_mean_x = np.mean(x_samples)
    
    # 模拟数据的 E[ E[X|Y] ] (条件期望这个随机变量的平均)
    sim_mean_e_x_given_y = np.mean(e_x_given_y_samples)

    print(f"--- 重期望定律验证 (Law of Iterated Expectations) ---")
    print(f"理论 E[X]:              {theoretical_mean:.4f}")
    print(f"模拟 E[X]:              {sim_mean_x:.4f}  (X 的总平均)")
    print(f"模拟 E[ E[X|Y] ]:       {sim_mean_e_x_given_y:.4f}  (条件期望的平均)")
    print(f"结论: 两者非常接近，验证成功。\n")

    # B. 验证方差分解公式: Var(X) = E[Var(X|Y)] + Var(E[X|Y])
    # 1. 计算总方差 Var(X)
    total_var = np.var(x_samples)

    # 2. 计算“组间方差” Var(E[X|Y]) -> 可解释的波动
    explained_var = np.var(e_x_given_y_samples)

    # 3. 计算“组内方差的平均” E[Var(X|Y)] -> 不可解释的噪声
    # 这里我们用每个样本对应的理论 sigma^2 来近似 Var(X|Y)
    # 在实际数据中，这通常对应于残差 (X - E[X|Y])^2 的平均值
    unexplained_var_samples = [COND_PARAMS[y]['sigma']**2 for y in y_samples]
    mean_unexplained_var = np.mean(unexplained_var_samples)

    print(f"--- 方差分解验证 (Variance Decomposition) ---")
    print(f"总方差 Var(X):          {total_var:.4f}")
    print(f"组间方差 Var(E[X|Y]):   {explained_var:.4f}  (信号：由 Y 解释的部分)")
    print(f"组内方差 E[Var(X|Y)]:   {mean_unexplained_var:.4f}  (噪声：Y 解释不了的部分)")
    print(f"两者之和:               {explained_var + mean_unexplained_var:.4f}")
    print(f"结论: 分解之和近似等于总方差。\n")

    # --- 可视化 ---
    plot_results(x_samples, e_x_given_y_samples)

def plot_results(x_samples, e_x_given_y_samples):
    plt.figure(figsize=(10, 6))
    
    # 绘制 X 的分布（原本的复杂分布）
    plt.hist(x_samples, bins=50, alpha=0.5, color='gray', label='观测值 X (包含噪声)', density=True)
    
    # 绘制 E[X|Y] 的分布（去噪后的骨架）
    # 注意：这通常是离散的，因为它只取几个固定的均值
    plt.hist(e_x_given_y_samples, bins=50, alpha=0.7, color='blue', label='条件期望 E[X|Y] (去噪信号)', density=True, histtype='step', linewidth=2)
    
    plt.title('可视化：随机变量 X 与其条件期望 E[X|Y] 的分布对比')
    plt.xlabel('数值')
    plt.ylabel('频率密度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 增加说明文本
    plt.text(0.05, 0.9, '注意观察：\n蓝色线(条件期望)大幅减少了波动，\n但它本身依然是一个随机变量，\n因为它随着组别(Y)的变化而跳变。', 
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.show()

if __name__ == "__main__":
    run_simulation()