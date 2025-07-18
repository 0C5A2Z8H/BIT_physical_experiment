# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# --- 实验数据 ---
# 电阻 R_m (Ω)
R_ohm = np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 2000, 3000, 4000, 10000])

# 电压 U (V)
U_V = np.array([0.063, 0.854, 1.6, 2.28, 2.85, 3.27, 3.57, 3.81, 3.98, 4.1, 4.2, 4.27, 4.33, 4.37, 4.41, 4.44, 4.55, 4.66, 4.7, 4.78])

# 电流 I (mA)
I_mA = np.array([8, 7.9, 7.7, 7.3, 6.9, 6.4, 5.8, 5.3, 4.9, 4.5, 4, 3.7, 3.5, 3.2, 3.1, 2.9, 2.2, 1.5, 1.2, 0.5])

# --- 数据检查 ---
if not (len(R_ohm) == len(U_V) == len(I_mA)):
    print("错误：输入的电阻、电压、电流数据长度不一致！请检查数据。")
    exit()

# --- 计算功率 P (mW) ---
# P = U * I (电压单位V，电流单位mA，则功率单位mW)
P_mW = U_V * I_mA

# --- 绘制 I-U 曲线 ---
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(U_V, I_mA, 'o-', label='实验数据')
ax1.set_xlabel('电压 U (V)')
ax1.set_ylabel('电流 I (mA)')
ax1.set_title('太阳能电池板负载特性 (I-U曲线)')
ax1.grid(True)
ax1.legend()

# 突出X和Y轴，原点在左下角
ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_color('black')
ax1.spines['left'].set_color('black')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlim(left=0) # 确保X轴从0开始
if len(I_mA) > 0:
    ax1.set_ylim(bottom=0) # 确保Y轴从0开始

plt.savefig('load_I_U_curve.png')
print("I-U 曲线已保存为 load_I_U_curve.png")

# --- 绘制 P-R 依赖关系曲线 ---
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(R_ohm, P_mW, 'o-', label='实验数据')
ax2.set_xlabel('电阻 R (Ω)')
ax2.set_ylabel('功率 P (mW)')
ax2.set_title('太阳能电池板负载特性 (P-R曲线)')
ax2.grid(True)

# 查找并标记最佳匹配电阻 (最大功率点)
if len(P_mW) > 0:
    P_max = np.max(P_mW)
    R_optimal_indices = np.where(P_mW == P_max)[0]
    # 如果有多个点功率相同且最大，取第一个（或平均，这里简单取第一个）
    R_optimal = R_ohm[R_optimal_indices[0]]
    P_max_at_R_optimal = P_mW[R_optimal_indices[0]]

    ax2.plot(R_optimal, P_max_at_R_optimal, 'ro', markersize=10, label=f'最佳匹配点')
    ax2.annotate(f'最佳匹配\n  R = {R_optimal} Ω\n  P = {P_max_at_R_optimal:.3f} mW',
                 xy=(R_optimal, P_max_at_R_optimal),
                 xytext=(R_optimal + 0.05 * np.max(R_ohm), P_max_at_R_optimal - 0.1 * np.max(P_mW) if P_max_at_R_optimal > 0.1 * np.max(P_mW) else P_max_at_R_optimal + 0.05 * np.max(P_mW) ),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=0.72, alpha=0.8))

ax2.legend()

# 突出X和Y轴，原点在左下角
ax2.spines['bottom'].set_linewidth(1.5)
ax2.spines['left'].set_linewidth(1.5)
ax2.spines['bottom'].set_color('black')
ax2.spines['left'].set_color('black')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_xlim(left=0) # 确保X轴从0开始
if len(P_mW) > 0:
    ax2.set_ylim(bottom=0) # 确保Y轴从0开始

plt.savefig('load_P_R_curve.png')
print("P-R 曲线已保存为 load_P_R_curve.png")

print("\n--- 分析完成 ---")
if 'P_max' in locals() and 'R_optimal' in locals(): # 确保P_max和R_optimal已定义
    print(f"已找到最大功率 P_max = {P_max_at_R_optimal:.3f} mW")
    print(f"对应的最佳匹配电阻 R_optimal = {R_optimal} Ω")

    # --- 计算并打印填充因子 (FF) ---
    # 开路电压 Voc: 取最后一个数据点的电压 (假设此时电阻足够大接近开路)
    # 如果有更明确的开路数据点，应使用那个点
    if len(U_V) > 0:
        Voc = U_V[-1] #最后一个电压值
    else:
        Voc = np.nan # 避免数据为空时出错
        print("警告：电压数据为空，无法获取Voc")

    # 短路电流 Isc: 取第一个数据点的电流 (假设此时电阻为0或接近短路)
    # 如果有更明确的短路数据点，应使用那个点
    if len(I_mA) > 0:
        Isc = I_mA[0] # 第一个电流值
    else:
        Isc = np.nan # 避免数据为空时出错
        print("警告：电流数据为空，无法获取Isc")
        
    if not (np.isnan(Voc) or np.isnan(Isc) or Isc == 0 or Voc == 0): # 确保Voc和Isc有效且不为0
        # P_max_at_R_optimal 的单位是 mW
        # Voc 的单位是 V
        # Isc 的单位是 mA
        # Voc * Isc 的单位是 mW，与P_max_at_R_optimal单位一致
        fill_factor = P_max_at_R_optimal / (Voc * Isc)
        print(f"近似开路电压 Voc ≈ {Voc:.3f} V (取自 R={R_ohm[-1]} Ω 数据点)")
        print(f"近似短路电流 Isc ≈ {Isc:.3f} mA (取自 R={R_ohm[0]} Ω 数据点)")
        print(f"计算得到的填充因子 FF ≈ {fill_factor:.4f}")
    else:
        print("警告：无法计算填充因子，Voc或Isc无效或为零。")
        if Voc == 0:
            print("原因：近似开路电压 Voc 为 0。")
        if Isc == 0:
            print("原因：近似短路电流 Isc 为 0。")
else:
    print("警告：未能找到最大功率点，无法计算填充因子。")
