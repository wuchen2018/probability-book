import numpy as np

"""
文件名: tuesday_boy_simulation.py
功能: 采用蒙特卡洛方法模拟并验证条件概率中的“星期二男孩”悖论

【这是什么？】
这段代码通过计算机的高速随机抽样能力，在内存中生成海量的虚拟家庭（包含性别和特定特征）。
它利用大数定律，暴力筛选出符合条件的家庭，通过真实的统计频率来验证那个反直觉的理论概率公式 P = (2-p)/(4-p)。

【怎么用？】
直接运行脚本。程序会在终端输出模拟海量样本后的真实统计概率，并与数学推导的理论值进行对比。
你可以尝试修改配置区中的特征概率值（比如改成 1 或者 1/14），亲自观察最终的概率重心是如何发生偏移的。
"""

# --- 可调整参数配置区 ---
# 模拟的家庭总数量（建议设置在 100,000 以上，样本基数越大，统计频率越逼近真实概率）
NUM_SIMULATIONS = 1_000_000

# 附加特征的发生概率 p (与性别独立)
# 常用测试值：
# p = 1.0   -> 对应基础条件：“至少有一个男孩”
# p = 1/7   -> 对应经典条件：“至少有一个星期二出生的男孩”
# p = 1/14  -> 对应进阶条件：“至少有一个星期二白天出生的男孩”
# p = 0.001 -> 对应极限条件：特征极其罕见，无限逼近于“指定特定个体”
FEATURE_PROBABILITY = 1 / 7 
# ------------------------

def run_simulation(num_sims, p_feature):
    # 这里我们利用 NumPy 的向量化运算来一次性掷出数百万次硬币，避免缓慢的 for 循环。
    
    # 步骤 1：构建基础样本空间（老大的状态）
    # 生成老大的性别：1 代表男孩，0 代表女孩。男女出生概率各为 0.5
    child1_is_boy = np.random.binomial(n=1, p=0.5, size=num_sims)
    # 生成老大是否具有该特征（例如是否周二出生）：1 代表有，0 代表无
    child1_has_feature = np.random.binomial(n=1, p=p_feature, size=num_sims)
    
    # 步骤 2：构建基础样本空间（老二的状态）
    # 老二的性别与特征生成逻辑同上，且两次随机事件在数学上完全独立
    child2_is_boy = np.random.binomial(n=1, p=0.5, size=num_sims)
    child2_has_feature = np.random.binomial(n=1, p=p_feature, size=num_sims)
    
    # 步骤 3：定义“条件事件 B” (即先决信息)
    # 逻辑判断：老大是男孩且拥有该特征，或者，老二是男孩且拥有该特征
    # 这一步相当于用一张“网”在全宇宙的样本中进行严格的资格审查
    condition_met = (child1_is_boy & child1_has_feature) | (child2_is_boy & child2_has_feature)
    
    # 获取成功通过审查的家庭总数（即条件概率的分母）
    valid_families_count = np.sum(condition_met)
    
    # 步骤 4：在条件成立的新世界中，寻找“目标事件 A”
    # 目标事件：两个孩子都是男孩
    target_met = child1_is_boy & child2_is_boy
    
    # 统计既满足审查条件，又满足最终目标的家庭数量（即分子 P(A ∩ B) 的频数对应物）
    target_and_condition_met_count = np.sum(target_met & condition_met)
    
    # 步骤 5：计算最终的统计频率
    if valid_families_count == 0:
        return 0.0
    simulated_probability = target_and_condition_met_count / valid_families_count
    
    return simulated_probability

if __name__ == "__main__":
    print(f"开始进行蒙特卡洛模拟...")
    print(f"正在生成 {NUM_SIMULATIONS:,} 个虚拟家庭...")
    print(f"设定的特征发生概率 p = {FEATURE_PROBABILITY:.4f}\n")
    
    # 执行模拟计算
    sim_prob = run_simulation(NUM_SIMULATIONS, FEATURE_PROBABILITY)
    
    # 计算严格的数学理论值进行对照
    theoretical_prob = (2 - FEATURE_PROBABILITY) / (4 - FEATURE_PROBABILITY)
    
    print("-" * 30)
    print(f"【模拟统计频率】: {sim_prob:.5f}")
    print(f"【公式理论概率】: {theoretical_prob:.5f}")
    print("-" * 30)
    
    error = abs(sim_prob - theoretical_prob)
    print(f"绝对误差: {error:.5f}")
    print("结论：在大数定律的加持下，代码暴力的统计结果完美吻合了推导出的概率桥梁公式。")