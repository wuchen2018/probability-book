"""
文件名: conditional_prob_simulator.py
功能: 用蒙特卡洛模拟演示“条件”如何改变概率（样本空间坍缩）

【这是什么？】
这段代码通过掷几百万次虚拟骰子，用大数定律的暴力统计方法来验证条件概率。它直观地展示了当我们知道某个前提条件后，原来的“全集”是如何被一刀切掉的，以及目标事件在剩下的“新世界”里所占的比例是如何发生变化的。

【怎么用？】
直接运行脚本。你可以在配置区修改掷骰子的总次数。运行后，控制台会输出无条件概率与三种不同条件下的条件概率统计值，你可以直观感受一下大样本下频率向理论概率收敛的过程。
"""

import numpy as np

# --- 可调整参数配置区 ---
NUM_TRIALS = 1_000_000  # 模拟总次数，即最初的“大世界”样本容量（建议在 1万 到 1000万 之间调整观察收敛情况）
TARGET_RED = 4          # 事件 A（我们关心的猎物）：红骰子掷出的点数
COND_BLUE = 4           # 事件 B（条件 1）：蓝骰子的点数
COND_SUM = 7            # 事件 C（条件 2）：两颗骰子点数之和
# ------------------------

def main():
    print(f"[*] 正在生成 {NUM_TRIALS} 个平行宇宙（抛掷两颗骰子）...\n")
    
    # 1. 构建初始的完整样本空间 Omega
    # 使用 numpy 生成均匀分布的随机整数，对应古典概型中各个基本事件的等可能性
    red_dice = np.random.randint(1, 7, NUM_TRIALS)
    blue_dice = np.random.randint(1, 7, NUM_TRIALS)
    
    # --- 实验 0：无条件概率 P(A) ---
    # 在完整的 Omega 空间中，寻找满足 target_red 的样本数量
    count_A = np.sum(red_dice == TARGET_RED)
    prob_A = count_A / NUM_TRIALS
    print(f"【无条件概率】")
    print(f"P(红骰={TARGET_RED}) 的模拟频率: {prob_A:.4f} (理论值: {1/6:.4f})\n")

    
    # --- 实验 1：条件提供无效信息（独立性体现） ---
    # 步骤一：世界坍缩。筛选出满足条件 B 的样本下标，构建新世界。
    # 这对应数学中的寻找条件事件的子集。
    world_B_mask = (blue_dice == COND_BLUE)
    size_world_B = np.sum(world_B_mask) # 对应公式分母 P(B) 的基数
    
    # 步骤二：在新世界中寻找目标。
    # 取交集 A ∩ B：在满足条件 B 的前提下，红骰子也满足目标的样本数。
    intersection_A_and_B = np.sum((red_dice == TARGET_RED) & world_B_mask)
    
    # 步骤三：计算条件概率 P(A|B)
    prob_A_given_B = intersection_A_and_B / size_world_B
    print(f"【条件概率 - 情报无效】")
    print(f"已知[蓝骰={COND_BLUE}]，新世界样本量缩减至: {size_world_B}")
    print(f"P(红骰={TARGET_RED} | 蓝骰={COND_BLUE}) 模拟频率: {prob_A_given_B:.4f} (理论值: {1/6:.4f})")
    print(f"-> 观察：条件发生改变了总样本量，但猎物的占比丝毫未变。\n")


    # --- 实验 2：条件提供有效信息（概率发生改变） ---
    # 步骤一：根据新条件重新划定边界
    world_even_mask = (red_dice % 2 == 0)
    size_world_even = np.sum(world_even_mask)
    
    # 步骤二：在新世界中寻找交集
    intersection_A_and_even = np.sum((red_dice == TARGET_RED) & world_even_mask)
    
    # 步骤三：重新计算比例
    prob_A_given_even = intersection_A_and_even / size_world_even
    print(f"【条件概率 - 情报有效】")
    print(f"已知[红骰为偶数]，新世界样本量缩减至: {size_world_even}")
    print(f"P(红骰={TARGET_RED} | 红骰为偶数) 模拟频率: {prob_A_given_even:.4f} (理论值: {1/3:.4f})")
    print(f"-> 观察：有效情报一刀砍掉了不可能的选项，极大地提升了目标事件的浓度。")

if __name__ == "__main__":
    main()