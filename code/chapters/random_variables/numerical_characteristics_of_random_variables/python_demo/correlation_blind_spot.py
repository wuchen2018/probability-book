"""
文件名: correlation_blind_spot.py
功能: 揭示皮尔逊相关系数的“盲区”：不相关并不意味着独立

【这是什么？】
皮尔逊相关系数本质上是一个“线性关系探测雷达”。这段代码通过生成两组截然不同的数据：
一组是带有噪声的线性关系，另一组是完美的对称非线性关系（如抛物线）。
通过逐步拆解并计算它们的协方差和相关系数，直观展示为何存在100%确定性函数关系的数据，相关系数却依然会“失明”显示为0。

【怎么用？】
直接运行脚本。程序会在控制台输出两组数据的逐步计算过程（均值、协方差、标准差、相关系数），
并弹出一张包含两个散点图的对比面板。
建议尝试修改配置区中的“非线性函数类型”（例如改为绝对值或余弦函数），观察“雷达”对不同规律的反应。
"""

import numpy as np
import matplotlib.pyplot as plt

# 兼容中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] # Windows和Mac的中文字体
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
# 样本数量：样本越多，大数定律让计算结果越接近理论期望值
SAMPLE_SIZE = 1000

# X 的取值范围：默认从 -10 到 10
X_MIN = -10
X_MAX = 10

# 线性关系的参数
LINEAR_SLOPE = 2.0    # 线性斜率，正数代表正相关，负数代表负相关
LINEAR_NOISE = 5.0    # 线性扰动（噪声）的大小：值越大，数据越发散，相关系数越偏离 1 或 -1

# 非线性关系的噪声
NONLINEAR_NOISE = 0.0 # 设为0代表绝对的确定性函数关系，你也可以尝试加点噪声

# --- 核心计算逻辑区 ---

def calculate_correlation(x, y, label="数据"):
    """
    手动逐步计算相关系数，还原数学公式背后的每一个物理动作
    """
    print(f"\n[{label}] 开始计算...")
    
    # 步骤 1：寻找重力中心 —— 计算期望（此处用样本均值代替数学期望 E[X] 和 E[Y]）
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    
    # 步骤 2：数据中心化 —— 计算偏差 (X - E[X]) 和 (Y - E[Y])
    # 这一步相当于把坐标系的原点移动到了数据群的中心
    x_centered = x - mu_x
    y_centered = y - mu_y
    
    # 步骤 3：捕捉协同波动 —— 计算协方差 Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
    # 将 X 和 Y 的偏离值逐个相乘，然后求平均。
    # 如果经常同号，乘积为正，协方差为正；如果一正一负，协方差为负；如果正负乱序对称，均值为0。
    covariance = np.mean(x_centered * y_centered)
    
    # 步骤 4：衡量自身波动 —— 计算标准差（方差的平方根）
    # Var(X) = E[(X - E[X])^2]，标准差 sigma_x = sqrt(Var(X))
    var_x = np.mean(x_centered**2)
    var_y = np.mean(y_centered**2)
    sigma_x = np.sqrt(var_x)
    sigma_y = np.sqrt(var_y)
    
    # 步骤 5：剥离量纲的标尺 —— 计算相关系数 rho = Cov(X, Y) / (sigma_x * sigma_y)
    # 将协方差除以两者的波动幅度，将其强行压缩到 [-1, 1] 的区间内
    correlation = covariance / (sigma_x * sigma_y)
    
    print(f"  -> 协方差 (Cov) : {covariance:.4f}")
    print(f"  -> 相关系数 (rho) : {correlation:.4f}")
    
    return correlation

# --- 1. 生成数据 ---
# 生成均匀分布的 X
x_data = np.random.uniform(X_MIN, X_MAX, SAMPLE_SIZE)

# 生成线性关系数据：Y = aX + b + 噪声
y_linear = LINEAR_SLOPE * x_data + np.random.normal(0, LINEAR_NOISE, SAMPLE_SIZE)

# 生成非线性关系数据：Y = X^2 + 噪声 (完全确定的二次函数规律)
y_nonlinear = x_data**2 + np.random.normal(0, NONLINEAR_NOISE, SAMPLE_SIZE)

# --- 2. 验证与计算 ---
corr_lin = calculate_correlation(x_data, y_linear, "线性关系数据")
corr_nonlin = calculate_correlation(x_data, y_nonlinear, "非线性(二次函数)关系数据")

# --- 3. 结果可视化 ---
# 绘制图表，直观对比“散点形状”与“雷达读数”的差异
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 绘制线性关系
ax1.scatter(x_data, y_linear, alpha=0.5, color='#1F77B4')
ax1.set_title(f"线性关系\n相关系数 $\\rho$ = {corr_lin:.2f}", fontsize=14)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.axhline(np.mean(y_linear), color='black', linestyle='--', alpha=0.3)
ax1.axvline(np.mean(x_data), color='black', linestyle='--', alpha=0.3)

# 绘制非线性关系
ax2.scatter(x_data, y_nonlinear, alpha=0.5, color='#D62728')
ax2.set_title(f"完全确定的非线性关系 ($Y=X^2$)\n相关系数 $\\rho$ = {corr_nonlin:.2f}", fontsize=14)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.axhline(np.mean(y_nonlinear), color='black', linestyle='--', alpha=0.3)
ax2.axvline(np.mean(x_data), color='black', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()