# -*- coding: utf-8 -*-
"""
文件名: sgd_random_walk_demo.py
功能: 模拟并对比“批量梯度下降(BGD)”与“随机梯度下降(SGD)”在优化景观上的路径差异

【这是什么？】
这段代码直观展示了机器学习训练中“全量数据”与“小批量随机数据”的区别。
我们将一个损失函数想象成连绵的山峦，优化的目标是找到最低的山谷。
你会看到：BGD 像是一个清醒的登山者，走直线但缓慢；SGD 像是一个醉汉，虽然步履蹒跚（随机震荡），但最终也能跌跌撞撞地滚向山谷底。

【怎么用？】
直接运行即可。程序会生成一张对比图，展示两条不同的下山路径。
你可以尝试修改配置区的“噪声强度”，观察当随机性过大时，醉汉是否会“走丢”。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 (Playground) ---
LEARNING_RATE = 0.05    # 学习率 (步长)：决定了每一步跨多大
STEPS = 50              # 迭代次数：也就是我们要走多少步
NOISE_LEVEL = 3.0       # 噪声强度：模拟 SGD 中“小批量”带来的随机性。数值越大，代表 batch_size 越小，随机性越强
START_POINT = [-2.0, 1.0] # 起始位置 (x, y)

# 为了防止中文乱码，设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------------------------------------

def loss_function(x, y):
    """
    定义一个不对称的损失函数面（类似一个椭圆形的碗）。
    f(x, y) = x^2 + 5y^2
    """
    return x**2 + 5 * y**2

def true_gradient(x, y):
    """
    计算真实的梯度（数学上的最优方向）。
    对应：看完所有训练数据后算出的精确方向。
    """
    grad_x = 2 * x
    grad_y = 10 * y
    return np.array([grad_x, grad_y])

def get_stochastic_gradient(x, y, noise_scale):
    """
    获取随机梯度。
    原理：在真实梯度上叠加高斯白噪声。
    对应：只看了一小撮（Mini-batch）数据，导致方向算得不准，带有随机误差。
    """
    true_grad = true_gradient(x, y)
    # 生成随机噪声，服从正态分布 N(0, noise_scale)
    # 这模拟了大数定律中的“单次抽样具有偶然性”
    noise = np.random.normal(0, noise_scale, size=2)
    return true_grad + noise

def simulate_path(mode='bgd'):
    """
    模拟优化路径
    mode: 'bgd' (批量梯度下降) 或 'sgd' (随机梯度下降)
    """
    path = [np.array(START_POINT)]
    current_pos = np.array(START_POINT)
    
    for _ in range(STEPS):
        x, y = current_pos
        
        if mode == 'bgd':
            # BGD: 沿着最精确的梯度方向走
            grad = true_gradient(x, y)
        else:
            # SGD: 沿着带噪声的梯度方向走
            # 这里体现了“无偏估计”：虽然单次方向是歪的，但长期期望是准的
            grad = get_stochastic_gradient(x, y, NOISE_LEVEL)
        
        # 更新参数：位置 = 旧位置 - 学习率 * 梯度
        current_pos = current_pos - LEARNING_RATE * grad
        path.append(current_pos)
        
    return np.array(path)

# --- 绘图主逻辑 ---
def plot_landscape():
    # 1. 创建网格数据，用于画等高线背景
    x_range = np.linspace(-2.5, 2.5, 100)
    y_range = np.linspace(-1.5, 1.5, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = loss_function(X, Y)

    plt.figure(figsize=(10, 6))
    
    # 画等高线 (地形图)
    plt.contour(X, Y, Z, levels=20, cmap='gray_r', alpha=0.4)
    
    # 2. 模拟并绘制 BGD 路径
    path_bgd = simulate_path(mode='bgd')
    plt.plot(path_bgd[:, 0], path_bgd[:, 1], 'b-o', label='批量梯度下降 (全量数据)', linewidth=2, markersize=4)
    
    # 3. 模拟并绘制 SGD 路径
    path_sgd = simulate_path(mode='sgd')
    plt.plot(path_sgd[:, 0], path_sgd[:, 1], 'r--x', label='随机梯度下降 (小批量)', linewidth=1, markersize=4)
    
    # 标记起点和终点（理论最优解在 0,0）
    plt.plot(START_POINT[0], START_POINT[1], 'k*', markersize=15, label='起点')
    plt.plot(0, 0, 'g*', markersize=15, label='谷底 (最优解)')

    plt.title(f"优化路径对比: 清醒的BGD vs 醉酒的SGD (噪声强度={NOISE_LEVEL})")
    plt.xlabel("参数 w1")
    plt.ylabel("参数 w2")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    print(f"模拟完成。")
    print(f"BGD 最终位置: {path_bgd[-1]}")
    print(f"SGD 最终位置: {path_sgd[-1]}")
    print("提示：SGD 虽然路径曲折，但通常也能收敛到最优解附近。")
    
    plt.show()

if __name__ == "__main__":
    plot_landscape()