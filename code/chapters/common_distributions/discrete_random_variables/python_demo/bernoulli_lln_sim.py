import numpy as np
import matplotlib.pyplot as plt

"""
文件名: bernoulli_lln_sim.py
功能: 模拟伯努利实验的大数定律（Law of Large Numbers）收敛过程

【这是什么？】
代码演示了为什么“虽然每次实验结果非0即1，但长期平均值却是一个小数（如0.7）”。
它模拟了成千上万次抛硬币（或投篮），实时计算“当前的成功率”，让你亲眼看到数据是如何从“剧烈波动”逐渐稳定到“数学期望”的。

【怎么用？】
直接运行即可。
你可以修改配置区的 PROBABILITY_SUCCESS（成功率）和 TOTAL_TRIALS（实验次数），
观察参数变化对“稳定速度”的影响。
"""

# --- 可调整参数配置区 ---
PROBABILITY_SUCCESS = 0.7  # 伯努利实验成功的概率 (p)，例如 0.7 代表 70% 命中率
TOTAL_TRIALS = 2000        # 模拟实验的总次数 (n)，次数越多越接近理论值
RANDOM_SEED = 42           # 随机种子，保证每次运行结果一致（想看随机结果可设为 None）

def run_simulation():
    # 设置随机种子，确保可复现性（教学代码常用）
    if RANDOM_SEED is not None:
        np.random.seed(RANDOM_SEED)

    # 1. 生成实验数据
    # np.random.binomial(n=1, p=..., size=...) 就是标准的伯努利分布生成器
    # 结果是一个包含 0 和 1 的数组，代表每一次实验是“失败”还是“成功”
    outcomes = np.random.binomial(n=1, p=PROBABILITY_SUCCESS, size=TOTAL_TRIALS)

    # 2. 计算“跑动平均值” (Running Average)
    # cumsum 是累加函数。例如 outcomes=[1, 0, 1]，cumsum后变成 [1, 1, 2]
    cumulative_successes = np.cumsum(outcomes)
    
    # 生成一个从 1 到 N 的数组，代表当前的实验次数
    trial_indices = np.arange(1, TOTAL_TRIALS + 1)
    
    # 核心数学逻辑：
    # 当前频率 = 截止目前的成功总数 / 截止目前的实验总次数
    # 这就是大数定律中 \bar{X}_n = (X_1 + ... + X_n) / n
    running_averages = cumulative_successes / trial_indices

    # 3. 绘图展示
    plt.figure(figsize=(12, 6))
    
    # 绘制模拟出的“实际频率”曲线
    # 观察：在实验初期（左侧），曲线剧烈震荡；随着次数增加（右侧），曲线趋于平滑
    plt.plot(trial_indices, running_averages, label='Running Average (Actual)', color='#1F77B4', linewidth=1.5)
    
    # 绘制“理论概率”直线 (p)
    # 这是我们的数学期望，也是大数定律收敛的目标
    plt.axhline(y=PROBABILITY_SUCCESS, color='#D62728', linestyle='--', linewidth=2, label=f'Theoretical Expectation (p={PROBABILITY_SUCCESS})')

    # 图表装饰
    plt.title('Law of Large Numbers: Convergence of Bernoulli Trials', fontsize=14)
    plt.xlabel('Number of Trials (n)', fontsize=12)
    plt.ylabel('Proportion of Successes', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 设置y轴范围，让波动看得更清楚 (以 p 为中心上下浮动)
    plt.ylim(0, 1) 
    
    print(f"模拟结束。")
    print(f"设定概率 p: {PROBABILITY_SUCCESS}")
    print(f"最终 {TOTAL_TRIALS} 次实验后的平均值: {running_averages[-1]:.4f}")
    
    plt.show()

if __name__ == "__main__":
    run_simulation()