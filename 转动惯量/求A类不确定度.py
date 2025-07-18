import statistics
import math

# 输入六组角加速度数据，用逗号隔开
# 例如: angular_accelerations = [1.23, 1.25, 1.22, 1.26, 1.24, 1.23]
angular_accelerations = [0.21389,0.21515,0.21743,0.21997,0.21693,0.21849]

# 检查数据输入
if not angular_accelerations:
    print("错误：未输入数据，无法计算。")
elif len(angular_accelerations) < 2:
    print(f"错误：至少需要两组数据才能计算标准差，当前只有 {len(angular_accelerations)} 组。")
else:
    n = len(angular_accelerations)
    print(f"测量次数: {n}")

    # 1. 计算平均值
    mean_aa = statistics.mean(angular_accelerations)
    print(f"平均角加速度 (ᾱ): {mean_aa:.5f}")

    # 2. 计算实验标准差 (样本标准差)
    stdev_aa = statistics.stdev(angular_accelerations)
    print(f"实验标准差 (s(α)): {stdev_aa:.5f}")

    # 3. 计算A类不确定度
    u_A = stdev_aa / math.sqrt(n)
    print(f"角加速度的A类不确定度 (u_A(ᾱ)): {u_A:.5f}")

    print("\n计算完成！")
