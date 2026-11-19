"""
文件名: linear_regression_viz.py
功能: 模拟一元线性回归的两种求解过程：解析解（上帝视角）vs 梯度下降（探险家视角）

【这是什么？】
这段代码不仅仅是画一条线。它展示了“机器学习”最核心的过程——从错误的预测开始，
通过不断计算“梯度”（坡度），一步步修正参数，最终逼近真理。
你可以直观地看到直线是如何在迭代中“扭动”并最终拟合数据的。

【怎么用？】
直接运行即可。
1. console 会输出每一步的训练损失，让你看到误差是如何下降的。
2. 弹出的窗口会展示两张图：
   - 上图：原始数据点 + 最终拟合直线（红色） + 学习过程中的中间直线（浅灰色）。
   - 下图：损失函数（MSE）随迭代次数下降的曲线，这就是机器“学习”的轨迹。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 (Playground) ---
# 真实世界的规律（上帝视角）
TRUE_BETA_0 = 5.0      # 真实的截距
TRUE_BETA_1 = 3.0      # 真实的斜率
NOISE_LEVEL = 2.0      # 数据的噪点程度（随机误差 epsilon 的标准差）
SAMPLE_SIZE = 100      # 样本数据点的数量

# 机器的学习参数（探险家视角）
LEARNING_RATE = 0.01   # 学习率 (eta)：步子太大容易扯着蛋（发散），太小走得慢
EPOCHS = 1000          # 迭代次数：探险家尝试下山的步数
VISUALIZE_STEP = 50    # 每隔多少步在图中画一条“中间状态”的线（用于展示学习过程）

# ---------------------------------------------------------

def generate_data(n, b0, b1, noise_std):
    """
    生成模拟数据：Y = b0 + b1*X + epsilon
    """
    np.random.seed(42) # 固定随机种子，保证每次运行结果一致
    X = 2 * np.random.rand(n, 1) # 生成 0到2 之间的随机 X
    epsilon = np.random.randn(n, 1) * noise_std # 生成符合正态分布的噪音
    Y = b0 + b1 * X + epsilon
    return X, Y

def analytical_solution(X, Y):
    """
    解析解（最小二乘法公式）：一步到位求出最优解
    对应公式：b1 = S_xy / S_xx
    """
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    
    # 分子：S_xy (协方差的分子)
    numerator = np.sum((X - X_mean) * (Y - Y_mean))
    # 分母：S_xx (方差的分子)
    denominator = np.sum((X - X_mean) ** 2)
    
    b1 = numerator / denominator
    b0 = Y_mean - b1 * X_mean
    return b0, b1

def gradient_descent(X, Y, lr, epochs):
    """
    梯度下降法：模拟探险家一步步摸索下山的过程
    """
    # 1. 随机初始化参数（就像探险家被随机扔到了山上某处）
    b0 = np.random.randn()
    b1 = np.random.randn()
    
    n = len(Y)
    loss_history = [] # 记录每一步的损失，用于画图
    param_history = [] # 记录每一步的参数，用于画中间状态的线
    
    print(f"--- 开始训练 (学习率: {lr}) ---")
    
    for epoch in range(epochs):
        # --- 前向传播：利用当前参数进行预测 ---
        # 对应数学公式：Y_hat = b0 + b1 * X
        Y_pred = b0 + b1 * X
        
        # --- 计算残差 ---
        # 对应数学公式：error = Y - Y_hat
        error = Y - Y_pred
        
        # --- 计算损失 (MSE) ---
        # 对应数学公式：Loss = (1/n) * sum(error^2)
        loss = (1/n) * np.sum(error**2)
        loss_history.append(loss)
        
        # --- 反向传播：计算梯度 (坡度) ---
        # 这里的 2/n 系数源于对 MSE 求导 (x^2 求导变成 2x)
        # 梯度 = 损失函数对参数的偏导数
        grad_b0 = -(2/n) * np.sum(error)         # 对 b0 求导
        grad_b1 = -(2/n) * np.sum(error * X)     # 对 b1 求导
        
        # --- 更新参数 (迈出一步) ---
        # 新参数 = 旧参数 - 学习率 * 梯度
        # 减号意味着沿着梯度的反方向（下坡方向）走
        b0 = b0 - lr * grad_b0
        b1 = b1 - lr * grad_b1
        
        # 记录中间状态用于绘图
        if epoch % VISUALIZE_STEP == 0:
            param_history.append((b0, b1))
            print(f"Epoch {epoch}: Loss = {loss:.4f}, b0={b0:.2f}, b1={b1:.2f}")
            
    return b0, b1, loss_history, param_history

def main():
    # 1. 准备数据
    X, Y = generate_data(SAMPLE_SIZE, TRUE_BETA_0, TRUE_BETA_1, NOISE_LEVEL)
    
    # 2. 方法一：解析解 (数学公式直接算)
    b0_exact, b1_exact = analytical_solution(X, Y)
    print(f"\n【解析解】上帝视角算出: b0={b0_exact:.4f}, b1={b1_exact:.4f}")
    
    # 3. 方法二：梯度下降 (迭代优化)
    b0_gd, b1_gd, loss_hist, param_hist = gradient_descent(X, Y, LEARNING_RATE, EPOCHS)
    print(f"【梯度下降】探险家最终走到: b0={b0_gd:.4f}, b1={b1_gd:.4f}")
    
    # --- 绘图展示 ---
    plt.figure(figsize=(10, 8))
    
    # 子图1：拟合过程可视化
    plt.subplot(2, 1, 1)
    plt.scatter(X, Y, color='blue', alpha=0.5, label='真实数据点 (含噪)')
    
    # 画出中间过程的线 (浅色)
    x_range = np.array([X.min(), X.max()])
    for i, (p_b0, p_b1) in enumerate(param_hist):
        y_range = p_b0 + p_b1 * x_range
        # 颜色逐渐变深，代表学习过程
        alpha_val = 0.1 + 0.8 * (i / len(param_hist))
        label = "学习过程" if i == 0 else ""
        plt.plot(x_range, y_range, color='gray', alpha=alpha_val, linestyle='--', label=label)
        
    # 画出最终拟合结果 (红色)
    plt.plot(x_range, b0_gd + b1_gd * x_range, color='red', linewidth=3, label='最终拟合直线')
    plt.title(f"线性回归：从懵懂到精通 (Epochs={EPOCHS}, LR={LEARNING_RATE})")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # 子图2：损失函数下降曲线
    plt.subplot(2, 1, 2)
    plt.plot(loss_hist, color='green', linewidth=2)
    plt.title("学习曲线：损失函数 (Loss) 随迭代次数的变化")
    plt.xlabel("迭代次数 (Epoch)")
    plt.ylabel("均方误差 (MSE)")
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()