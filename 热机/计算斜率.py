import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- 1. 输入实验数据 ---
# 注意：请用你自己的实验数据替换以下示例数据
# 高度 h，单位：毫米 (mm)
h_data_mm = np.array([10, 20, 30, 40, 50, 60])
# 对应的周期平方 T^2，单位：毫秒平方 (ms²)
T2_data_ms2 = np.array([334.89, 470.89, 660.49, 745.29, 1024, 1274.49])

# 计算比热容比所需的参数
m = 0.0485  # 振动物体质量 (kg)
A = 0.00082958 # 活塞面积 (m^2)
P = 101300 # 大气压强 (Pa)

# --- 2. 数据处理与绘图 ---
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 线性拟合：h = K * T^2 + b
coefficients = np.polyfit(T2_data_ms2, h_data_mm, 1)
K_mm_ms2 = coefficients[0] # 斜率 K (mm/ms²)
b_mm = coefficients[1] # 截距 b (mm)

# 计算拟合直线上的点用于绘图
T2_fit_ms2 = np.linspace(T2_data_ms2.min(), T2_data_ms2.max(), 100)
h_fit_mm = K_mm_ms2 * T2_fit_ms2 + b_mm

# 生成图例标签
sign = '-' if b_mm < 0 else '+'
if abs(b_mm) < 1e-3:
    legend_label = f'线性拟合: h = {K_mm_ms2:.3f} $T^2$'
else:
    legend_label = f'线性拟合: h = {K_mm_ms2:.3f} $T^2$ {sign} {abs(b_mm):.2f}'

# 绘制图表
plt.figure(figsize=(10, 6))
plt.scatter(T2_data_ms2, h_data_mm, label='实验数据点', color='blue', marker='o')
plt.plot(T2_fit_ms2, h_fit_mm, label=legend_label, color='red', linestyle='--')

plt.title('高度 h vs 周期平方 $T^2$ 关系图', fontsize=16)
plt.xlabel('周期平方 $T^2$ ($ms^2$)', fontsize=12)
plt.ylabel('高度 h (mm)', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# 打印拟合结果
print(f"线性拟合结果:")
print(f"斜率 K = {K_mm_ms2:.4f} mm/ms²")
print(f"截距 b = {b_mm:.4f} mm")

# --- 3. 计算比热容比 gamma --- 
# 单位换算：斜率从 mm/ms² 转换为 m/s²
K_m_s2 = K_mm_ms2 * 1000.0
print(f"\n换算后的斜率 K = {K_m_s2:.4f} m/s²")

if m is not None and A is not None and P is not None:
    gamma = (4 * np.pi**2 * m * K_m_s2) / (A * P)
    print("\n计算比热容比 γ:")
    print(f"使用参数: m = {m} kg, A = {A} m², P = {P} Pa")
    print(f"计算得到的空气比热容比 γ = {gamma:.3f}")
    
    # 与理论值比较
    gamma_theoretical = 1.4
    error_percentage = abs(gamma - gamma_theoretical) / gamma_theoretical * 100
    print(f"空气理论比热容比约为 1.4")
    print(f"相对误差: {error_percentage:.2f}%")
else:
    print("\n无法计算比热容比 γ，缺少质量 m、面积 A 或压强 P 的值。")
    print("请在代码开头提供这些参数。")
