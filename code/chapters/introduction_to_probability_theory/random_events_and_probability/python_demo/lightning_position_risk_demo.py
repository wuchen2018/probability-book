"""
文件名: lightning_position_risk_demo.py
功能: 模拟“无放回抽样”机制下的座次风险衰减现象

【这是什么？】
这是一个蒙特卡洛模拟程序。它通过模拟成千上万次“多人依次从共用牌堆中抽牌”的过程，来验证一个反直觉的概率陷阱：在类似俄罗斯轮盘赌的无放回抽样中，所谓的“公平轮流”其实隐藏着系统性的座次不平等。

【怎么用？】
直接运行脚本。程序会在终端打印出每个座次的实际“中招”次数和频率，并生成一张柱状图。你会直观地看到，风险是如何随着座次靠后而逐级递减的。
"""

import random
import matplotlib.pyplot as plt

# 设置中文字体，兼容多平台显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
TOTAL_CARDS = 160         # 牌堆总数（样本空间总容量）
TARGET_CARDS = 8          # 触发惩罚的“危险牌”数量（有利结果总数）
PLAYERS = 8               # 参与判定的玩家人数
SIMULATION_ROUNDS = 50000 # 蒙特卡洛模拟的总局数
# ------------------------

def run_simulation():
    # 初始化每个座次的中招计数器
    # 对应数学中的频数统计数组
    hit_counts = [0] * PLAYERS
    
    print(f"开始模拟，总局数: {SIMULATION_ROUNDS}...")

    for _ in range(SIMULATION_ROUNDS):
        # 步骤 1：构建本局的牌堆
        # 用 1 表示危险牌，0 表示安全牌
        deck = [1] * TARGET_CARDS + [0] * (TOTAL_CARDS - TARGET_CARDS)
        
        # 步骤 2：洗牌
        # 对应古典概型中的“等可能随机打乱”，确保每张牌在牌堆顶的概率相等
        random.shuffle(deck)
        
        # 步骤 3：依次判定（模拟第一轮）
        # 这里对应的是“无放回抽样（Sampling without replacement）”
        for i in range(PLAYERS):
            # 玩家依次从牌堆顶翻牌
            drawn_card = deck[i]
            
            if drawn_card == 1:
                # 翻到危险牌，当前座次中招
                hit_counts[i] += 1
                # 危险牌被触发，判定流程终止，跳出循环
                break 

    # --- 统计与可视化 ---
    # 计算大数定律下的经验频率，用频率逼近理论概率
    hit_probabilities = [count / SIMULATION_ROUNDS * 100 for count in hit_counts]
    
    print("-" * 30)
    print("各座次第一轮中招的经验概率：")
    for i, prob in enumerate(hit_probabilities):
        print(f"第 {i+1} 顺位: {prob:.2f}%")

    # 绘制直观的对比柱状图
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(1, PLAYERS + 1), hit_probabilities, color='#1F77B4', alpha=0.8, edgecolor='black')
    
    # 绘制一条“直觉公平线”作为参照系（如果完全公平，大家应该平摊风险）
    # 但注意，由于第一轮不一定百分百有人中招，这只是一个直觉参考点
    naive_fair_prob = (TARGET_CARDS / TOTAL_CARDS) * 100
    plt.axhline(y=naive_fair_prob, color='#E64A19', linestyle='--', linewidth=2, label='首位玩家的绝对风险绝对基准线')
    
    plt.title('无放回抽样中的座次风险衰减 (蒙特卡洛模拟验证)', fontsize=14)
    plt.xlabel('玩家判定顺位', fontsize=12)
    plt.ylabel('实际中招概率 (%)', fontsize=12)
    plt.xticks(range(1, PLAYERS + 1))
    
    # 在柱子上标注具体数值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.2f}%', ha='center', va='bottom', fontsize=10)

    plt.legend()
    plt.grid(axis='y', alpha=0.3, linestyle=':')
    plt.show()

if __name__ == "__main__":
    run_simulation()