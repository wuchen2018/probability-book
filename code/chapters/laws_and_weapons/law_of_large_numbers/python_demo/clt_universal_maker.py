import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

"""
文件名: clt_universal_maker.py
功能: 模拟中心极限定理（CLT），展示任意分布的样本均值如何收敛于正态分布。

【这是什么？】
中心极限定理告诉我们：不管原始数据长得多么“歪瓜裂枣”（偏态、均匀、多峰），
只要我们每次随机抽取 n 个数算平均值，重复很多次，
这些“平均值”的分布形状最终都会变成标准的“钟形曲线”（正态分布）。

【怎么用？】
1. 直接运行代码，你会看到一个画板，展示当 n 分别为 1, 5, 30, 100 时，分布形状的演变。
2. 尝试修改下方【可调整参数配置区】中的 DISTRIBUTION_TYPE，看看指数分布或泊松分布是否也能变成钟形。
"""

# ==========================================
# --- 可调整参数配置区 (Playground) ---
# ==========================================

# 选择原始分布类型：
# 'uniform'     -> 均匀分布 (平顶，像砖头)
# 'exponential' -> 指数分布 (极度偏斜，像滑梯)
# 'poisson'     -> 泊松分布 (离散，像台阶)
DISTRIBUTION_TYPE = 'exponential'

# 样本量列表：我们要观察 n 取不同值时的效果
# 建议：保留 1 (看原始形状) 和一个大数 (看最终收敛)
SAMPLE_SIZES = [1, 5, 30, 100]

# 模拟实验次数：为了画出光滑的直方图，需要足够多的实验数据
# 越大越光滑，但计算越慢
NUM_TRIALS = 10000 

# ==========================================
# --- 核心逻辑区 (Logic) ---
# ==========================================

def get_random_samples(dist_type, size):
    """根据配置生成随机数，并返回理论上的总体均值(mu)和标准差(sigma)"""
    if dist_type == 'uniform':
        # 0到1之间的均匀分布
        data = np.random.uniform(0, 1, size)
        mu = 0.5
        sigma = np.sqrt(1/12)
    elif dist_type == 'exponential':
        # lambda=1 的指数分布
        data = np.random.exponential(1, size)
        mu = 1.0
        sigma = 1.0
    elif dist_type == 'poisson':
        # lambda=3 的泊松分布
        data = np.random.poisson(3, size)
        mu = 3.0
        sigma = np.sqrt(3)
    else:
        raise ValueError("不支持的分布类型，请检查拼写")
    return data, mu, sigma

def main():
    # 设置中文字体（避免乱码），如果报错可尝试改为 'Arial Unicode MS' 或英文
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建画布
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    print(f"正在启动模拟... 当前分布类型: {DISTRIBUTION_TYPE}")

    for i, n in enumerate(SAMPLE_SIZES):
        ax = axes[i]
        
        # --- 步骤 1: 模拟采样过程 ---
        # 我们生成一个矩阵：行数=实验次数(NUM_TRIALS)，列数=每次抽取的样本量(n)
        # 例如：做10000次实验，每次抽30个人
        raw_data, pop_mu, pop_sigma = get_random_samples(DISTRIBUTION_TYPE, (NUM_TRIALS, n))
        
        # --- 步骤 2: 计算样本均值 ---
        # 对每一行求平均值。这就是中心极限定理的主角：X_bar
        sample_means = np.mean(raw_data, axis=1)
        
        # --- 步骤 3: 绘制实验数据的直方图 ---
        # bins=50 表示把数据切成50条，density=True 表示面积归一化（方便和理论曲线对比）
        ax.hist(sample_means, bins=50, density=True, alpha=0.6, color='#1f77b4', label='模拟实验结果')
        
        # --- 步骤 4: 绘制理论正态曲线 (The "Ghost" Curve) ---
        # 根据中心极限定理：
        # 样本均值的期望 = 总体期望 (mu)
        # 样本均值的标准差 = 总体标准差 / sqrt(n)  <-- 注意这里！波动会随着 n 增大而迅速减小
        clt_sigma = pop_mu if n == 0 else pop_sigma / np.sqrt(n)
        
        # 生成平滑的曲线坐标
        x_min, x_max = ax.get_xlim()
        x_axis = np.linspace(x_min, x_max, 1000)
        y_axis = norm.pdf(x_axis, pop_mu, clt_sigma)
        
        ax.plot(x_axis, y_axis, 'r-', lw=2, label='理论正态曲线')
        
        # --- 图表美化 ---
        ax.set_title(f"样本量 n = {n}", fontsize=12)
        ax.set_xlabel("样本均值")
        ax.set_ylabel("概率密度")
        if i == 0:
            ax.legend(loc='upper right')
            
        print(f"进度: 完成 n={n} 的模拟")

    plt.suptitle(f"中心极限定理演示：原始分布为 {DISTRIBUTION_TYPE}", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()