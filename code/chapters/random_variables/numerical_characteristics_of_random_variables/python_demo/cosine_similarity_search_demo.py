"""
文件名: cosine_similarity_search_demo.py
功能: 揭秘余弦相似度与相关系数的数学本质，并模拟一个极简的“语义搜索引擎”

【这是什么？】
这段代码首先从底层数学公式出发，一步步拆解并对比了“余弦相似度”与“皮尔逊相关系数”的计算过程，
用代码证明了“相关系数本质上就是中心化后的余弦相似度”。接着，它构建了一个包含三个隐藏维度的极简向量空间，
模拟了现代 AI 搜索引擎是如何通过计算向量夹角，跨越字面精准匹配到用户真实意图的。

【怎么用？】
直接运行脚本。控制台会先输出数学推导结果（均值、模长、内积等），证明两个公式的微妙关系。
然后会打印出模拟搜索引擎的检索排行榜。你可以尝试修改“可调整参数配置区”中的查询向量或文档特征，
看看排行榜会发生怎样奇妙的变化。
"""

import numpy as np

# --- 可调整参数配置区 ---

# [实验一] 用于对比相关系数与余弦相似度的两组观测数据
VECTOR_X = [1.0, 2.0, 3.0]
VECTOR_Y = [2.0, 4.0, 5.0]

# [实验二] 模拟搜索引擎的隐式语义空间 (假设维度1: IT算法, 维度2: 农业自然, 维度3: 商业变现)
# 你可以尝试修改 QUERY_VECTOR，比如改成 [0.1, 0.9, 0.1] (想搜种地教程)，看看推荐结果如何变化
QUERY_VECTOR = [0.9, 0.0, 0.4]

# 候选文档特征库
DOCUMENTS = {
    "文档A (硬核iOS代码教程)": [1.0, 0.0, 0.3],
    "文档B (果园机械化种植)": [0.1, 0.9, 0.2],
    "文档C (AI大模型变现实战)": [0.8, 0.0, 0.9]
}

# ------------------------


def math_lab_cosine_vs_correlation():
    print("=" * 50)
    print("实验一：数学硬核拆解 - 余弦相似度 vs 相关系数")
    print("=" * 50)
    
    x = np.array(VECTOR_X)
    y = np.array(VECTOR_Y)
    
    print(f"原始向量 X: {x}")
    print(f"原始向量 Y: {y}\n")

    # 1. 计算纯粹的余弦相似度 (Cosine Similarity)
    # 数学原理：内积除以两个向量模长的乘积，代表空间中两个绝对方向向量的夹角余弦。
    dot_product = np.dot(x, y)  
    norm_x = np.linalg.norm(x)  # 求向量 x 的模长 (欧几里得空间的绝对长度)
    norm_y = np.linalg.norm(y)  # 求向量 y 的模长
    
    cos_sim = dot_product / (norm_x * norm_y)
    print(f"【余弦相似度】(不改变原点): {cos_sim:.4f}")

    # 2. 计算皮尔逊相关系数 (Pearson Correlation)
    # 数学原理：协方差除以标准差的乘积。
    # 几何意义：先将数据“中心化”（减去均值，平移坐标系原点到数据重心），再求新向量的夹角。
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # 执行中心化操作
    centered_x = x - mean_x
    centered_y = y - mean_y
    
    print(f"\n中心化后的 X: {centered_x}")
    print(f"中心化后的 Y: {centered_y}")
    
    # 对中心化后的新向量，再次计算余弦相似度
    dot_centered = np.dot(centered_x, centered_y)
    norm_centered_x = np.linalg.norm(centered_x)
    norm_centered_y = np.linalg.norm(centered_y)
    
    correlation = dot_centered / (norm_centered_x * norm_centered_y)
    print(f"【相关系数】(中心化后的余弦相似度): {correlation:.4f}")
    
    print("\n结论：当向量未中心化时，两者关注点不同；中心化后，余弦相似度与相关系数在数学上完全等价！\n")


def compute_cosine_similarity(vec1, vec2):
    """一个专门计算余弦相似度的极简函数"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def semantic_search_engine():
    print("=" * 50)
    print("实验二：模拟向量搜索引擎排行榜")
    print("=" * 50)
    
    print(f"用户查询向量 (Query): {QUERY_VECTOR}")
    print("-" * 30)
    
    results = []
    # 遍历文档库，计算查询向量与每个文档向量的“夹角余弦”
    for doc_name, doc_vector in DOCUMENTS.items():
        sim_score = compute_cosine_similarity(QUERY_VECTOR, doc_vector)
        results.append((doc_name, sim_score))
        print(f"正在匹配 [{doc_name}] ... 相似度得分: {sim_score:.4f}")
    
    # 根据余弦相似度得分进行降序排列 (越接近1，说明空间夹角越小，意图越匹配)
    results.sort(key=lambda item: item[1], reverse=True)
    
    print("-" * 30)
    print("🏆 搜索引擎最终推荐排行榜：")
    for rank, (doc_name, score) in enumerate(results, 1):
        print(f"Top {rank}: {doc_name} (匹配度: {score:.1%})")


if __name__ == "__main__":
    math_lab_cosine_vs_correlation()
    semantic_search_engine()