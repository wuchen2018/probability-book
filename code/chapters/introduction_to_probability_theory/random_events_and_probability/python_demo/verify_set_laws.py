"""
文件名: verify_set_laws.py
功能: 用 Python 集合运算暴力验证德摩根律和分配律

【这是什么？】
数学公式里的交、并、补运算，在编程中完美对应着集合的交集(&)、并集(|)和差集(-)。
这段代码通过在庞大的样本空间中按规则生成海量事件，分别计算等式左边和右边的结果，
用最直白的数据比对，证明那些看似绕口的反直觉运算定律（如“镜子法则”）是绝对成立的。

【怎么用？】
直接运行脚本。程序会在控制台输出各个集合的计算规模，
并最终告诉你：等式两边独立计算出的集合是否 100% 严丝合缝地相等。
你可以尝试在参数区修改样本空间的大小或事件的筛选规则，看看定律会不会被打破。
"""

# --- 可调整参数配置区 ---
OMEGA_SIZE = 100000    # 样本空间的大小（即模拟 10 万个基础样本点）
A_CONDITION = 3        # 事件 A 的规则：样本空间内能被该数整除的元素
B_CONDITION = 5        # 事件 B 的规则：样本空间内能被该数整除的元素
C_CONDITION = 7        # 事件 C 的规则：样本空间内能被该数整除的元素

def main():
    print(f"正在生成包含 {OMEGA_SIZE} 个样本点的全集空间...")
    
    # 构造全集 Omega (样本空间)：包含从 1 到 OMEGA_SIZE 的所有整数
    # 这相当于我们把所有可能发生的基础结果，打包成了一个大集合
    omega = set(range(1, OMEGA_SIZE + 1))
    
    # 定义事件 A、B、C
    # 在数学上，这对应着 A = {ω ∈ Ω | ω 满足特定条件}
    event_a = {x for x in omega if x % A_CONDITION == 0}
    event_b = {x for x in omega if x % B_CONDITION == 0}
    event_c = {x for x in omega if x % C_CONDITION == 0}
    
    print("\n" + "="*40)
    print("【第一部分：验证德摩根律第一句】")
    print("公式：(A ∪ B)的补集 = A的补集 ∩ B的补集")
    print("="*40)
    
    # --- 计算等式左边 ---
    # 步骤 1：先求 A 和 B 的并集 (A ∪ B)，即“满足 A 或满足 B 或两者皆满足”的结果
    a_union_b = event_a | event_b 
    
    # 步骤 2：求并集的补集。在全集 Omega 中剔除掉 (A ∪ B) 发生的情况
    # 这代表“A 和 B 都没有发生”
    left_side_demorgan = omega - a_union_b
    
    # --- 计算等式右边 ---
    # 步骤 1：分别求 A 的补集和 B 的补集
    # 即各自“不发生”的情况
    not_a = omega - event_a
    not_b = omega - event_b
    
    # 步骤 2：求这两个补集的交集 (not_a ∩ not_b)
    # 这代表“不发生 A，同时也不发生 B”
    right_side_demorgan = not_a & not_b
    
    # --- 核对结果 ---
    is_demorgan_true = (left_side_demorgan == right_side_demorgan)
    print(f"左边集合包含元素个数: {len(left_side_demorgan)}")
    print(f"右边集合包含元素个数: {len(right_side_demorgan)}")
    print(f"德摩根律验证结果: {'成立！完全一致' if is_demorgan_true else '失败'}")


    print("\n" + "="*40)
    print("【第二部分：验证交对并的分配律】")
    print("公式：A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)")
    print("="*40)

    # --- 计算等式左边 ---
    # 逻辑：先锁定 (B ∪ C) 发生的范围，然后再看其中哪些也同时满足 A
    b_union_c = event_b | event_c
    left_side_distributive = event_a & b_union_c

    # --- 计算等式右边 ---
    # 逻辑：分别找出“既满足A又满足B”的部分，以及“既满足A又满足C”的部分，然后合并
    a_intersect_b = event_a & event_b
    a_intersect_c = event_a & event_c
    right_side_distributive = a_intersect_b | a_intersect_c

    # --- 核对结果 ---
    is_distributive_true = (left_side_distributive == right_side_distributive)
    print(f"左边集合包含元素个数: {len(left_side_distributive)}")
    print(f"右边集合包含元素个数: {len(right_side_distributive)}")
    print(f"分配律验证结果: {'成立！完全一致' if is_distributive_true else '失败'}")

if __name__ == "__main__":
    main()