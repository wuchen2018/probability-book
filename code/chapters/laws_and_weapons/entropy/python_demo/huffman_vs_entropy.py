# -*- coding: utf-8 -*-
"""
文件名: huffman_vs_entropy.py
功能: 演示“赫夫曼编码”如何逼近“信息熵”定义的理论极限

【这是什么？】
香农告诉我们要想无损压缩数据，平均每个符号所需的比特数（码长）不可能低于“信息熵”。
这段代码会让你输入一段文字，先算出它的理论熵值，然后真正构建一棵赫夫曼树进行编码。
你会亲眼看到：无论怎么优化，实际的平均码长只能无限接近熵，却永远无法打破这个物理铁律。

【怎么用？】
1. 在下方的“参数配置区”修改 demo_text 变量（建议输入长一点的中英文混合文本）。
2. 运行代码。
3. 观察控制台输出的“理论极限（熵）”与“实际表现（赫夫曼）”的对比。
"""

import math
import heapq
from collections import Counter

# ==========================================
# --- 可调整参数配置区 ---
# ==========================================

# 你可以在这里输入任何你想测试的文本：你的名字、一段歌词、或者一句情话
# 文本越长，字符分布越不均匀，效果越明显
demo_text = "Sherlock Holmes took his bottle from the corner of the mantelpiece, and his hypodermic syringe from its neat morocco case."
# demo_text = "大漠孤烟直，长河落日圆。大漠孤烟直，长河落日圆。" # 也可以试试中文

# ==========================================
# --- 核心逻辑区 (无需修改) ---
# ==========================================

class Node:
    """赫夫曼树的节点类"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # 定义比较规则，为了让优先队列（heapq）知道谁大谁小
    def __lt__(self, other):
        return self.freq < other.freq

def calculate_entropy(text):
    """
    计算文本的信息熵
    对应数学公式: H(X) = -∑ p(x) * log2(p(x))
    """
    total_len = len(text)
    counter = Counter(text)
    entropy = 0.0
    
    print(f"\n--- 1. 频率分析 (Top 5) ---")
    for char, count in counter.most_common(5):
        # 计算概率 p(x) = 频数 / 总数
        p = count / total_len
        # 对应信息熵公式中的每一项： -p * log2(p)
        entropy -= p * math.log2(p)
        print(f"字符 '{char}': 出现 {count} 次, 概率 p ≈ {p:.4f}")
        
    return entropy

def build_huffman_tree(text):
    """
    构建赫夫曼树，并生成编码本
    这是实现“最短平均码长”的经典贪心算法
    """
    counter = Counter(text)
    # 将所有字符转化为叶子节点，放入优先队列
    # 堆结构保证我们每次都能以 O(1) 取出频率最小的两个节点
    heap = [Node(char, freq) for char, freq in counter.items()]
    heapq.heapify(heap)

    # 只要堆里还有多于1个节点，就合并
    while len(heap) > 1:
        # 取出频率最小的两个节点（对应直觉：出现少的字符，给它长编码也没关系）
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        # 合并成一个新节点，频率是两者之和
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        # 放回堆中
        heapq.heappush(heap, merged)

    return heap[0] # 返回根节点

def generate_codes(node, prefix="", codebook={}):
    """递归生成01编码"""
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def analyze_huffman_performance(text, codebook):
    """计算实际编码后的平均码长"""
    total_bits = 0
    for char in text:
        # 查表，看每个字符变成了几个 bit
        bits_len = len(codebook[char])
        total_bits += bits_len
    
    avg_bits = total_bits / len(text)
    return avg_bits

# ==========================================
# --- 主程序执行流 ---
# ==========================================
if __name__ == "__main__":
    print(f"正在分析文本: \"{demo_text[:20]}...\" (共 {len(demo_text)} 个字符)")

    # 1. 计算理论上的“信息熵”
    theoretical_entropy = calculate_entropy(demo_text)

    # 2. 运行赫夫曼算法进行实际编码
    root = build_huffman_tree(demo_text)
    huffman_codes = generate_codes(root)
    
    # 3. 计算实际表现
    actual_avg_len = analyze_huffman_performance(demo_text, huffman_codes)

    # 4. 最终对比
    print(f"\n--- 最终对决结果 ---")
    print(f"理论极限 (信息熵)      : {theoretical_entropy:.4f} bits/符号")
    print(f"实际表现 (赫夫曼平均码长): {actual_avg_len:.4f} bits/符号")
    print(f"编码效率 (Entropy/Avg) : {(theoretical_entropy/actual_avg_len)*100:.2f}%")
    
    print("\n" + "="*40)
    if actual_avg_len >= theoretical_entropy:
        print("验证成功！实际码长 >= 理论熵值")
        print("香农的棺材板按住了，物理定律依然有效。")
    else:
        print("警告：发现物理学圣杯？不可能，请检查代码逻辑。")
    print("="*40 + "\n")