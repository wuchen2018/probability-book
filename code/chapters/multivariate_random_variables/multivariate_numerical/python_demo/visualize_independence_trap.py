"""
文件名: visualize_independence_trap.py
功能: 通过蒙特卡洛模拟，直观对比“矩形定义域”与“三角形定义域”对独立性的影响

【这是什么？】
这段代码模拟了成千上万个随机数据点 (X, Y)。
我们通过对比两种形状（正方形 vs 三角形）来验证一个核心数学事实：
只有当 X 和 Y 的活动范围互不干涉（矩形）且密度可分离时，它们才独立。
一旦形状变成三角形，X 的取值就会“锁死” Y 的范围，独立性瞬间瓦解。

【怎么用？】
1. 直接运行脚本。
2. 观察控制台输出的“概率乘积检验”：看看 P(AB) 是否等于 P(A)P(B)。
3. 观察弹出的散点图：直观感受数据点的分布形状。
4. 尝试修改下方的 SHAPE_TYPE 参数，体验不同定义域的效果。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
# 模拟的数据点数量（建议 10000 以上，点越多，概率计算越准）
N_SAMPLES = 20000

# 选择定义域形状：
# 'square'   = 单位正方形 [0,1]x[0,1] (独立)
# 'triangle' = 三角形区域 0 < x < y < 1 (不独立)
SHAPE_TYPE = 'triangle' 

# 验证独立性的阈值设置（用于定义事件 A 和 B）
# 事件 A: X < x_threshold
# 事件 B: Y > y_threshold
X_THRESHOLD = 0.5
Y_THRESHOLD = 0.5

# --------------------------

def run_simulation():
    print(f"--- 正在启动模拟: 形状 = {SHAPE_TYPE} ---")
    
    # 1. 生成原始随机数 (假设 X, Y 都在 0-1 之间均匀分布)
    # 这一步对应于在一个大的矩形画布上随机撒点
    x_raw = np.random.rand(N_SAMPLES)
    y_raw = np.random.rand(N_SAMPLES)
    
    x_final, y_final = [], []

    # 2. 根据形状筛选数据点（这是核心步骤）
    if SHAPE_TYPE == 'square':
        # 矩形区域：X 和 Y 没有任何相互约束
        # 对应数学定义：f(x,y) = 1 (在正方形内)
        x_final, y_final = x_raw, y_raw
        print(">> 定义域为正方形：X 和 Y 互不限制。")
        
    elif SHAPE_TYPE == 'triangle':
        # 三角形区域：强行要求 x < y
        # 对应数学定义：定义域 D = {(x,y) | 0 < x < y < 1}
        # 这种筛选就是一种“依赖注入”：Y 的取值被迫要比 X 大
        mask = x_raw < y_raw
        x_final = x_raw[mask]
        y_final = y_raw[mask]
        print(f">> 定义域为三角形 (0 < x < y < 1)：筛选后剩余 {len(x_final)} 个点。")
    
    else:
        print("未知的形状类型，请检查配置。")
        return

    # 3. 数学检验：P(AB) = P(A)P(B) ?
    # 定义事件 A: X < 0.5
    event_A = x_final < X_THRESHOLD
    # 定义事件 B: Y > 0.5
    event_B = y_final > Y_THRESHOLD
    # 定义联合事件 AB: A 和 B 同时发生
    event_AB = event_A & event_B
    
    # 计算频率（根据大数定律，频率 -> 概率）
    p_A = np.mean(event_A)
    p_B = np.mean(event_B)
    p_AB = np.mean(event_AB)
    p_product = p_A * p_B
    
    # 计算皮尔逊相关系数 (Correlation Coefficient)
    # 独立变量的相关系数应接近 0
    correlation = np.corrcoef(x_final, y_final)[0, 1]

    # 4. 输出统计结果
    print("\n--- 数学检验报告 ---")
    print(f"事件 A (X < {X_THRESHOLD}) 的概率 P(A): {p_A:.4f}")
    print(f"事件 B (Y > {Y_THRESHOLD}) 的概率 P(B): {p_B:.4f}")
    print(f"理论上的 P(A) * P(B):        {p_product:.4f}")
    print(f"实际观测的联合概率 P(AB):    {p_AB:.4f}")
    print(f"差异 (Diff):                 {abs(p_AB - p_product):.4f}")
    print(f"相关系数 (Correlation):      {correlation:.4f}")
    
    if abs(p_AB - p_product) < 0.01:
        print("\n>> 结论：P(AB) ≈ P(A)P(B)，数据支持【独立性】假设。")
    else:
        print("\n>> 结论：P(AB) ≠ P(A)P(B)，【独立性破裂】！")

    # 5. 可视化绘图
    plt.figure(figsize=(8, 8))
    
    # 绘制所有散点
    plt.scatter(x_final, y_final, alpha=0.1, s=2, color='blue', label='Samples')
    
    # 画出事件分割线
    plt.axvline(X_THRESHOLD, color='red', linestyle='--', label=f'X={X_THRESHOLD}')
    plt.axhline(Y_THRESHOLD, color='green', linestyle='--', label=f'Y={Y_THRESHOLD}')
    
    # 标注四个区域的意义
    plt.title(f"Geometry of {SHAPE_TYPE.capitalize()} Domain\nCorrelation: {correlation:.4f}")
    plt.xlabel("Random Variable X")
    plt.ylabel("Random Variable Y")
    plt.legend(loc='upper left')
    plt.axis('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    
    plt.show()

if __name__ == "__main__":
    run_simulation()