"""
文件名: coin_toss_sample_space.py
功能: 自动构建离散随机试验的样本空间，并演示事件的筛选与组合爆炸现象。

【这是什么？】
这段代码在计算机里完整重现了“穷举所有可能性”的数学过程。它会帮你自动算出无论抛多少枚硬币时的总基本结果数，还能让你直观看到包含这些结果的“所有可能事件”数量是如何以指数级飙升到天文数字的。

【怎么用？】
你可以修改下方配置区中的“硬币数量”或“关心的正面个数”，直接运行。代码会打印出完整的样本空间，并帮你把满足特定条件的“事件”单独作为子集提取出来。
"""

import itertools
import math

# --- 可调整参数配置区 ---
COIN_COUNT = 3        # 抛掷硬币的数量（初次运行建议保持在 3，之后可以尝试修改为 10 或更高）
TARGET_HEADS = 2      # 设定我们关心的具体事件条件：“至少出现这么多个正面”
# ------------------------

def main():
    print(f"=== 实验开始：抛掷 {COIN_COUNT} 枚硬币 ===")
    
    # 【数学对应：构建样本空间 \Omega】
    # itertools.product 在这里执行的是数学上的“笛卡尔积”。
    # 它相当于让每一枚硬币独立地在“正”和“反”中做选择，
    # 从而穷举出所有物理上可区分的、互斥的有序序列，构建出毫无遗漏的底层地图。
    basic_outcomes = ['正', '反']
    sample_space = list(itertools.product(basic_outcomes, repeat=COIN_COUNT))
    
    # 【数学对应：样本空间的大小 |\Omega|】
    # 独立试验的结果总数遵循乘法原理。每多一枚硬币，总数乘 2。
    omega_size = len(sample_space)
    
    print(f"\n1. 样本空间构建完毕！")
    print(f"总共包含的样本点（基本结果）数量: {omega_size}")
    if omega_size <= 32:
        print(f"样本空间 \u03A9 = {sample_space}")
    else:
        print("（样本点过多，为了保持屏幕整洁已折叠显示）")

    # 【数学对应：所有可能事件的总数 2^|\Omega|】
    # 任何一个事件都是样本空间的一个“子集”。
    # 构建子集时，对于样本空间中的每一个点，都有“包含”或“不包含”两种选择。
    # 这是一个关于子集数量的组合计数问题，结果是 2 的 n 次方。
    try:
        total_events = 2 ** omega_size
        print(f"\n2. 理论事件总数计算：")
        print(f"基于当前样本空间，理论上可以定义出 2^{omega_size} = {total_events} 个不同的事件！")
    except OverflowError:
        print(f"\n2. 理论事件总数计算：")
        print(f"数字太大溢出了！2^{omega_size} 是一个极端的超大数字，足以证明组合爆炸的威力。")

    # 【数学对应：事件的定义与筛选 A \subseteq \Omega】
    # 事件是对样本空间的一种人工聚类。
    # 我们遍历样本空间中的每一个点，并施加判定条件（正面的数量 >= TARGET_HEADS）。
    # 只有满足条件（True）的样本点，才会被收纳进我们定义的事件集合 A 中。
    print(f"\n3. 事件筛选：寻找“至少有 {TARGET_HEADS} 枚正面”的事件 A")
    
    event_A = []
    for outcome in sample_space:
        # outcome 是一个元组，比如 ('正', '反', '正')
        if outcome.count('正') >= TARGET_HEADS:
            event_A.append(outcome)
            
    print(f"事件 A 包含的样本点数量: {len(event_A)}")
    if len(event_A) <= 32:
        print(f"事件 A = {event_A}")
    else:
        print("（符合条件的样本点过多，已折叠显示）")
        
    print("\n=== 实验结束 ===")

if __name__ == "__main__":
    main()