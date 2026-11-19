"""
功能: 【实验】验证香农熵是数据压缩的极限

【这是什么？】
我们在书中讲过：信息熵（Entropy）不仅仅是一个抽象的“不确定性”数值，
它还是任何无损编码方案（比如把你的文字变成0和1）的“理论极限”。
也就是说，无论你的压缩算法多牛，平均每个字符所需的比特数，几乎不可能低于这个数据的熵。

这个脚本将带领你：
1. 输入一段任意文本（或者使用默认的样例文本）。
2. 计算这段文本的【理论熵值】。
3. 模拟真实的【赫夫曼编码】（Huffman Coding）过程，给每个字分配01代码。
4. 对比“理论极限”和“实际编码长度”，见证数学的神奇预测能力。

【怎么用？】
直接运行本脚本。控制台会打印出详细的计算过程和对比结果。
你可以尝试修改代码底部的 text 变量，换成你自己的名字、歌词或文章。
"""

import math
import heapq
from collections import Counter

def calculate_entropy(text):
    """
    计算字符串的香农熵 (Shannon Entropy)
    公式: H(X) = - sum(p_i * log2(p_i))
    """
    total_len = len(text)
    if total_len == 0:
        return 0
    
    # 1. 统计每个字符出现的次数
    counts = Counter(text)
    
    entropy = 0
    print(f"\n--- 正在分析字符分布 (总长度: {total_len}) ---")
    print(f"{'字符':<6} {'出现次数':<10} {'概率(p)':<10} {'信息量(-log2(p))':<15}")
    print("-" * 50)
    
    # 2. 遍历计算每一项
    for char, count in counts.items():
        p = count / total_len
        # 单个字符的信息量
        info_content = -math.log2(p)
        # 累加到熵 (期望值)
        entropy += p * info_content
        
        # 打印前5个或特定字符的详细信息，避免刷屏
        if len(counts) < 10 or count > total_len * 0.1: 
             print(f"'{char}'\t {count:<10} {p:.4f}     {info_content:.4f} bits")
            
    return entropy

class Node:
    """赫夫曼树的节点类"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # 定义比较规则，用于优先队列排序
    def __lt__(self, other):
        return self.freq < other.freq

def calculate_huffman_avg_len(text):
    """
    模拟赫夫曼编码，计算平均编码长度
    赫夫曼编码是一种贪心算法，给高频词短码，低频词长码。
    """
    if len(text) == 0: return 0
    counts = Counter(text)
    
    # 1. 创建优先队列（最小堆），包含所有叶子节点
    priority_queue = [Node(char, freq) for char, freq in counts.items()]
    heapq.heapify(priority_queue)
    
    # 2. 构建赫夫曼树
    # 每次取出频率最小的两个节点，合并成一个新节点，放回队列
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(priority_queue, merged)
        
    root = priority_queue[0]
    
    # 3. 递归生成编码表
    codes = {}
    def generate_codes(node, current_code):
        if node is None: return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")
        
    generate_codes(root, "")
    
    # 4. 计算平均码长
    # 平均码长 = sum(概率 * 该字符的编码长度)
    total_len = len(text)
    avg_len = 0
    print("\n--- 赫夫曼编码结果 (部分) ---")
    sample_count = 0
    for char, code in codes.items():
        p = counts[char] / total_len
        avg_len += p * len(code)
        
        if sample_count < 5: # 只打印前几个看看
            print(f"字符: '{char}' -> 编码: {code:<10} (长度: {len(code)})")
            sample_count += 1
            
    return avg_len

# ==========================================
# 主程序入口
# ==========================================
if __name__ == "__main__":
    # 💡 可以在这里修改你要测试的文本
    # 这是一个典型的“不均匀分布”例子：空格和元音很多，z/q很少
    text_input = "this is a simple example to show how entropy works regarding information theory"
    
    print(">>> 实验开始 <<<")
    print(f"分析文本内容: \"{text_input}\"")
    
    # 1. 计算理论极限：熵
    entropy_val = calculate_entropy(text_input)
    
    # 2. 计算实际工程：赫夫曼编码平均长度
    huffman_len = calculate_huffman_avg_len(text_input)
    
    print("\n" + "="*40)
    print(">>> 最终对决结果 <<<")
    print("="*40)
    print(f"1. 数学理论值 (信息熵):    {entropy_val:.4f} bits/字符")
    print(f"   -> 含义：如果要无损传输这段话，每个字【最少】需要这么多比特。")
    print("-" * 40)
    print(f"2. 工程实践值 (赫夫曼编码): {huffman_len:.4f} bits/字符")
    print(f"   -> 含义：使用经典的赫夫曼算法压缩后，每个字实际占用的平均比特。")
    print("-" * 40)
    
    efficiency = entropy_val / huffman_len * 100
    print(f"编码效率 (熵 / 实际长度): {efficiency:.2f}%")
    
    if huffman_len >= entropy_val:
        print("\n✅ 验证成功！实际平均码长 >= 信息熵。")
        print("   (香农就像是一个给宇宙这一行设下路障的交警，你永远超不过他画的线。)")
    else:
        print("\n❌ 发生异常！这在理论上是不可能的，请检查是否有计算错误。")