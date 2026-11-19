# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
文件名: covariance_matrix_pca_whitening.py
功能: 演示协方差矩阵的几何意义，以及利用它进行 PCA（旋转）和白化（缩放）的全过程。

【这是什么？】
这段代码带你把数学公式变成“整形手术”。
它首先生成一团“甚至有点畸形”的 correlated 数据（代表现实世界中复杂的变量关系）。
然后，它利用协方差矩阵计算出的“特征向量”和“特征值”，一步步把这团数据“摆正”（去相关）并“捏圆”（白化/归一化）。
这是理解现代数据预处理最直观的实验。

【怎么用？】
直接运行即可。
你会看到三个步骤的对比图，以及控制台输出的协方差矩阵数值变化。
尝试修改配置区的 ANGLE（旋转角度）或 SCALE（拉伸程度），看看算法能不能适应各种奇形怪状的数据。
"""

# --- 可调整参数配置区 ---
# 样本数量：点越多，统计性质越稳定
NUM_SAMPLES = 2000

# 原始数据的“畸形”程度
# 1. 初始拉伸：X轴方向拉伸倍数（方差差异）
STRETCH_X = 3.0
STRETCH_Y = 1.0

# 2. 初始旋转：数据云团的倾斜角度（引入协方差/相关性）
# 尝试修改为 30, 45, -60 等角度
ROTATION_ANGLE_DEG = 45 

# 随机种子：保证每次运行结果一致（想看随机效果可设为 None）
RANDOM_SEED = 42

# -------------------------

def run_experiment():
    if RANDOM_SEED is not None:
        np.random.seed(RANDOM_SEED)

    # ===========================
    # 第一步：制造“脏”数据
    # ===========================
    # 1. 生成标准正态分布 (圆球状，无相关，方差为1)
    data_standard = np.random.randn(NUM_SAMPLES, 2)

    # 2. 拉伸矩阵 (改变方差)
    scale_matrix = np.array([[STRETCH_X, 0], 
                             [0, STRETCH_Y]])
    
    # 3. 旋转矩阵 (引入协方差)
    theta = np.radians(ROTATION_ANGLE_DEG)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta),  np.cos(theta)]])
    
    # 混合变换：先拉伸，再旋转
    transformation = rotation_matrix @ scale_matrix
    data_raw = data_standard @ transformation.T
    
    # 为了严谨，我们强制把数据中心移到原点 (去中心化)
    data_raw = data_raw - np.mean(data_raw, axis=0)

    print(f"【阶段1】原始数据生成完毕")
    print_covariance_matrix("原始数据的协方差矩阵", data_raw)
    print("-" * 30)

    # ===========================
    # 第二步：PCA (主成分分析) —— 负责“摆正”
    # ===========================
    # 1. 计算协方差矩阵
    # rowvar=False 表示每一行是一个样本，每一列是一个特征
    cov_matrix = np.cov(data_raw, rowvar=False)

    # 2. 特征值分解 (Eigen Decomposition)
    # values: 特征值 (代表在主轴方向上的方差大小)
    # vectors: 特征向量 (代表主轴的方向，即旋转矩阵)
    eigen_values, eigen_vectors = np.linalg.eigh(cov_matrix)

    # 对特征值从大到小排序，确保 PC1 是长轴
    sorted_indices = np.argsort(eigen_values)[::-1]
    eigen_values = eigen_values[sorted_indices]
    eigen_vectors = eigen_vectors[:, sorted_indices]

    # 3. 旋转投影
    # 数学含义：将数据投影到特征向量构建的新坐标系中
    # 几何直觉：把倾斜的椭圆“掰正”，使其主轴与坐标轴平行
    data_pca = data_raw @ eigen_vectors

    print(f"【阶段2】PCA旋转完成")
    print(f"   > 提取出的特征值 (方差): {eigen_values}")
    print(f"   > 理论上，此时非对角线元素(协方差)应该接近 0")
    print_covariance_matrix("PCA后的协方差矩阵", data_pca)
    print("-" * 30)

    # ===========================
    # 第三步：白化 (Whitening) —— 负责“捏圆”
    # ===========================
    # 数学含义：每个维度除以该维度的标准差
    # 几何直觉：把长短不一的椭圆轴，缩放到长度一致，变成正圆
    #epsilon = 1e-5 # 防止除以0
    std_devs = np.sqrt(eigen_values)
    data_whitened = data_pca / std_devs

    print(f"【阶段3】白化缩放完成")
    print(f"   > 理论上，此时变成了单位矩阵 (方差=1，协方差=0)")
    print_covariance_matrix("白化后的协方差矩阵", data_whitened)

    # ===========================
    # 可视化展示
    # ===========================
    plot_results(data_raw, data_pca, data_whitened)

def print_covariance_matrix(label, data):
    cov = np.cov(data, rowvar=False)
    print(f"\n--- {label} ---")
    print(f"[[{cov[0,0]:.4f}, {cov[0,1]:.4f}]")
    print(f" [{cov[1,0]:.4f}, {cov[1,1]:.4f}]]")

def plot_results(d1, d2, d3):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 统一绘图范围，方便肉眼对比比例
    limit = max(np.max(np.abs(d1)), 4) 
    
    titles = ["1. Original Raw Data\n(Correlated & Stretched)", 
              "2. After PCA Rotation\n(Uncorrelated but Stretched)", 
              "3. After Whitening\n(Uncorrelated & Unit Variance)"]
    
    colors = ['#FF4C4C', '#1F77B4', '#2CA02C'] # 红，蓝，绿

    dataset_list = [d1, d2, d3]

    for i, ax in enumerate(axes):
        data = dataset_list[i]
        # 绘制散点
        ax.scatter(data[:, 0], data[:, 1], alpha=0.3, s=5, c=colors[i])
        
        # 绘制坐标轴辅助线
        ax.axhline(0, color='black', lw=0.5)
        ax.axvline(0, color='black', lw=0.5)
        
        # 强制坐标轴比例一致，否则看不出“变圆”的效果
        ax.set_aspect('equal')
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_title(titles[i], fontsize=12, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.4)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_experiment()