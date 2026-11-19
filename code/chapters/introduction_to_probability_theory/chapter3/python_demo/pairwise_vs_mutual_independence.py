"""
文件名: pairwise_vs_mutual_independence.py
功能: 通过大样本蒙特卡洛模拟，直观验证“两两独立”并不等于“相互独立”。

【这是什么？】
数学上证明了三个事件可以满足任意两个都互不干扰（两两独立），但三个凑在一起时却产生了强烈的绑定关系。这段代码抛掷了海量的虚拟硬币，用频率统计来代替复杂的公式推导，向你证明这个反直觉的数学事实：局部无关联，推不出整体无关联。

【怎么用？】
直接运行脚本。控制台会输出各个事件的单独发生频率、两两同时发生的频率，以及三者同时发生的频率。你会亲眼看到理论上的乘法公式在双边关系中完美成立，却在三方聚会时彻底破产。
"""

import numpy as np

# --- 可调整参数配置区 ---
NUM_TRIALS = 1000000  # 抛硬币的总次数（样本量越大，大数定律让频率越接近真实概率）
COIN_HEADS = 1        # 定义正面的数值表示
COIN_TAILS = 0        # 定义反面的数值表示

def main():
    print(f"--- 正在进行 {NUM_TRIALS:,} 次独立重复抛币实验 ---\n")

    # 模拟抛掷两枚公平的硬币
    # 这里生成一个形状为 (NUM_TRIALS, 2) 的矩阵，代表所有实验的两次结果
    tosses = np.random.randint(0, 2, size=(NUM_TRIALS, 2))
    coin1 = tosses[:, 0]
    coin2 = tosses[:, 1]

    # 定义三个观察事件
    # 对应数学定义中的事件 A、B、C
    event_A = (coin1 == COIN_HEADS)
    event_B = (coin2 == COIN_HEADS)
    event_C = (coin1 == coin2)  # 两枚硬币结果相同（同为正或同为反）

    # 计算基础事件的发生频率（对应边缘概率 P(A), P(B), P(C)）
    prob_A = np.mean(event_A)
    prob_B = np.mean(event_B)
    prob_C = np.mean(event_C)

    print("【第一步：基础事件概率】")
    print(f"P(A) 第一枚是正面: {prob_A:.4f}")
    print(f"P(B) 第二枚是正面: {prob_B:.4f}")
    print(f"P(C) 两枚硬币同面: {prob_C:.4f}\n")

    # 计算两两同时发生的频率（对应联合概率 P(AB), P(AC), P(BC)）
    # 在 Python 中，符号 & 代表布尔数组的逐元素逻辑与操作，即求交集
    prob_AB = np.mean(event_A & event_B)
    prob_AC = np.mean(event_A & event_C)
    prob_BC = np.mean(event_B & event_C)

    print("【第二步：验证两两独立】")
    print("规则：如果 P(XY) ≈ P(X) * P(Y)，则 X 与 Y 相互独立。")
    print(f"P(A)*P(B) = {prob_A * prob_B:.4f}  |  P(AB) 实际统计 = {prob_AB:.4f} -> 独立！")
    print(f"P(A)*P(C) = {prob_A * prob_C:.4f}  |  P(AC) 实际统计 = {prob_AC:.4f} -> 独立！")
    print(f"P(B)*P(C) = {prob_B * prob_C:.4f}  |  P(BC) 实际统计 = {prob_BC:.4f} -> 独立！\n")

    # 计算三者同时发生的频率（对应联合概率 P(ABC)）
    prob_ABC = np.mean(event_A & event_B & event_C)
    
    # 理论上的三者相乘
    prob_A_B_C_multiplied = prob_A * prob_B * prob_C

    print("【第三步：验证相互独立（终极考验）】")
    print("规则：如果 P(ABC) ≈ P(A)*P(B)*P(C)，则三者相互独立。")
    print(f"P(A)*P(B)*P(C) 理论期望 = {prob_A_B_C_multiplied:.4f}")
    print(f"P(ABC) 实际统计结果     = {prob_ABC:.4f}")
    
    print("\n【结论】")
    if abs(prob_ABC - prob_A_B_C_multiplied) > 0.05:
        print("发现巨大断层！实际统计的 P(ABC) 根本不等于各自概率的乘积。")
        print("这证明了：两两独立，绝对推不出相互独立！")
    else:
        print("样本量太小，建议调大 NUM_TRIALS 重新运行。")

if __name__ == "__main__":
    main()