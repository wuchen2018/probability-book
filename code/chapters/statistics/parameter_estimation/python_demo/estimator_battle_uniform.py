"""
文件名: estimator_battle_uniform.py
功能: 模拟均匀分布下“矩估计”与“最大似然估计”的对决，直观展示无偏性、有效性与均方误差（MSE）。

【这是什么？】
这段代码通过几千次重复实验，模拟了“估计全长”的过程。
它对比了两位选手：
1. 矩估计（2倍均值）：号称“无偏”，但发挥不稳定。
2. 最大似然估计（最大值）：虽然“有偏”（总是低估），但发挥极其稳定。
最终你会看到：在均方误差（MSE）这个终极裁判面前，谁才是赢家。

【怎么用？】
直接运行即可。程序会生成一张对比图，展示两种估计量的分布情况。
你可以尝试修改配置区的 SAMPLE_SIZE（样本量），观察当 n 变大时，两者的表现如何变化。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
TRUE_THETA = 100       # 真实的参数值（比如长廊的总长度）
SAMPLE_SIZE = 5        # 每次实验抽取的样本量 n (尝试改为 5, 20, 100)
NUM_TRIALS = 5000      # 模拟实验的重复次数（次数越多，分布越平滑）
# ---------------------

def run_simulation():
    # 1. 生成实验数据
    # shape=(NUM_TRIALS, SAMPLE_SIZE) 表示我们要进行 NUM_TRIALS 次实验，
    # 每次实验从 0 到 TRUE_THETA 之间随机抽取 SAMPLE_SIZE 个数。
    data = np.random.uniform(0, TRUE_THETA, (NUM_TRIALS, SAMPLE_SIZE))
    
    # 2. 计算矩估计 (Method of Moments)
    # 逻辑：总体均值是 theta/2，所以 theta = 2 * 样本均值
    # axis=1 表示对每一行（每一次实验）求均值
    estimates_mom = 2 * np.mean(data, axis=1)
    
    # 3. 计算最大似然估计 (MLE)
    # 逻辑：认为最合理的 theta 就是样本中观测到的最大值
    estimates_mle = np.max(data, axis=1)
    
    # 4. 计算评估指标
    # 偏差 (Bias): 估计量的平均值 - 真实值
    bias_mom = np.mean(estimates_mom) - TRUE_THETA
    bias_mle = np.mean(estimates_mle) - TRUE_THETA
    
    # 方差 (Variance): 估计量围绕其自身均值的波动程度
    var_mom = np.var(estimates_mom)
    var_mle = np.var(estimates_mle)
    
    # 均方误差 (MSE): 方差 + 偏差的平方
    mse_mom = np.mean((estimates_mom - TRUE_THETA)**2)
    mse_mle = np.mean((estimates_mle - TRUE_THETA)**2)

    # --- 打印裁判结果 ---
    print(f"{'-'*15} 实验报告 (n={SAMPLE_SIZE}) {'-'*15}")
    print(f"真实值 (Theta): {TRUE_THETA}")
    print(f"\n【选手1：矩估计 (2*Mean)】")
    print(f"  平均值: {np.mean(estimates_mom):.2f} (偏差: {bias_mom:.2f}) -> {abs(bias_mom):.2f} 接近 0，验证了无偏性")
    print(f"  方差  : {var_mom:.2f} -> 波动很大")
    print(f"  MSE   : {mse_mom:.2f}")
    
    print(f"\n【选手2：MLE (Max)】")
    print(f"  平均值: {np.mean(estimates_mle):.2f} (偏差: {bias_mle:.2f}) -> 负偏差，说明总是系统性低估")
    print(f"  方差  : {var_mle:.2f} -> 波动极小，非常稳定！")
    print(f"  MSE   : {mse_mle:.2f}")
    
    if mse_mle < mse_mom:
        print(f"\n🏆 最终赢家: MLE (虽然它有偏，但它的总误差更小！)")
    else:
        print(f"\n🏆 最终赢家: 矩估计")

    # --- 绘图可视化 ---
    plot_results(estimates_mom, estimates_mle)

def plot_results(mom, mle):
    plt.figure(figsize=(10, 6))
    
    # 绘制矩估计的分布
    plt.hist(mom, bins=50, alpha=0.5, label='矩估计 (2*Mean)', color='gray', density=True)
    
    # 绘制 MLE 的分布
    plt.hist(mle, bins=50, alpha=0.7, label='MLE (Max)', color='#1F77B4', density=True)
    
    # 绘制真实值参考线
    plt.axvline(TRUE_THETA, color='red', linestyle='--', linewidth=2, label='真实值 (Truth)')
    
    plt.title(f'估计量分布对比 (n={SAMPLE_SIZE})\n矩估计波动大 vs MLE 稳定但低估', fontsize=14)
    plt.xlabel('估计出的参数值')
    plt.ylabel('频率密度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 自动调整显示范围，确保能看到全部波动
    plt.xlim(TRUE_THETA * 0.5, TRUE_THETA * 1.5)
    
    plt.show()

if __name__ == "__main__":
    run_simulation()