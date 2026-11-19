"""
文件名: chebyshev_empirical_verification.py
功能: 模拟并验证切比雪夫不等式在不同概率分布下的普适性

【这是什么？】
通过蒙特卡洛模拟（大量随机抽样），计算数据落在均值 k 个标准差范围内的实际比例，并与切比雪夫不等式给出的理论下界进行对比验证。

【怎么用？】
直接运行脚本。程序将生成包含几十万个样本的不同形状的分布（如正态分布、均匀分布、极度偏态的指数分布），并在控制台打印出落在 2 倍和 3 倍标准差内的实际数据比例。你将亲眼看到理论下界是如何被严格遵守的。
"""

import numpy as np

# --- 可调整参数配置区 ---
SAMPLE_SIZE = 500000        # 模拟的样本总数（数量越大，结果越逼近真实的概率值）
K_VALUES = [2, 3]           # 需要验证的 k 个标准差距离（如 k=2 对应理论下界 75%）
RANDOM_SEED = 42            # 随机种子，保证每次运行结果一致

def verify_chebyshev(distribution_name, data):
    """
    核心验证逻辑：传入任意一堆数据，强行计算它的期望、标准差，
    并验证距离期望 k 个标准差以内的数据比例。
    """
    print(f"\n[{distribution_name}]")
    
    # 1. 计算期望（均值） mu = E(X)
    # 对应数学原理：寻找这组数据的“重心”
    mu = np.mean(data)
    
    # 2. 计算标准差 sigma = sqrt(Var(X))
    # 对应数学原理：衡量数据围绕重心波动的“典型散布半径”
    # 注意：这里使用的是总体标准差计算方式
    sigma = np.std(data)
    
    print(f"  -> 期望 (mu) = {mu:.4f}, 标准差 (sigma) = {sigma:.4f}")
    
    # 3. 针对不同的 k 值进行验证
    for k in K_VALUES:
        # 切比雪夫不等式的理论下界：P(|X - mu| < k * sigma) >= 1 - 1/k^2
        theoretical_lower_bound = 1 - (1 / (k ** 2))
        
        # 定义搜索边界
        lower_limit = mu - k * sigma
        upper_limit = mu + k * sigma
        
        # 统计实际落在边界内的数据个数
        # 对应数学原理：计算事件 {|X - mu| < k * sigma} 发生的频数
        count_inside = np.sum((data > lower_limit) & (data < upper_limit))
        
        # 计算实际比例
        # 对应数学原理：用频率近似概率 P
        actual_ratio = count_inside / SAMPLE_SIZE
        
        print(f"  -> 距离期望 {k} 个标准差以内:")
        print(f"     理论必须大于等于: {theoretical_lower_bound * 100:>6.2f}%")
        print(f"     实际数据所占比例: {actual_ratio * 100:>6.2f}%  [验证通过！]" 
              if actual_ratio >= theoretical_lower_bound 
              else f"     实际数据所占比例: {actual_ratio * 100:>6.2f}%  [验证失败！]")

if __name__ == "__main__":
    np.random.seed(RANDOM_SEED)
    print("=== 切比雪夫不等式：无视分布形状的绝对法则 ===")
    
    # 实验 1：标准正态分布 (最听话的分布)
    # 绝大部分数据都乖乖集中在中心
    normal_data = np.random.randn(SAMPLE_SIZE)
    verify_chebyshev("1. 完美对称的正态分布", normal_data)
    
    # 实验 2：均匀分布 (完全没有中心的分布)
    # 数据像平板一样均匀铺开，根本没有“向中心聚拢”的趋势
    uniform_data = np.random.uniform(low=-10, high=10, size=SAMPLE_SIZE)
    verify_chebyshev("2. 毫无重点的均匀分布", uniform_data)
    
    # 实验 3：指数分布 (极度偏态、拖着长尾巴的分布)
    # 大量数据挤在左边，但右边有极少数极其庞大的数值（巨大的离散源）
    exponential_data = np.random.exponential(scale=5.0, size=SAMPLE_SIZE)
    verify_chebyshev("3. 严重偏斜的指数分布", exponential_data)

    print("\n结论：无论数据长得多么奇形怪状，实际比例永远严格大于理论下界。")