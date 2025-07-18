
import numpy as np

# --- 实验数据和参数 ---
rho_water = 0.997795  # g/cm³, 水在22°C的密度
m_a = 10.3            # g, 待测物在空气中的质量
m_asw = 20.6          # g, 物在空气中 + 坠子在水中的系统质量读数
m_osw = 9.15          # g, 物体和坠子都浸入水中的系统质量读数
delta_ins_mass = 0.05 # g, 物理天平的仪器误差限
k_balance = 1.645     # 物理天平测量质量的包含因子
k_density = 1.0       # 最终密度报告使用的包含因子 (按要求，与天平的k无关)

print(f"--- 实验数据 ---")
print(f"水在22°C的密度 (ρ_water): {rho_water} g/cm³")
print(f"待测物在空气中的质量 (m_a): {m_a} g")
print(f"物在空气中 + 坠子在水中的质量 (m_asw): {m_asw} g")
print(f"物体和坠子都浸入水中的质量 (m_osw): {m_osw} g")
print(f"物理天平仪器误差限 (Δ_ins_mass): {delta_ins_mass} g")
print(f"物理天平对应包含因子 (k_balance): {k_balance}")
print(f"最终密度报告使用包含因子 (k_density): {k_density}\n")

# --- 计算过程 ---

# 1. 计算各质量测量的标准不确定度 u_c(m)
u_b_mass = delta_ins_mass / np.sqrt(3)
u_a_mass = 0
uc_m = np.sqrt(u_a_mass**2 + u_b_mass**2)

print(f"--- 中间计算值 ---")
print(f"单个质量测量的标准不确定度 u_c(m): {uc_m:.4f} g")

# 2. 计算物体排开水的质量 (m_dw) 及其不确定度
m_dw = m_asw - m_osw
uc_m_dw_sq = uc_m**2 + uc_m**2
uc_m_dw = np.sqrt(uc_m_dw_sq)

print(f"物体排开水的质量 m_dw: {m_dw:.2f} g")
print(f"m_dw 的标准不确定度 u_c(m_dw): {uc_m_dw:.4f} g")

# 3. 计算物体的体积 (V_obj)
if rho_water == 0:
    print("错误：水的密度为零，无法计算体积。")
    V_obj = 0
    uc_V_obj = 0
else:
    V_obj = m_dw / rho_water
    if m_dw != 0:
        relative_uc_V_obj_sq = (uc_m_dw / m_dw)**2
        uc_V_obj = V_obj * np.sqrt(relative_uc_V_obj_sq)
    else:
        print("错误: m_dw 为零，无法计算体积不确定度")
        uc_V_obj = 0

if V_obj != 0:
    print(f"物体的体积 V_obj: {V_obj:.3f} cm³")
    print(f"V_obj 的标准不确定度 u_c(V_obj): {uc_V_obj:.4f} cm³")
elif rho_water !=0:
    print("m_dw 计算为零或导致体积为零。")
print("") # 添加空行以分隔

# 4. 计算物体的密度 (ρ_obj) 及其不确定度
if V_obj == 0:
    # 错误信息已在计算V_obj时打印
    rho_obj = 0
    uc_rho_obj = 0
    relative_uc_rho_obj = 0
else:
    rho_obj = m_a / V_obj
    if m_a != 0 and m_dw != 0:
        term1_sq_rho = (uc_m / m_a)**2
        term2_sq_rho = (uc_m_dw / m_dw)**2
        relative_uc_rho_obj_sq = term1_sq_rho + term2_sq_rho
        relative_uc_rho_obj = np.sqrt(relative_uc_rho_obj_sq)
        uc_rho_obj = rho_obj * relative_uc_rho_obj
    else:
        print("错误: m_a 或 m_dw 为零导致无法计算密度不确定度 (尽管体积可能已计算)")
        relative_uc_rho_obj = 0
        uc_rho_obj = 0

# 5. 扩展不确定度
U_rho_obj = k_density * uc_rho_obj # 使用k_density (通常为1.0)
relative_U_rho_obj = U_rho_obj / rho_obj if rho_obj !=0 and V_obj !=0 else 0

print(f"--- 最终结果 (使用包含因子 k_density={k_density} 进行最终报告) ---")
if rho_obj != 0 and V_obj !=0:
    print(f"计算得到的物体密度 ρ_obj: {rho_obj:.3f} g/cm³")
    print(f"密度的相对标准不确定度 u_c(ρ_obj)/ρ_obj: {relative_uc_rho_obj:.4f}")
    print(f"密度的绝对标准不确定度 u_c(ρ_obj): {uc_rho_obj:.4f} g/cm³")
    print(f"物体密度最终报告值 ρ_obj = ({rho_obj:.3f} ± {U_rho_obj:.3f}) g/cm³ (k={k_density})")
    print(f"其相对扩展不确定度 U(ρ_obj)/ρ_obj: {relative_U_rho_obj:.3f} (或 {relative_U_rho_obj*100:.1f} %)")
elif V_obj == 0:
    print("由于体积计算错误，无法报告最终密度结果。")
elif m_a == 0 and V_obj !=0:
    print(f"物体质量 m_a 为零，计算密度为0。最终报告值 ρ_obj = ({rho_obj:.3f} ± {U_rho_obj:.3f}) g/cm³ (k={k_density})")
else: 
    print("由于输入数据问题，无法完整计算密度及其不确定度。")

print("\n--- 计算结束 ---")
