"""
文件名: monty_hall_simulation.py
功能: 蒙特卡洛模拟三门问题，验证“换门”与“不换门”的真实获胜概率

【这是什么？】
利用大数定律，让计算机替我们玩成千上万次三门问题游戏。通过记录每一次“坚持原选”和“果断换门”的比赛结果，绘制出胜率随实验次数增加的动态收敛过程，用暴力的统计学方法验证贝叶斯条件概率的推导结果。

【怎么用？】
直接运行该脚本。终端会打印出最终的胜率统计，同时会弹出一张折线图。你将会在图表中看到，随着实验局数的增加，两条策略的胜率曲线是如何上下震荡，并最终死死咬合在 1/3 和 2/3 这两条数学红线上的。
"""

import random
import matplotlib.pyplot as plt

# --- 兼容中文显示的系统字体配置 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# --- 可调整参数配置区 ---
TOTAL_GAMES = 10000  # 总模拟局数。你可以尝试把它改成 100，看看小样本下结果有多不可靠；再改成 50000 看看大数定律的威力。
DOORS_COUNT = 3      # 门的数量。经典问题是 3 扇门。你甚至可以改成 100 扇门，直观感受“概率坍缩”的震撼。

def simulate_monty_hall(games, num_doors):
    # 用于记录每次游戏后，两种策略的累计获胜次数
    win_count_if_stay = 0
    win_count_if_switch = 0
    
    # 记录动态胜率，用于画图
    history_stay_win_rate = []
    history_switch_win_rate = []

    for i in range(1, games + 1):
        # 1. 初始化阶段：生成所有门的编号列表 (例如 [0, 1, 2])
        doors = list(range(num_doors))
        
        # 汽车被随机放置在其中一扇门后，这代表了客观存在的先验概率分布
        car_position = random.choice(doors)
        
        # 2. 玩家行动：玩家根据直觉盲猜一扇门
        player_choice = random.choice(doors)
        
        # 3. 主持人行动：条件概率的干预点
        # 主持人不能开玩家选的门，也不能开藏着车的门
        # 这里模拟了信息的“非对称产生机制”：主持人的选择受限于汽车的真实位置
        available_doors_for_host = [d for d in doors if d != player_choice and d != car_position]
        
        # 如果剩下多扇可开的羊门（说明玩家恰好首选命中汽车），主持人随机开一扇
        # 否则（玩家首选羊门），主持人只能被迫打开唯一剩下的羊门
        host_opens = random.choice(available_doors_for_host)
        
        # 4. 结算阶段：如果坚持最初的选择
        if player_choice == car_position:
            win_count_if_stay += 1
            
        # 5. 结算阶段：如果换门
        # 排除掉玩家初始选的门，再排除掉主持人打开的羊门，剩下的门里玩家随便挑一扇
        # 在经典三门问题中，其实这就只剩唯一的一扇门了
        available_doors_for_switch = [d for d in doors if d != player_choice and d != host_opens]
        new_choice = random.choice(available_doors_for_switch)
        
        if new_choice == car_position:
            win_count_if_switch += 1
            
        # 记录当前的动态胜率（累计获胜次数 / 当前已进行的总局数），体现频率向概率收敛的过程
        history_stay_win_rate.append(win_count_if_stay / i)
        history_switch_win_rate.append(win_count_if_switch / i)

    return history_stay_win_rate, history_switch_win_rate

def plot_results(stay_rates, switch_rates, total_games, num_doors):
    # 理论胜率计算
    # 初始选中的概率是 1/N，所以不换门的胜率永远是 1/N
    theoretical_stay_rate = 1 / num_doors
    # 换门的胜率是将剩下的 (N-1)/N 概率，平分给剩余的 (N-2) 扇门
    # 对于经典三门问题，这就是 2/3
    theoretical_switch_rate = (num_doors - 1) / (num_doors * (num_doors - 2))

    plt.figure(figsize=(10, 6))
    
    # 绘制模拟的动态胜率曲线
    plt.plot(stay_rates, label=f'坚持不换 (最终胜率: {stay_rates[-1]:.2%})', color='#ff7f0e', alpha=0.8)
    plt.plot(switch_rates, label=f'果断换门 (最终胜率: {switch_rates[-1]:.2%})', color='#1f77b4', alpha=0.8)
    
    # 绘制数学理论的参考基准线
    plt.axhline(y=theoretical_stay_rate, color='black', linestyle='--', alpha=0.5, label=f'理论不换胜率 ({theoretical_stay_rate:.2%})')
    plt.axhline(y=theoretical_switch_rate, color='red', linestyle='--', alpha=0.5, label=f'理论换门胜率 ({theoretical_switch_rate:.2%})')
    
    plt.title(f'蒙特卡洛模拟：{num_doors}门问题中的胜率收敛过程 (共 {total_games} 局)')
    plt.xlabel('模拟局数')
    plt.ylabel('累计获胜频率 (胜率)')
    plt.ylim(0, 1.05)
    plt.legend(loc='best')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print(f"开始模拟，总局数：{TOTAL_GAMES}，门的总数：{DOORS_COUNT}...")
    stay_history, switch_history = simulate_monty_hall(TOTAL_GAMES, DOORS_COUNT)
    print("模拟完成！正在生成收敛趋势图...")
    plot_results(stay_history, switch_history, TOTAL_GAMES, DOORS_COUNT)