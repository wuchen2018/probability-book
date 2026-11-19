"""
文件名: martingale_ruin_simulator.py
功能: 模拟“倍投策略”（Martingale）在资金有限情况下的必然破产过程

【这是什么？】
这段代码复现了最著名的赌徒陷阱：试图通过“输了就加倍下注”来保证稳赚不赔。
但在数学上，这是一个负期望值的随机游走。你会看到，虽然资金曲线在大部分时间里缓慢上涨（这是幻觉），
但一旦遇到一次大概率会发生的“长连负”，指数级增长的赌注会瞬间击穿任何有限的本金。

【怎么用？】
直接运行即可。代码会生成两张图：
1. 资金变化图：看你的钱是如何一点点增加，然后突然归零的。
2. 赌注金额图：观察为了挽回损失，你需要押上多么惊人的赌注。
你可以尝试在配置区修改 INITIAL_CAPITAL（本金），看看一百万能不能抗住数学规律。
"""

import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 可调整参数配置区 (Playground) ---
INITIAL_CAPITAL = 1000   # 你的初始本金 (元)
BASE_BET = 1             # 第一次下注的金额 (元)
WIN_PROB = 0.5           # 赢的概率 (0.5为公平游戏，0.48为常见的赌场轮盘赌)
MAX_ROUNDS = 1000        # 最多玩多少局 (如果没输光，玩到这里强制停止)
# ------------------------------------

def simulate_martingale():
    # 初始化状态
    current_capital = INITIAL_CAPITAL
    current_bet = BASE_BET
    
    # 记录数据用于画图
    capital_history = [current_capital]
    bet_history = []  # 记录每一局下注了多少
    
    rounds = 0
    
    print(f"--- 模拟开始：本金 {INITIAL_CAPITAL} 元，基础赌注 {BASE_BET} 元 ---")

    while current_capital > 0 and rounds < MAX_ROUNDS:
        rounds += 1
        
        # 检查：如果当前需要下的注超过了剩余本金，这就叫“爆仓”
        # 在真实世界中，你只能梭哈（All-in）剩余的所有钱
        if current_bet > current_capital:
            current_bet = current_capital
        
        bet_history.append(current_bet)
        
        # 模拟抛硬币 (random.random() 生成 0 到 1 之间的随机浮点数)
        # 如果小于 WIN_PROB，判定为赢；否则为输
        if random.random() < WIN_PROB:
            # === 赢了 ===
            current_capital += current_bet
            # 倍投策略的核心逻辑：
            # 赢了之后，立刻收手，把赌注重置回最小单位，落袋为安。
            current_bet = BASE_BET 
            result = "赢"
        else:
            # === 输了 ===
            current_capital -= current_bet
            # 倍投策略的核心逻辑：
            # 输了之后，下一把必须加倍下注。
            # 目的：只要赢一把，不仅能覆盖刚才输的，还能赚回最开始想赚的那1元。
            current_bet = current_bet * 2
            result = "输"
            
        capital_history.append(current_capital)

    # --- 绘图部分 ---
    # 设置字体以支持中文显示 (尝试常见的系统字体)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'SimSun']
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # 图1：资金曲线
    ax1.plot(capital_history, color='#1F77B4', linewidth=1.5)
    ax1.axhline(y=INITIAL_CAPITAL, color='gray', linestyle='--', alpha=0.5, label='初始本金')
    ax1.axhline(y=0, color='red', linewidth=2, label='破产线')
    ax1.set_ylabel('持有资金 (元)')
    ax1.set_title(f'倍投策略资金变化 (本金: {INITIAL_CAPITAL})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 图2：赌注大小
    # 这张图至关重要：它揭示了资金曲线突然“跳水”的真相——指数爆炸的赌注
    ax2.bar(range(1, len(bet_history)+1), bet_history, color='#FF7F0E', alpha=0.7)
    ax2.set_ylabel('单局下注金额 (元)')
    ax2.set_xlabel('局数')
    ax2.set_title('你需要承担的风险 (赌注金额)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

    # 控制台输出最终结果
    if current_capital <= 0:
        print(f"--- 结局：惨败 ---")
        print(f"在第 {rounds} 局，你破产了。")
        print("原因：遇到了连续失败，导致赌注指数级增长，最终超过了你的本金上限。")
    else:
        print(f"--- 结局：幸存 ---")
        print(f"坚持了 {rounds} 局没有破产，当前资金：{current_capital} 元。")
        print("但这不代表策略有效，只是这次运气好，没有遇到足够长的连败。")

if __name__ == "__main__":
    simulate_martingale()