# -*- coding: utf-8 -*-
"""
文件名: random_clustering_demo.py
功能: 模拟随机过程中的“聚类错觉”，可视化连续出现的“长条纹”

【这是什么？】
这段代码模拟了一个绝对公平的硬币连续抛掷的过程。
人类直觉认为“随机”意味着频繁交替（如正反正反），但数学告诉我们，
真正的随机过程中会出现大量的“扎堆”现象（如连续6个正面）。
程序将生成一个随机序列，并自动把那些让你觉得“这肯定有鬼”的连续片段高亮标记出来。

【怎么用？】
直接运行即可。
1. 程序会生成一幅类似“条形码”的图。
2. 蓝色代表正面，灰色代表反面。
3. 红色框会圈出所有长度超过你设定的“敏感阈值”的连续片段。
你可以修改下方的配置参数，看看随机性是如何“捉弄”你的直觉的。
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 可调整参数配置区 ---
TOTAL_TOSSES = 200        # 模拟抛硬币的总次数（建议 100-500）
STREAK_THRESHOLD = 5      # “聚类”阈值：连续出现多少次相同结果，你就会觉得“不随机”？
PROBABILITY = 0.5         # 硬币正面的概率（0.5 代表绝对公平）
SEED = None               # 随机种子（填入数字如 42 可复现相同结果，填 None 则每次随机）

# --- 绘图风格配置 ---
COLOR_HEAD = '#1F77B4'    # 正面颜色 (深蓝)
COLOR_TAIL = '#E0E0E0'    # 反面颜色 (浅灰)
COLOR_ALERT = '#FF4136'   # 聚类高亮框颜色 (红色)

def generate_and_visualize_clustering():
    # 1. 设置随机环境
    # 如果指定了种子，每次运行结果将一致，方便复盘
    if SEED is not None:
        np.random.seed(SEED)
    
    # 2. 生成核心数据
    # 使用伯努利试验模型生成序列 (0代表反面, 1代表正面)
    # 这一步对应数学中的独立同分布 (i.i.d.) 随机变量生成
    tosses = np.random.choice([0, 1], size=TOTAL_TOSSES, p=[1-PROBABILITY, PROBABILITY])
    
    # 3. 准备画布
    # 我们用“条形码”的形式来展示，这样更容易看清序列的纹理
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # 4. 绘制基础序列
    # 遍历每一次抛掷结果，绘制竖线
    for i, result in enumerate(tosses):
        color = COLOR_HEAD if result == 1 else COLOR_TAIL
        # 在图上画一条竖线，代表一次事件
        ax.bar(i, 1, width=1.0, color=color, edgecolor="none", align='edge')

    # 5. 核心算法：寻找并标记“聚类”（Streaks）
    # 这里我们需要找出所有长度 >= STREAK_THRESHOLD 的连续片段
    current_streak_len = 1
    current_val = tosses[0]
    start_index = 0
    
    found_clusters = 0 # 计数器

    # 遍历序列（从第2个元素开始比对前一个）
    for i in range(1, TOTAL_TOSSES):
        if tosses[i] == current_val:
            # 如果和前一个一样，说明聚类在继续
            current_streak_len += 1
        else:
            # 如果不一样，说明上一个聚类结束了，结算一下
            if current_streak_len >= STREAK_THRESHOLD:
                # 对应数学原理：在独立事件中，连续出现 k 次特定结果的概率虽然低，
                # 但在长序列中出现至少一次的概率极高 (大样本下的必然性)
                _highlight_streak(ax, start_index, current_streak_len)
                found_clusters += 1
            
            # 重置计数器，开始统计新的片段
            current_streak_len = 1
            current_val = tosses[i]
            start_index = i
            
    # 别忘了处理收尾（如果最后一段也是长聚类）
    if current_streak_len >= STREAK_THRESHOLD:
        _highlight_streak(ax, start_index, current_streak_len)
        found_clusters += 1

    # 6. 图表修饰
    ax.set_xlim(0, TOTAL_TOSSES)
    ax.set_ylim(0, 1.2) # 留出顶部空间画红框
    ax.set_yticks([])   # 隐藏Y轴刻度
    ax.set_xlabel('抛掷次序 (Time Sequence)', fontsize=12)
    ax.set_title(f'聚类错觉模拟：在 {TOTAL_TOSSES} 次随机实验中，发现了 {found_clusters} 处“疑似人为”的聚类\n(蓝色=正面，灰色=反面，红框=连续{STREAK_THRESHOLD}次以上相同)', fontsize=14)
    
    # 去除多余边框，保持极简
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    print(f"模拟完成。共检测到 {found_clusters} 个长聚类。请查看弹出的图表。")
    plt.tight_layout()
    plt.show()

def _highlight_streak(ax, start, length):
    """
    辅助函数：在图表上画一个红色的矩形框，圈出聚类区域
    """
    # 绘制红框
    rect = plt.Rectangle((start, 0), length, 1, 
                         linewidth=2, edgecolor=COLOR_ALERT, facecolor='none', zorder=10)
    ax.add_patch(rect)
    # 在红框上方标记长度
    ax.text(start + length/2, 1.05, str(length), 
            color=COLOR_ALERT, ha='center', va='bottom', fontsize=10, fontweight='bold')

if __name__ == "__main__":
    generate_and_visualize_clustering()