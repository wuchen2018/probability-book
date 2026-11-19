"""
文件名: bayes_belief_update_sim.py
功能: 模拟贝叶斯推理中“信念动态更新”的全过程（从先验到后验，再到新先验）。

【这是什么？】
这段代码演示了贝叶斯公式最迷人的特性：它不是一个静态的计算器，而是一个“学习机器”。
它展示了当我们连续获取新证据（例如：产品是否合格）时，
我们对某个假设（例如：机器是正常的）的信心是如何起起伏伏的。
你会直观地看到：建立高置信度需要漫长的积累，但一次“意外”就可能让信心崩塌。

【怎么用？】
1. 在下方的“可调整参数配置区”修改 EVIDENCE_SEQUENCE（观测序列）。
2. 运行脚本。
3. 观察生成的折线图，看你的“信念”是如何随着每一步证据而变化的。
"""

import matplotlib.pyplot as plt
import numpy as np

# --- 必不可少的配置：让图表支持中文显示，防止出现方框乱码 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 保证坐标轴的负号正常显示

# --- 可调整参数配置区 ---

# 场景假设：我们要判断一台机器是否“正常”。

# 1. 初始信念 (Prior)
# 在还没看任何产品之前，你觉得这台机器正常的概率是多少？
INITIAL_BELIEF = 0.98 

# 2. 似然度 (Likelihoods) - 核心假设
# 如果机器是【正常】的，它生产出【合格品】的概率
P_PASS_GIVEN_NORMAL = 0.99
# 如果机器是【故障】的，它依然能碰巧生产出【合格品】的概率
P_PASS_GIVEN_BROKEN = 0.95

# 3. 观测证据序列 (Evidence)
# 1 代表“合格品”，0 代表“次品”
# 建议尝试：
# 情况A (稳步上升)：[1, 1, 1, 1, 1]
# 情况B (信任崩塌)：[1, 1, 1, 1, 1, 0]
# 情况C (艰难重建)：[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
EVIDENCE_SEQUENCE = [1, 1, 1, 0, 1, 1, 1] 

# --- 以下是核心逻辑区（无需修改，但建议阅读注释） ---

def bayesian_update(current_belief, evidence, p_pass_norm, p_pass_brk):
    """
    执行一次贝叶斯更新。
    
    参数:
    current_belief: 当前认为机器正常的概率 P(正常)
    evidence:       新证据 (1=合格, 0=次品)
    
    返回:
    new_belief:     更新后的概率 P(正常 | 新证据)
    """
    
    # 步骤 1: 确定似然度 P(证据 | 假设)
    # 我们要问：在这个假设下，出现当前证据的可能性有多大？
    if evidence == 1:
        likelihood_normal = p_pass_norm       # 正常机器产出合格品的概率
        likelihood_broken = p_pass_brk        # 故障机器产出合格品的概率
    else:
        likelihood_normal = 1 - p_pass_norm   # 正常机器产出次品的概率 (极小)
        likelihood_broken = 1 - p_pass_brk    # 故障机器产出次品的概率
        
    # 步骤 2: 计算分子 (先验概率 × 似然度)
    # 这是贝叶斯公式的分子部分
    numerator = current_belief * likelihood_normal
    
    # 步骤 3: 计算分母 (全概率 / 标准化常数)
    # 全概率公式：不管机器好坏，产生这个证据的总概率是多少？
    # P(证据) = P(正常)P(证据|正常) + P(故障)P(证据|故障)
    denominator = (current_belief * likelihood_normal) + \
                  ((1 - current_belief) * likelihood_broken)
    
    # 步骤 4: 计算后验概率
    new_belief = numerator / denominator
    
    return new_belief

# --- 主程序 ---

def main():
    # 用于记录每一步的信念值，以便画图
    history = [INITIAL_BELIEF]
    current_p = INITIAL_BELIEF
    
    print(f"--- 贝叶斯信念动态更新模拟开始 ---")
    print(f"初始信念: {current_p:.4%}")
    
    # 循环处理每一个新证据
    for i, evidence in enumerate(EVIDENCE_SEQUENCE):
        # 核心：将上一步的后验概率，作为这一步的先验概率！
        # 这就是“贝叶斯迭代”的精髓。
        new_p = bayesian_update(current_p, evidence, 
                                P_PASS_GIVEN_NORMAL, P_PASS_GIVEN_BROKEN)
        
        history.append(new_p)
        
        # 打印过程
        result_str = "合格品" if evidence == 1 else ">>> 次品 <<<"
        print(f"第 {i+1} 步观测: {result_str} | 信念更新: {current_p:.4%} -> {new_p:.4%}")
        
        # 更新当前信念，为下一轮循环做准备
        current_p = new_p

    # --- 绘图部分 ---
    
    plt.figure(figsize=(10, 6))
    
    # 绘制信念变化曲线
    steps = range(len(history))
    plt.plot(steps, history, marker='o', linewidth=2, color='#1F77B4', label='机器正常的概率')
    
    # 添加辅助线和标注
    plt.axhline(y=INITIAL_BELIEF, color='gray', linestyle='--', alpha=0.5, label='初始信念')
    plt.ylim(0, 1.05)
    plt.xlabel('观测步数（个）')
    plt.ylabel('信念度（概率值）')
    plt.title('贝叶斯信念动态演变全过程')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 在图上标注出“次品”出现的位置，因为这是信念崩塌的转折点
    for i, evidence in enumerate(EVIDENCE_SEQUENCE):
        if evidence == 0:
            # 在对应的时间点画一个红色的警示箭头
            plt.annotate('出现次品！', xy=(i+1, history[i+1]), xytext=(i+1, history[i+1]-0.1),
                         arrowprops=dict(facecolor='red', shrink=0.05),
                         ha='center', color='red', fontweight='bold')

    print("\n模拟结束。请查看弹出的折线图，直观感受信任的崩塌与重建。")
    plt.show()

if __name__ == "__main__":
    main()