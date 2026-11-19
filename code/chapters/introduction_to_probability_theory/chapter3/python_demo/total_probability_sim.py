import numpy as np
import matplotlib.pyplot as plt

"""
文件名: total_probability_sim.py
功能: 通过蒙特卡洛模拟揭示全概率公式的物理意义

【这是什么？】
利用计算机模拟成千上万次“两阶段随机试验”（比如先选某个路径/车间，再看目标事件是否发生）。
通过统计最终目标事件发生的总频率，验证它是否与全概率公式计算出的理论加权结果严格一致。

【怎么用？】
直接运行本脚本。程序会在终端输出理论计算值与模拟统计值的对比，
并自动绘制一张折线图，让你直观看到：随着模拟次数的增加，经验频率是如何死死咬住理论全概率的。
"""

# --- 图表中文显示配置 ---
# 设置兼容 Windows/Mac/Linux 的常见中文字体，防止图表出现方块乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'Microsoft YaHei', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False 

# --- 可调整参数配置区 ---
# 第一阶段：完备事件组 B_i 的先验概率（必须非负且和为1）
# 含义：代表不同路径、情境或分类的权重比例
PRIOR_PROBS = [0.5, 0.3, 0.2] 

# 第二阶段：在各个 B_i 发生的条件下，目标事件 A 发生的条件概率 P(A|B_i)
# 含义：代表各个局部情境下的发生风险或成功率
CONDITIONAL_PROBS = [0.01, 0.02, 0.03]

# 模拟的总试验次数（建议调大点，直观感受大数定律的威力）
NUM_SIMULATIONS = 10000
# --------------------------

def main():
    # 数据合法性校验：确保提供的是一个完备事件组
    if not np.isclose(sum(PRIOR_PROBS), 1.0):
        raise ValueError("先验概率之和必须严格为 1，否则无法构成完备事件组！")
    
    num_partitions = len(PRIOR_PROBS)
    
    # 1. 理论计算：使用全概率公式 P(A) = sum( P(B_i) * P(A|B_i) )
    # 对应数学操作：将局部条件概率按其先验权重进行“加权求和”
    theoretical_P_A = sum(p * c for p, c in zip(PRIOR_PROBS, CONDITIONAL_PROBS))
    print(f"【理论值】根据全概率公式严格计算的 P(A) = {theoretical_P_A:.4f}")

    # 2. 开始蒙特卡洛模拟过程
    
    # 模拟第一阶段：根据先验概率 PRIOR_PROBS 随机投点，选择路径 B_i
    # 对应数学操作：在样本空间中发生了一个完备事件组中的某个特定事件
    stage_1_choices = np.random.choice(
        a=num_partitions, 
        size=NUM_SIMULATIONS, 
        p=PRIOR_PROBS
    )

    # 模拟第二阶段：在已经确定的路径 B_i 下，测试目标事件 A 是否发生
    # 先生成一组 0 到 1 之间的均匀分布随机数作为判定标尺
    random_thresholds = np.random.rand(NUM_SIMULATIONS)
    
    # 查表操作：找出每一次试验所对应的局部条件概率 P(A|B_i)
    # 对应数学操作：锁定当前局部情境下的发生概率
    current_conditional_probs = np.array(CONDITIONAL_PROBS)[stage_1_choices]

    # 判定事件 A 是否发生：如果随机数标尺落在了条件概率范围内，则视为发生 (True)
    # 对应数学操作：在给定的 P(A|B_i) 参数下进行伯努利试验（抛硬币）
    event_A_occurred = random_thresholds < current_conditional_probs

    # 3. 统计与可视化
    
    # 统计每一步试验后，事件 A 的累积发生总数
    cumulative_A_counts = np.cumsum(event_A_occurred)
    
    # 计算每一步的动态经验频率：累积发生次数 / 当前已进行的试验总数
    # 对应数学操作：利用大数定律，通过实际发生的频率去逼近真实的概率
    trials = np.arange(1, NUM_SIMULATIONS + 1)
    empirical_frequencies = cumulative_A_counts / trials

    final_empirical_freq = empirical_frequencies[-1]
    print(f"【模拟值】经过 {NUM_SIMULATIONS} 次物理模拟得到的最终经验频率 = {final_empirical_freq:.4f}")
    
    # 绘制频率收敛图
    plt.figure(figsize=(9, 5))
    
    # 画出动态的经验频率震荡曲线
    plt.plot(trials, empirical_frequencies, label='动态经验频率', color='#1F77B4', alpha=0.9, linewidth=1.5)
    
    # 画出全概率公式计算出的绝对基准红线
    plt.axhline(y=theoretical_P_A, color='red', linestyle='--', linewidth=2, label=f'理论全概率 P(A) = {theoretical_P_A:.4f}')
    
    plt.title('全概率公式的蒙特卡洛模拟过程')
    plt.xlabel('试验总次数（对数刻度）')
    plt.ylabel('事件 A 的累积发生频率')
    
    # 横坐标使用对数刻度，能更清楚地放大看到初期的剧烈震荡和后期的逐渐平稳
    plt.xscale('log') 
    
    # 动态调整纵坐标范围以适应不同参数
    upper_limit = min(theoretical_P_A * 2.5, 1.0)
    plt.ylim(0, max(upper_limit, 0.1))
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()