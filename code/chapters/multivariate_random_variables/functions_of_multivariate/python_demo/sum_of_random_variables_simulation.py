"""
文件名: sum_of_random_variables_simulation.py
功能: 模拟两个独立随机变量相加的过程，验证“卷积”对分布形状的影响。

【这是什么？】
这段代码通过“蒙特卡洛模拟”（也就是暴力掷骰子）来演示概率论中一个反直觉的现象：
两个“平顶”的均匀分布加在一起，为什么会变成一个“尖顶”的三角分布？
两个正态分布加在一起，为什么还是正态分布？
它让你亲眼看到，随着实验次数增加，数据的柱状图是如何一步步逼近理论公式推导出的曲线的。

【怎么用？】
直接运行即可。程序会弹出两个窗口：
1. 展示两个均匀分布相加的结果（验证三角分布）。
2. 展示两个正态分布相加的结果（验证正态分布的可加性）。
你可以在下方的配置区修改样本数量，观察“大数定律”的力量。
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# --- 可调整参数配置区 ---
N_SAMPLES = 100000      # 模拟实验的次数（数值越大，柱状图越平滑，越接近理论曲线）
BINS = 100              # 直方图的柱子数量（分辨率）

# 均匀分布参数
UNIFORM_LOW = 0.0       # 均匀分布下界
UNIFORM_HIGH = 1.0      # 均匀分布上界

# 正态分布参数
NORMAL_MU = 0.0         # 均值
NORMAL_SIGMA = 1.0      # 标准差
# ---------------------

def set_plot_style():
    """设置绘图风格，支持中文显示（如果有字体问题会自动降级）"""
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    try:
        # 尝试启用常见的支持中文的字体，防止乱码
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    except:
        pass
    plt.rcParams['axes.unicode_minus'] = False

def demo_uniform_sum():
    """
    演示 1：两个均匀分布之和 X + Y
    理论结果：应该产生一个三角分布
    """
    print(f"正在模拟 {N_SAMPLES} 次均匀分布相加实验...")
    
    # 1. 生成数据（模拟上帝掷骰子）
    # np.random.uniform 对应数学中的 X ~ U(a, b)
    X = np.random.uniform(UNIFORM_LOW, UNIFORM_HIGH, N_SAMPLES)
    Y = np.random.uniform(UNIFORM_LOW, UNIFORM_HIGH, N_SAMPLES)
    
    # 2. 计算和（模拟变换 Z = X + Y）
    # 在代码中，这是两个数组对应元素相加，对应数学中“随机变量的和”
    Z = X + Y
    
    # 3. 绘制实验结果（直方图）
    # density=True 确保面积为1，从而能与概率密度函数(PDF)进行对比
    plt.figure()
    plt.hist(Z, bins=BINS, density=True, alpha=0.6, color='#1F77B4', label='模拟实验数据 (Histogram)')
    
    # 4. 绘制理论曲线（验证推导是否正确）
    # 我们知道 U(0,1)+U(0,1) 的理论分布是三角分布
    # 定义域是 [0, 2]，顶点在 1
    z_values = np.linspace(0, 2, 200)
    # 使用 numpy 的 clip 实现三角波函数：f(z) = 1 - |z - 1| (在0到2之间)
    pdf_values = np.clip(1 - np.abs(z_values - 1), 0, 1)
    
    plt.plot(z_values, pdf_values, 'r--', linewidth=2, label='理论密度曲线 (PDF)')
    
    plt.title(f'均匀分布之和的模拟 (n={N_SAMPLES})', fontsize=14)
    plt.xlabel('Z = X + Y 的取值')
    plt.ylabel('概率密度')
    plt.legend()
    plt.text(0.1, 0.8, "直觉破坏：\n两个平平的分布相加，\n竟然变成了尖尖的形状！", 
             transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

def demo_normal_sum():
    """
    演示 2：两个正态分布之和 X + Y
    理论结果：仍然是正态分布 N(μ1+μ2, σ1^2+σ2^2)
    """
    print(f"正在模拟 {N_SAMPLES} 次正态分布相加实验...")
    
    # 1. 生成数据
    # X ~ N(0, 1), Y ~ N(0, 1)
    X = np.random.normal(NORMAL_MU, NORMAL_SIGMA, N_SAMPLES)
    Y = np.random.normal(NORMAL_MU, NORMAL_SIGMA, N_SAMPLES)
    
    # 2. 计算和
    Z = X + Y
    
    # 3. 绘制实验结果
    plt.figure()
    plt.hist(Z, bins=BINS, density=True, alpha=0.6, color='#2CA02C', label='模拟实验数据 (Histogram)')
    
    # 4. 绘制理论曲线
    # 理论推导：E(Z) = 0+0=0, Var(Z) = 1+1=2 => Std(Z) = sqrt(2)
    new_mu = NORMAL_MU + NORMAL_MU
    new_sigma = np.sqrt(NORMAL_SIGMA**2 + NORMAL_SIGMA**2)
    
    z_values = np.linspace(min(Z), max(Z), 200)
    pdf_values = stats.norm.pdf(z_values, new_mu, new_sigma)
    
    plt.plot(z_values, pdf_values, 'r--', linewidth=2, label=f'理论密度曲线 N(0, 2)')
    
    plt.title(f'正态分布之和的模拟 (n={N_SAMPLES})', fontsize=14)
    plt.xlabel('Z = X + Y 的取值')
    plt.ylabel('概率密度')
    plt.legend()
    plt.text(0.05, 0.8, "稳定性验证：\n正态加正态，还是正态。\n这就是“血统纯正”！", 
             transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

if __name__ == "__main__":
    set_plot_style()
    demo_uniform_sum()
    demo_normal_sum()
    print("绘图完成！请查看弹出的窗口。")
    plt.show()