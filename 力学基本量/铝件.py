import numpy as np

# --- 用户输入数据 ---
# 请在此处填入您的测量数据和仪器参数

# 1. 各项尺寸的7次测量值 (单位: mm)
outer_diameter_measurements = [25.30,25.30,25.40,25.28,25.30,25.34,25.30] # 示例数据，请替换为您的外径测量值
inner_diameter_measurements = [14.72,14.74,14.74,14.66,14.70,14.70,14.70] # 示例数据，请替换为您的内径测量值
depth_measurements = [22.10,22.16,22.00,21.80,22.10,22.26,22.14]          # 示例数据，请替换为您的凹槽深度测量值
height_measurements = [33.20,33.18,33.20,33.10,33.20,33.12,33.18]         # 示例数据，请替换为您的总高度测量值

# 2. 铝件质量 (单位: g)
mass_measurement = 35.75 # 示例数据，请替换为您的质量测量值

# 3. 仪器误差参数
# 长度测量仪器的仪器误差限 (例如，游标卡尺为0.02mm或0.05mm，千分尺为0.004mm)
# 这个值 'a' 用于计算B类不确定度 u_B = a / sqrt(3)
delta_ins_length = 0.02           # (mm) 示例数据，请根据您的仪器修改
delta_ins_mass = 0.05             # (g) (题目给定)

# 4. 包含因子
k_mass = 1.645                    # (题目给定, 仅用于质量)

# --- 辅助函数：计算单个物理量的统计数据和不确定度 ---\
def calculate_dimension_stats(measurements, delta_ins_dim_val, dimension_name):
    """
    计算给定测量序列的平均值、标准差、A类、B类及合成标准不确定度。
    
    Args:
        measurements (list): 测量数据列表。
        delta_ins_dim_val (float): 该物理量的仪器误差限。
        dimension_name (str): 物理量的名称 (用于打印)。
        
    Returns:
        tuple: mean_val, std_dev, u_A, u_B, u_c 
               (u_c is the combined standard uncertainty)
    """
    if not measurements:
        print(f"警告: {dimension_name} 的测量数据为空!")
        return 0, 0, 0, 0, 0
        
    n = len(measurements)
    mean_val = np.mean(measurements)
    
    if n > 1:
        std_dev = np.std(measurements, ddof=1) # ddof=1 使用贝塞尔校正 (n-1)
        u_A = std_dev / np.sqrt(n)
    else:
        std_dev = 0 # 单次测量，标准差为0
        u_A = 0     # 单次测量，A类不确定度为0
    
    # B类不确定度 (假设为均匀分布)
    u_B = delta_ins_dim_val / np.sqrt(3)
    
    # 合成标准不确定度
    u_c = np.sqrt(u_A**2 + u_B**2)
        
    return mean_val, std_dev, u_A, u_B, u_c

# --- 计算过程 ---

print("--- 物理量测量结果与不确定度分析 ---")

# 1. 外直径 (D)
mean_D, std_D, uA_D, uB_D, uc_D = calculate_dimension_stats(outer_diameter_measurements, delta_ins_length, "外直径")
U_D = uc_D # 扩展不确定度 (k=1)
print(f"外直径 (D):")
print(f"  测量数据: {outer_diameter_measurements} mm")
print(f"  平均值: {mean_D:.3f} mm")
print(f"  标准差 (s_D): {std_D:.3f} mm")
print(f"  A类不确定度 (u_A(D)): {uA_D:.4f} mm")
print(f"  B类不确定度 (u_B(D)) (基于 Δ_ins_L = {delta_ins_length:.3f} mm): {uB_D:.4f} mm")
print(f"  合成标准不确定度 (u_c(D)): {uc_D:.4f} mm")
print(f"  扩展不确定度 (U_D, k=1): {U_D:.3f} mm")
print(f"  测量结果: D = ({mean_D:.3f} ± {U_D:.3f}) mm (k=1)\\n")

# 2. 内直径 (d)
mean_d, std_d, uA_d, uB_d, uc_d = calculate_dimension_stats(inner_diameter_measurements, delta_ins_length, "内直径")
U_d = uc_d # 扩展不确定度 (k=1)
print(f"内直径 (d):")
print(f"  测量数据: {inner_diameter_measurements} mm")
print(f"  平均值: {mean_d:.3f} mm")
print(f"  标准差 (s_d): {std_d:.3f} mm")
print(f"  A类不确定度 (u_A(d)): {uA_d:.4f} mm")
print(f"  B类不确定度 (u_B(d)) (基于 Δ_ins_L = {delta_ins_length:.3f} mm): {uB_d:.4f} mm")
print(f"  合成标准不确定度 (u_c(d)): {uc_d:.4f} mm")
print(f"  扩展不确定度 (U_d, k=1): {U_d:.3f} mm")
print(f"  测量结果: d = ({mean_d:.3f} ± {U_d:.3f}) mm (k=1)\\n")

# 3. 凹槽深度 (h_cavity)
mean_h_cavity, std_h_cavity, uA_h_cavity, uB_h_cavity, uc_h_cavity = calculate_dimension_stats(depth_measurements, delta_ins_length, "凹槽深度")
U_h_cavity = uc_h_cavity # 扩展不确定度 (k=1)
print(f"凹槽深度 (h_cavity):")
print(f"  测量数据: {depth_measurements} mm")
print(f"  平均值: {mean_h_cavity:.3f} mm")
print(f"  标准差 (s_h_cavity): {std_h_cavity:.3f} mm")
print(f"  A类不确定度 (u_A(h_cavity)): {uA_h_cavity:.4f} mm")
print(f"  B类不确定度 (u_B(h_cavity)) (基于 Δ_ins_L = {delta_ins_length:.3f} mm): {uB_h_cavity:.4f} mm")
print(f"  合成标准不确定度 (u_c(h_cavity)): {uc_h_cavity:.4f} mm")
print(f"  扩展不确定度 (U_h_cavity, k=1): {U_h_cavity:.3f} mm")
print(f"  测量结果: h_cavity = ({mean_h_cavity:.3f} ± {U_h_cavity:.3f}) mm (k=1)\\n")

# 4. 总高度 (H)
mean_H, std_H, uA_H, uB_H, uc_H = calculate_dimension_stats(height_measurements, delta_ins_length, "总高度")
U_H = uc_H # 扩展不确定度 (k=1)
print(f"总高度 (H):")
print(f"  测量数据: {height_measurements} mm")
print(f"  平均值: {mean_H:.3f} mm")
print(f"  标准差 (s_H): {std_H:.3f} mm")
print(f"  A类不确定度 (u_A(H)): {uA_H:.4f} mm")
print(f"  B类不确定度 (u_B(H)) (基于 Δ_ins_L = {delta_ins_length:.3f} mm): {uB_H:.4f} mm")
print(f"  合成标准不确定度 (u_c(H)): {uc_H:.4f} mm")
print(f"  扩展不确定度 (U_H, k=1): {U_H:.3f} mm")
print(f"  测量结果: H = ({mean_H:.3f} ± {U_H:.3f}) mm (k=1)\\n")

# 5. 质量 (m)
print(f"使用的质量包含因子 k_mass = {k_mass}\\n")
uB_m = delta_ins_mass / np.sqrt(3)
uA_m = 0.0 
uc_m = np.sqrt(uA_m**2 + uB_m**2)
U_m = k_mass * uc_m # 仅质量使用特定的k值
print(f"质量 (m):")
print(f"  测量值: {mass_measurement:.2f} g")
print(f"  A类不确定度 (u_A(m)): {uA_m:.4f} g (假设为0，除非有重复称量数据)")
print(f"  B类不确定度 (u_B(m)) (基于 Δ_ins_m = {delta_ins_mass:.3f} g): {uB_m:.4f} g")
print(f"  合成标准不确定度 (u_c(m)): {uc_m:.4f} g")
print(f"  扩展不确定度 (U_m, k={k_mass}): {U_m:.3f} g")
print(f"  测量结果: m = ({mass_measurement:.2f} ± {U_m:.3f}) g (k={k_mass})\\n")

# 6. 体积 (V) 和其不确定度
# V = π/4 * (D² * H - d² * h_cavity)
V_calculated = (np.pi / 4) * (mean_D**2 * mean_H - mean_d**2 * mean_h_cavity)

term_D_sq = ((np.pi / 2) * mean_D * mean_H * uc_D)**2
term_H_sq = ((np.pi / 4) * mean_D**2 * uc_H)**2
term_d_sq = ((-np.pi / 2) * mean_d * mean_h_cavity * uc_d)**2
term_h_cavity_sq = ((-np.pi / 4) * mean_d**2 * uc_h_cavity)**2

uc_V_sq = term_D_sq + term_H_sq + term_d_sq + term_h_cavity_sq
uc_V = np.sqrt(uc_V_sq)
U_V = uc_V # 扩展不确定度 (k=1)

print(f"体积 (V):")
if V_calculated > 0:
    print(f"  计算体积: {V_calculated:.2f} mm³")
    print(f"  体积的合成标准不确定度 (u_c(V)): {uc_V:.2f} mm³")
    print(f"  体积的扩展不确定度 (U_V, k=1): {U_V:.2f} mm³")
    num_decimals_V = 2 
    if U_V < 1 : num_decimals_V = 3
    if U_V < 0.1 : num_decimals_V = 4
    print(f"  测量结果: V = ({V_calculated:.{num_decimals_V}f} ± {U_V:.{num_decimals_V}f}) mm³ (k=1)\\n")
else:
    print("  计算体积为零或负，请检查输入数据 (尤其是内径和外径的相对大小以及凹槽深度)。\\n")


# 7. 密度 (ρ) 和其不确定度
# ρ = m / V
if V_calculated > 0:
    rho_calculated_g_mm3 = mass_measurement / V_calculated # 单位: g/mm³
    
    if mass_measurement != 0 :
        # 以下不确定度计算仍然基于 g/mm³ 单位进行，以保持与体积不确定度单位的一致性
        relative_uc_m_sq = (uc_m / mass_measurement)**2 
        relative_uc_V_sq = (uc_V / V_calculated)**2 # uc_V 单位是 mm³, V_calculated 单位是 mm³
        uc_rho_g_mm3 = rho_calculated_g_mm3 * np.sqrt(relative_uc_m_sq + relative_uc_V_sq) # 单位: g/mm³
        U_rho_g_mm3 = uc_rho_g_mm3 # 扩展不确定度 (k=1), 单位: g/mm³
        
        # 转换为 g/cm³ 用于报告
        rho_calculated_g_cm3 = rho_calculated_g_mm3 * 1000
        uc_rho_g_cm3 = uc_rho_g_mm3 * 1000
        U_rho_g_cm3 = U_rho_g_mm3 * 1000
        
        print(f"密度 (ρ):")
        # 计算用于 g/cm³ 报告的小数位数
        num_decimals_gcm3 = 2  # 默认2位小数, e.g., 2.70
        if U_rho_g_cm3 < 0.1:
            num_decimals_gcm3 = 3
        if U_rho_g_cm3 < 0.01:
            num_decimals_gcm3 = 4
        if U_rho_g_cm3 < 0.001:
            num_decimals_gcm3 = 5

        # 标准不确定度通常可以比扩展不确定度多一位有效数字，这里我们让它比最终报告多一位小数
        num_decimals_uc_gcm3 = num_decimals_gcm3 + 1

        print(f"  计算密度: {rho_calculated_g_cm3:.{num_decimals_gcm3}f} g/cm³")
        print(f"  密度的合成标准不确定度 (u_c(ρ)): {uc_rho_g_cm3:.{num_decimals_uc_gcm3}f} g/cm³")
        print(f"  密度的扩展不确定度 (U_ρ, k=1): {U_rho_g_cm3:.{num_decimals_gcm3}f} g/cm³")
        
        print(f"  测量结果: ρ = ({rho_calculated_g_cm3:.{num_decimals_gcm3}f} ± {U_rho_g_cm3:.{num_decimals_gcm3}f}) g/cm³ (k=1)")

    else:
        print("质量为零，无法计算密度。")
else:
    print("体积计算无效，无法计算密度。")

print("\\n--- 计算结束 ---")
