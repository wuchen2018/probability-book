"""
文件名: covariance_visualizer.py
功能: 交互式体验协方差对数据分布形状的影响

【这是什么？】
这段代码带你“看见”协方差。它通过生成二维正态分布的随机数据，
展示了当协方差变化时，数据点云是如何拉伸、旋转和变形的。
这也是理解“相关性”与“线性关系”最直观的数学实验。

【怎么用？】
1. 修改下方的【可调整参数配置区】，特别是 COV_XY (协方差)。
2. 运行脚本，观察弹出的图像中点云的形状。
3. 尝试将协方差设为 0，或者设为接近 sqrt(VAR_X * VAR_Y) 的值，看看会发生什么。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

# --- 可调整参数配置区 (你可以随意修改这里的数值) ---

# 样本数量：模拟多少次实验
N_SAMPLES = 2000

# X 和 Y 的中心位置 (期望 E[X], E[Y])
MEAN_X = 50
MEAN_Y = 50

# X 和 Y 自身的波动程度 (方差 Var(X), Var(Y))
VAR_X = 100  # 标准差是 10
VAR_Y = 100  # 标准差是 10

# X 和 Y 的协同变化程度 (协方差 Cov(X, Y))
# 警告：根据柯西-施瓦茨不等式，协方差的绝对值不能超过 sqrt(VAR_X * VAR_Y)
# 在这个配置下，最大值是 100，最小值是 -100
COV_XY = 85.0

# ------------------------------------------------

def run_simulation():
    # 1. 数学检查：协方差矩阵必须是半正定的
    # 对应数学原理：相关系数 rho 的绝对值不能大于 1
    max_cov = np.sqrt(VAR_X * VAR_Y)
    if abs(COV_XY) > max_cov:
        print(f"【数学警告】: 你设置的协方差 {COV_XY} 太大了！")
        print(f"对于当前的方差设置，协方差必须在 {-max_cov} 到 {max_cov} 之间。")
        print("程序已自动将协方差调整为临界值。")
        cov_val = max_cov * np.sign(COV_XY) * 0.99 # 稍微留点余地防止数值误差
    else:
        cov_val = COV_XY

    # 2. 构建协方差矩阵 (Covariance Matrix)
    # 这是多维随机变量的核心，对角线是方差，非对角线是协方差
    # Matrix = [[Var(X),   Cov(X,Y)],
    #           [Cov(Y,X), Var(Y)]]
    cov_matrix = [[VAR_X, cov_val], 
                  [cov_val, VAR_Y]]

    # 3. 生成数据
    # 利用多维正态分布生成器
    # 对应数学原理：从联合分布 f(x,y) 中进行采样
    means = [MEAN_X, MEAN_Y]
    data = np.random.multivariate_normal(means, cov_matrix, N_SAMPLES)
    x_data, y_data = data.T

    # 4. 计算统计量 (验证理论值与样本值的差异)
    # 对应数学原理：大数定律 (样本量越大，样本协方差越接近理论协方差)
    sample_cov = np.cov(x_data, y_data)[0, 1]
    correlation = sample_cov / (np.std(x_data) * np.std(y_data))

    # --- 绘图可视化 ---
    plt.figure(figsize=(8, 8))
    
    # 绘制散点图
    plt.scatter(x_data, y_data, alpha=0.3, s=10, label='样本点 (Samples)')
    
    # 绘制中心点 (期望向量)
    plt.plot(MEAN_X, MEAN_Y, 'r+', markersize=15, markeredgewidth=3, label='期望重心 E[Z]')

    # 绘制置信椭圆 (Confidence Ellipse)
    # 对应数学原理：协方差矩阵的特征值和特征向量决定了椭圆的长轴和短轴
    # 这部分代码负责画出那个“包围圈”，直观展示数据的分布范围
    pearson = cov_val / np.sqrt(VAR_X * VAR_Y)
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    
    # 计算旋转角度 (45度对应方差相等的情况)
    angle = 45 if VAR_X == VAR_Y else np.degrees(0.5 * np.arctan(2 * cov_val / (VAR_X - VAR_Y)))
    
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, 
                      facecolor='none', edgecolor='red', linestyle='--', linewidth=2)
    
    # 将椭圆缩放并移动到正确位置 (3倍标准差覆盖 99% 的数据)
    scale_x = np.sqrt(VAR_X) * 3
    scale_y = np.sqrt(VAR_Y) * 3 
    
    transf = transforms.Affine2D() \
        .rotate_deg(angle) \
        .scale(scale_x, scale_y) \
        .translate(MEAN_X, MEAN_Y)
    
    ellipse.set_transform(transf + plt.gca().transData)
    plt.gca().add_patch(ellipse)

    # 图表装饰
    title_text = f"协方差 Cov = {cov_val:.1f} (相关系数 ρ ≈ {correlation:.2f})"
    plt.title(title_text, fontsize=14)
    plt.xlabel("随机变量 X", fontsize=12)
    plt.ylabel("随机变量 Y", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.axis('equal') # 保证 X 和 Y 轴刻度一致，这样看到的形状才是真实的
    
    print(f"--- 实验结果 ---")
    print(f"理论协方差: {cov_val}")
    print(f"样本协方差: {sample_cov:.4f}")
    print(f"样本相关系数: {correlation:.4f}")
    print(f"注意观察：正协方差使图像变为'撇'(/)，负协方差使其变为'捺'(\\)。")
    
    plt.show()

if __name__ == "__main__":
    run_simulation()