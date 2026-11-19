"""
文件名: berkson_paradox_simulation.py
功能: 模拟两个独立随机变量在经过“共同结果”筛选后产生虚假负相关的现象

【这是什么？】
这段代码用蒙特卡洛模拟证实了概率论中的一个反直觉现象：两个本来毫无关系的独立特征，只要我们设定一个“两者加权必须达标”的门槛来筛选数据，在这批被“准入”的数据集中，这两个特征就会神奇地表现出负相关（此消彼长）。这在统计学中被称为“条件依赖”或“对撞机偏差”。

【怎么用？】
直接运行本脚本。程序会在控制台打印出总体数据和筛选后数据的相关系数，并弹出一张直观的散点对比图。你可以尝试修改配置区里的“筛选门槛”，观察截断线是如何一步步把“独立”逼成“负相关”的。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# --- 可调整参数配置区 ---
SAMPLE_SIZE = 10000        # 生成的随机样本总数（总体规模）
MEAN_A = 50                # 特征A的平均值
STD_A = 15                 # 特征A的标准差
MEAN_B = 50                # 特征B的平均值
STD_B = 15                 # 特征B的标准差

# 核心筛选条件：特征A + 特征B 必须大于这个数值才能被记录
SELECTION_THRESHOLD = 120  

# --- 核心模拟逻辑 ---

# 1. 模拟自然界的原始状态：生成绝对独立的两个特征
# 这里使用的是正态分布。因为是用两个独立的随机函数分别生成，
# 在数学上确保了 P(A, B) = P(A) * P(B)，即它们在总体中没有任何因果或相关关系。
np.random.seed(42) # 固定随机种子，保证每次运行结果一致
trait_A = np.random.normal(MEAN_A, STD_A, SAMPLE_SIZE)
trait_B = np.random.normal(MEAN_B, STD_B, SAMPLE_SIZE)

# 2. 计算总体（原始状态）的相关系数
# 理论上这里的相关系数应该极度接近 0
correlation_population = np.corrcoef(trait_A, trait_B)[0, 1]

# 3. 施加筛选条件（引入对撞机偏差）
# 这一步对应了概率论中的“施加条件”。我们建立了一个布尔掩码（Mask），
# 只有满足 trait_A + trait_B > 门槛的样本才会返回 True。
# 这相当于一个共同结果 C 发生了，我们只研究 P(A, B | C发生)。
selected_mask = (trait_A + trait_B) > SELECTION_THRESHOLD

# 提取出被筛选出来的数据子集
selected_A = trait_A[selected_mask]
selected_B = trait_B[selected_mask]

# 4. 计算被筛选后的数据子集的相关系数
# 理论上这里会出现明显的负数，因为门槛效应导致了“特征A不够，特征B来凑”的代偿机制。
correlation_selected = np.corrcoef(selected_A, selected_B)[0, 1]

# --- 终端输出 ---
print("="*40)
print("伯克森悖论模拟结果")
print("="*40)
print(f"总体样本量: {SAMPLE_SIZE} 个")
print(f"筛选前（总体）特征A与B的相关系数: {correlation_population:.4f} (接近0代表独立)")
print("-" * 40)
print(f"设定的筛选门槛: A + B > {SELECTION_THRESHOLD}")
print(f"通过筛选的样本量: {len(selected_A)} 个")
print(f"筛选后（局部）特征A与B的相关系数: {correlation_selected:.4f} (负数代表存在负相关)")
print("="*40)

# --- 可视化 ---
# 设置中文字体（兼容Windows/Mac读者）
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 5))

# 图1：未受干扰的总体数据
plt.subplot(1, 2, 1)
plt.scatter(trait_A, trait_B, alpha=0.1, color='gray', s=10)
plt.title(f"原始总体分布 (相关系数: {correlation_population:.2f})\n呈现无规律的圆状星云")
plt.xlabel("特征 A")
plt.ylabel("特征 B")
# 画出那条致命的筛选门槛线
x_vals = np.array(plt.gca().get_xlim())
y_vals = SELECTION_THRESHOLD - x_vals
plt.plot(x_vals, y_vals, 'k--', label='筛选门槛线')
plt.legend()

# 图2：被筛选后的数据子集
plt.subplot(1, 2, 2)
# 先用极淡的灰色画出被抛弃的数据，作为背景对比
plt.scatter(trait_A[~selected_mask], trait_B[~selected_mask], alpha=0.05, color='gray', s=10)
# 用亮色标出留下来的数据
plt.scatter(selected_A, selected_B, alpha=0.3, color='#1f77b4', s=10)
plt.title(f"筛选后的数据 (相关系数: {correlation_selected:.2f})\n边界截断强制切出了负相关趋势")
plt.xlabel("特征 A")
plt.ylabel("特征 B")
plt.plot(x_vals, y_vals, 'k--')

plt.tight_layout()
plt.show()