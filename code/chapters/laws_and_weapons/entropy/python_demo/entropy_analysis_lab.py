"""
文件名: entropy_analysis_lab.py
功能: 输入任意联合概率矩阵，自动计算联合熵、条件熵与互信息，并验证链式法则。

【这是什么？】
这段代码是信息论公式的“计算器”。你只需要提供一个联合概率表（就像文中那个“技能vs成果”的表格），
它就会帮你算出所有的核心指标：H(X), H(Y), H(X,Y), H(X|Y), I(X;Y)。
它能帮你直观地理解：为什么互信息代表了两个变量“共享”的那部分不确定性。

【怎么用？】
1. 在“参数配置区”修改 joint_prob_matrix 变量（可以填入任何你想要的概率分布）。
2. 运行脚本。
3. 观察控制台输出的各项熵值，以及验证等式是否成立。
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 可调整参数配置区 ---
# 这里输入两个变量 X 和 Y 的联合概率分布矩阵 P(X, Y)
# 行代表 X 的取值，列代表 Y 的取值
# 默认值使用文中“非独立例子”的数据：
#        Y=0   Y=1
# X=0   0.4   0.1
# X=1   0.2   0.3
joint_prob_matrix = np.array([
    [0.4, 0.1],  # X=0 这一行
    [0.2, 0.3]   # X=1 这一行
])

# --------------------------

def calculate_entropy_metrics(p_xy):
    """
    核心计算逻辑：从联合分布推导所有熵
    """
    # 0. 预处理：归一化（防止用户输入的概率之和不为1）
    if not np.isclose(p_xy.sum(), 1.0):
        print(f"⚠️ 警告：输入的概率之和为 {p_xy.sum()}，正在自动归一化...")
        p_xy = p_xy / p_xy.sum()

    # 1. 计算边缘概率 (Marginal Probabilities)
    # P(X) 是把矩阵每一行加起来（消除 Y 的影响）
    p_x = np.sum(p_xy, axis=1)
    # P(Y) 是把矩阵每一列加起来（消除 X 的影响）
    p_y = np.sum(p_xy, axis=0)

    # 2. 定义基础熵函数 H(P) = -Σ p * log2(p)
    # 使用 np.nansum 和 np.log2，自动处理 0 * log(0) = 0 的情况（避免报错）
    def get_entropy(probs):
        # 过滤掉为0的概率，防止 log(0) 报错
        valid_probs = probs[probs > 0]
        return -np.sum(valid_probs * np.log2(valid_probs))

    # 3. 计算各个熵
    # H(X): X 自身的“神秘感”
    h_x = get_entropy(p_x)
    
    # H(Y): Y 自身的“神秘感”
    h_y = get_entropy(p_y)
    
    # H(X,Y): 联合熵（整体的不确定性）
    # 直接对整个矩阵所有元素求熵
    h_xy = get_entropy(p_xy.flatten())

    # 4. 计算条件熵 H(X|Y) 和 H(Y|X)
    # 利用链式法则公式推导：H(X,Y) = H(Y) + H(X|Y)  =>  H(X|Y) = H(X,Y) - H(Y)
    # 这是数学上最简便的算发，避免了繁琐的加权平均计算，结果是一样的
    h_x_given_y = h_xy - h_y
    h_y_given_x = h_xy - h_x

    # 5. 计算互信息 I(X;Y)
    # 定义：I(X;Y) = H(X) - H(X|Y)
    # 意义：X 原本的不确定性，减去 知道 Y 后剩下的不确定性，就是 Y 提供的“干货”
    mutual_info = h_x - h_x_given_y

    return {
        "P(X)": p_x,
        "P(Y)": p_y,
        "H(X)": h_x,
        "H(Y)": h_y,
        "H(X,Y)": h_xy,
        "H(X|Y)": h_x_given_y,
        "H(Y|X)": h_y_given_x,
        "I(X;Y)": mutual_info
    }

def visualize_results(matrix, metrics):
    """
    可视化：打印结果并画出概率热力图
    """
    print(f"\n{'='*10} 分析报告 {'='*10}")
    print(f"1. 边缘概率:")
    print(f"   P(X) = {metrics['P(X)']}")
    print(f"   P(Y) = {metrics['P(Y)']}")
    
    print(f"\n2. 基础熵 (比特):")
    print(f"   H(X)   = {metrics['H(X)']:.5f} (X 的不确定性)")
    print(f"   H(Y)   = {metrics['H(Y)']:.5f} (Y 的不确定性)")
    print(f"   H(X,Y) = {metrics['H(X,Y)']:.5f} (整体不确定性)")
    
    print(f"\n3. 条件熵 (比特):")
    print(f"   H(X|Y) = {metrics['H(X|Y)']:.5f} (知道 Y 后，X 剩下的不确定性)")
    # 验证信息不增原理
    if metrics['H(X|Y)'] <= metrics['H(X)']:
        print(f"   ✅ 验证：H(X|Y) <= H(X) 成立 (信息不增)")
    else:
        print(f"   ❌ 错误：违反信息不增原理！")

    print(f"\n4. 互信息 (比特):")
    print(f"   I(X;Y) = {metrics['I(X;Y)']:.5f} (X 和 Y 共享的信息量)")
    # 验证独立性
    if metrics['I(X;Y)'] < 1e-10:
        print("   -> 结论：X 和 Y 看起来是【独立】的")
    else:
        print("   -> 结论：X 和 Y 是【相关】的")

    # 绘图
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt='.2f', cmap='Blues', 
                cbar_kws={'label': 'Probability P(x,y)'})
    plt.title(f'Joint Distribution\nMutual Information = {metrics["I(X;Y)"]:.4f} bits')
    plt.xlabel('Y (Variable)')
    plt.ylabel('X (Variable)')
    plt.show()

if __name__ == "__main__":
    results = calculate_entropy_metrics(joint_prob_matrix)
    visualize_results(joint_prob_matrix, results)