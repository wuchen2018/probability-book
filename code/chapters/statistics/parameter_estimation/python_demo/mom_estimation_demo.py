"""
文件名: mom_estimation_demo.py
功能: 模拟矩估计法（Method of Moments）的收敛过程

【这是什么？】
这段代码直观地展示了“矩估计”是如何工作的。
我们设定一个真实的总体分布（比如均匀分布），然后模拟从里面不断抽取数据。
你会看到，随着样本量 n 的增加，通过样本均值和方差反推出来的参数（估计值），
是如何像被磁铁吸引一样，一步步逼近真实参数的。

【怎么用？】
1. 确保已安装 numpy 和 matplotlib 库。
2. 直接运行脚本。
3. 观察弹出的图表：
   - 上图展示了随着数据变多，估计值震荡收敛到真实值的过程。
   - 下图展示了利用这些估计参数复原出的分布形状与真实数据的对比。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
TRUE_A = 2.0        # 均匀分布的真实下界 (a)
TRUE_B = 10.0       # 均匀分布的真实上界 (b)
MAX_SAMPLES = 2000  # 最大样本量（模拟抽取多少个数据）
SEED = 42           # 随机种子，保证每次运行结果一致（可修改或删除）

# ------------------------------------------------------------------

def run_mom_simulation():
    np.random.seed(SEED)
    
    # 1. 生成“上帝视角”的总体数据
    # 我们假设总体服从均匀分布 U(a, b)
    data = np.random.uniform(TRUE_A, TRUE_B, MAX_SAMPLES)
    
    # 初始化记录数组，用于存放每一个样本量下的估计值
    estimates_a = []
    estimates_b = []
    sample_sizes = np.arange(10, MAX_SAMPLES + 1) # 从10个样本开始，一直增加到最大样本量

    # 2. 模拟“随着样本增加，不断更新估计”的过程
    for n in sample_sizes:
        # 截取前 n 个数据作为当前的“样本”
        current_sample = data[:n]
        
        # --- 核心算法：矩估计法 (Method of Moments) ---
        
        # 第一步：计算样本矩（Sample Moments）
        # 对应数学原理：用样本的一阶原点矩（均值）去匹配总体期望
        sample_mean = np.mean(current_sample)
        
        # 对应数学原理：用样本的二阶中心矩（方差）去匹配总体方差
        # 注意：矩估计通常直接使用 1/n 的有偏方差公式，而非 1/(n-1)
        sample_var = np.var(current_sample) 
        
        # 第二步：解方程组反推参数
        # 对于均匀分布 U(a,b)：
        # 期望 E(X) = (a+b)/2
        # 方差 Var(X) = (b-a)^2 / 12
        # 联立解得：
        # a = Mean - sqrt(3 * Var)
        # b = Mean + sqrt(3 * Var)
        
        half_width = np.sqrt(3 * sample_var)
        
        hat_a = sample_mean - half_width  # 估计出的下界
        hat_b = sample_mean + half_width  # 估计出的上界
        
        estimates_a.append(hat_a)
        estimates_b.append(hat_b)

    # 3. 结果可视化
    plt.figure(figsize=(12, 8))
    
    # 子图1：收敛轨迹
    plt.subplot(2, 1, 1)
    plt.plot(sample_sizes, estimates_a, label=r'Estimated $\hat{a}$', color='blue', alpha=0.6)
    plt.plot(sample_sizes, estimates_b, label=r'Estimated $\hat{b}$', color='green', alpha=0.6)
    
    # 绘制真实值参考线
    plt.axhline(TRUE_A, color='red', linestyle='--', linewidth=2, label=f'True a={TRUE_A}')
    plt.axhline(TRUE_B, color='orange', linestyle='--', linewidth=2, label=f'True b={TRUE_B}')
    
    plt.title(f'Convergence of Method of Moments Estimators (Uniform Distribution)', fontsize=14)
    plt.xlabel('Sample Size (n)', fontsize=12)
    plt.ylabel('Parameter Value', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 子图2：最终拟合效果对比
    plt.subplot(2, 1, 2)
    
    # 绘制数据的直方图
    plt.hist(data, bins=30, density=True, alpha=0.5, color='gray', label='Observed Data Histogram')
    
    # 绘制由于矩估计参数绘制的“理论”密度曲线
    # 使用最后一次迭代（样本量最大时）的估计值
    final_a = estimates_a[-1]
    final_b = estimates_b[-1]
    
    x_vals = np.linspace(min(TRUE_A, final_a) - 1, max(TRUE_B, final_b) + 1, 200)
    
    # 真实的概率密度函数 (PDF)
    true_pdf = np.where((x_vals >= TRUE_A) & (x_vals <= TRUE_B), 1/(TRUE_B-TRUE_A), 0)
    
    # 估计的概率密度函数 (PDF)
    est_pdf = np.where((x_vals >= final_a) & (x_vals <= final_b), 1/(final_b-final_a), 0)
    
    plt.plot(x_vals, true_pdf, 'r--', linewidth=2, label='True Distribution')
    plt.plot(x_vals, est_pdf, 'b-', linewidth=2, label=f'Estimated Distribution (MoM)\n a={final_a:.2f}, b={final_b:.2f}')
    
    plt.title('Final Estimated Distribution vs. True Distribution', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_mom_simulation()