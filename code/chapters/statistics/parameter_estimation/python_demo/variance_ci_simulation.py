"""
文件名: variance_ci_simulation.py
功能: 模拟方差区间估计的“捕获”过程，直观展示卡方分布构成的区间为何能包含真实方差。

【这是什么？】
我们在做区间估计时，总说“95%的置信水平”。但这到底是什么意思？
这段代码让你扮演“上帝”：设定一个真实的总体方差（True Variance），然后模拟 100 次抽样。
你会亲眼看到：每一次算出的区间（那些横线）长短不一，而且是不对称的。
绝大多数区间会“捕获”那条红色的真值线，但总有那么几个倒霉蛋会“脱靶”。

【怎么用？】
直接运行即可。
你将看到一张“瀑布图”：
1. 绿色线条：成功捕获真值的区间。
2. 红色线条：未能捕获真值的区间（犯了错误）。
3. 黑色竖线：真实的总体方差。
尝试修改“样本量”，看看样本越多，区间是不是变得越窄（估计越精确）？
"""

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- 可调整参数配置区 (Playground) ---
TRUE_SIGMA = 5.0          # 上帝视角：真实的总体标准差
SAMPLE_SIZE = 20          # 每次抽样抽多少个零件 (n)
CONFIDENCE_LEVEL = 0.95   # 置信水平 (1-alpha)，通常是 0.95 或 0.90
NUM_TRIALS = 100          # 模拟多少次实验 (画多少条线)
# -----------------------------------

def run_simulation():
    # 1. 准备数据容器
    # 用来记录每一次实验算出的区间下限和上限
    lower_bounds = []
    upper_bounds = []
    captured_status = [] # 记录是否成功捕获 (True/False)

    true_variance = TRUE_SIGMA ** 2
    df = SAMPLE_SIZE - 1  # 自由度 n-1
    
    # 2. 计算卡方分布的关键分位数 (The Keys)
    # 注意：卡方分布不对称，所以要分别算左右两个分位数
    # alpha 是“犯错的概率”
    alpha = 1 - CONFIDENCE_LEVEL
    
    # chi2_lower: 左边的分位数（数值小），对应右尾面积 1-alpha/2
    # chi2_upper: 右边的分位数（数值大），对应右尾面积 alpha/2
    chi2_lower = stats.chi2.ppf(alpha / 2, df)
    chi2_upper = stats.chi2.ppf(1 - alpha / 2, df)
    
    print(f"当前设定：真实方差={true_variance:.2f}, 样本量={SAMPLE_SIZE}")
    print(f"卡方分位数：左={chi2_lower:.2f}, 右={chi2_upper:.2f}")

    # 3. 开始模拟循环
    np.random.seed(42) # 固定随机种子，保证你复现的结果和别人一样
    
    for i in range(NUM_TRIALS):
        # 模拟上帝造物：从正态分布 N(0, sigma^2) 中抽取 n 个样本
        sample_data = np.random.normal(loc=0, scale=TRUE_SIGMA, size=SAMPLE_SIZE)
        
        # 计算样本方差 S^2 (注意：这是点估计)
        # ddof=1 表示除以 n-1，即无偏估计
        s_squared = np.var(sample_data, ddof=1)
        
        # --- 核心数学公式 ---
        # 根据公式：[(n-1)S^2 / chi2_upper, (n-1)S^2 / chi2_lower]
        # 注意：大的分位数 chi2_upper 在分母，算出的是区间的下限
        ci_lower = (df * s_squared) / chi2_upper
        ci_upper = (df * s_squared) / chi2_lower
        
        lower_bounds.append(ci_lower)
        upper_bounds.append(ci_upper)
        
        # 判断：真实的方差是否落在这个区间里？
        is_captured = (ci_lower <= true_variance <= ci_upper)
        captured_status.append(is_captured)

    # 4. 绘图展示
    plt.figure(figsize=(10, 6))
    
    # 绘制每一条置信区间
    for i in range(NUM_TRIALS):
        color = 'green' if captured_status[i] else 'red'
        # 画横线：从下限到上限
        plt.hlines(y=i, xmin=lower_bounds[i], xmax=upper_bounds[i], colors=color, alpha=0.6)
        # 画一个小点表示点估计 S^2 的位置 (可选)
        # plt.scatter((df * lower_bounds[i] * chi2_upper)/df, i, s=5, c='black', alpha=0.3)

    # 绘制真实方差的竖线
    plt.axvline(x=true_variance, color='black', linestyle='-', linewidth=2, label='真实方差 ($\sigma^2$)')
    
    # 图表装饰
    plt.title(f'方差置信区间模拟 (n={SAMPLE_SIZE}, 95%置信度)\n红色代表“未捕获”真值，绿色代表“捕获”', fontsize=12)
    plt.xlabel('方差值 ($\sigma^2$)')
    plt.ylabel('实验次数 (Trial ID)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # 计算实际覆盖率
    actual_coverage = sum(captured_status) / NUM_TRIALS * 100
    print(f"模拟结束：100次实验中，有 {int(actual_coverage)} 次成功捕获了真值。")
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_simulation()