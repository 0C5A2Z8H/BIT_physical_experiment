import math

# --- 用户输入区 ---
# 请将你的实验数据填入下面的列表中
# 每组数据格式为: (X1_left, X1_prime_right, X11_left, X11_prime_right) 单位: mm
# X1_left: 第1暗环左侧读数
# X1_prime_right: 第1暗环右侧读数
# X11_left: 第11暗环左侧读数
# X11_prime_right: 第11暗环右侧读数
#
# 示例数据 (共5组):
user_data_groups = [
    # (X1, X1', X11, X11') in mm
    (19.672, 21.961, 18.038, 23.551), # 示例：D1 = |4.45-2.35|=2.1, D11 = |7.60-1.50|=6.1
    (19.688, 21.975, 18.040, 23.500), # 示例：D1 = |4.42-2.30|=2.12, D11 = |7.55-1.48|=6.07
    (19.712, 21.978, 18.052, 23.568), # 示例：D1 = |4.50-2.40|=2.1, D11 = |7.65-1.52|=6.13
    (19.712, 21.962, 18.038, 23.510), # 示例：D1 = |4.43-2.33|=2.1, D11 = |7.58-1.49|=6.09
    (19.722, 22.012, 18.061, 23.588)  # 示例：D1 = |4.47-2.37|=2.1, D11 = |7.62-1.51|=6.11
]
# --- 常量定义 ---
lambda_nm = 589.3  # 钠黄光平均波长 (nm)
lambda_mm = lambda_nm * 1e-6  # 波长转换为 mm
delta_ins_mm = 0.005  # 仪器允许误差极限 (mm)
m_ring = 11  # 第 m 个暗环 (远环)
n_ring = 1   # 第 n 个暗环 (近环)

# --- 辅助计算函数 ---
def calculate_mean(values):
    """计算平均值"""
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_std_dev(values, mean_val):
    """计算样本标准差"""
    n = len(values)
    if n < 2: # 样本数小于2，标准差无意义或为0
        return 0.0
    return math.sqrt(sum([(x - mean_val)**2 for x in values]) / (n - 1))

def calculate_type_A_uncertainty(std_dev, num_measurements):
    """计算A类不确定度 (平均值的标准误差)"""
    if num_measurements == 0:
        return float('inf') # 避免除以零
    if num_measurements == 1 and std_dev == 0.0: # 单次测量A类不确定度通常不这样算或为0
        return 0.0
    return std_dev / math.sqrt(num_measurements) if num_measurements > 0 else float('inf')

def calculate_type_B_uncertainty_for_Dk_from_instrument(delta_ins):
    """
    计算单个直径 Dk = |Xk_R - Xk_L| 由于仪器误差极限引起的B类不确定度.
    u(X) = delta_ins / sqrt(3) (矩形分布)
    u(Dk) = sqrt(u(X_R)^2 + u(X_L)^2) = sqrt( (delta_ins/√3)^2 + (delta_ins/√3)^2 )
          = delta_ins * sqrt(2/3)
    """
    return delta_ins * math.sqrt(2.0/3.0)

def calculate_combined_uncertainty_of_mean_Dk(type_A_uncertainty_of_mean, type_B_uncertainty_for_single_Dk_measurement):
    """
    计算平均直径 Dk_avg 的合成不确定度.
    u_total(Dk_avg) = sqrt( u_A(Dk_avg)^2 + u_B_instrumental^2 )
    这里的 u_B_instrumental 是指仪器对单次Dk测量的固有B类不确定度分量。
    """
    return math.sqrt(type_A_uncertainty_of_mean**2 + type_B_uncertainty_for_single_Dk_measurement**2)

# --- 主要数据处理逻辑 ---
if not user_data_groups:
    print("错误：用户数据列表 user_data_groups 为空，请输入数据后再运行。")
else:
    D1_values = []
    D11_values = []

    for group_data in user_data_groups:
        X1_L, X1_R, X11_L, X11_R = group_data
        # Dk = |Xk_right - Xk_left|
        d1 = abs(X1_R - X1_L)
        d11 = abs(X11_R - X11_L)
        D1_values.append(d1)
        D11_values.append(d11)

    N = len(user_data_groups) # 测量组数

    # --- D1 (第1暗环直径) 相关计算 ---
    mean_D1 = calculate_mean(D1_values)
    std_dev_D1 = calculate_std_dev(D1_values, mean_D1)
    uA_mean_D1 = calculate_type_A_uncertainty(std_dev_D1, N)

    # --- D11 (第11暗环直径) 相关计算 ---
    mean_D11 = calculate_mean(D11_values)
    std_dev_D11 = calculate_std_dev(D11_values, mean_D11)
    uA_mean_D11 = calculate_type_A_uncertainty(std_dev_D11, N)

    # --- B类不确定度计算 (由仪器误差极限引起，对每次Dk测量均适用) ---
    uB_instr_Dk = calculate_type_B_uncertainty_for_Dk_from_instrument(delta_ins_mm)

    # --- D1 和 D11 平均值的合成不确定度 ---
    u_total_mean_D1 = calculate_combined_uncertainty_of_mean_Dk(uA_mean_D1, uB_instr_Dk)
    u_total_mean_D11 = calculate_combined_uncertainty_of_mean_Dk(uA_mean_D11, uB_instr_Dk)

    # --- 计算牛顿环曲率半径 R ---
    # 公式: R = (D_m^2 - D_n^2) / (4 * (m-n) * λ)
    # 其中 m = m_ring (远环), n = n_ring (近环)
    denominator_R = 4 * (m_ring - n_ring) * lambda_mm
    if denominator_R == 0:
        R_calculated = float('nan') # 避免除以零
        print("错误: R的计算公式分母为零，请检查环数 m 和 n 或波长 λ。")
    else:
        R_calculated = (mean_D11**2 - mean_D1**2) / denominator_R

    # --- 计算 R 的不确定度 u_R ---
    # u_R = (1 / (2 * (m-n) * λ)) * sqrt( (D_m * u_D_m)^2 + (D_n * u_D_n)^2 )
    # D_m = mean_D11, u_D_m = u_total_mean_D11
    # D_n = mean_D1, u_D_n = u_total_mean_D1
    denominator_uR_factor = 2 * (m_ring - n_ring) * lambda_mm
    if denominator_uR_factor == 0:
        u_R = float('nan')
        if denominator_R != 0: # R 本身可能已计算，但uR分母为零（理论上与R分母一致）
             print("错误: u_R的计算公式分母为零，请检查环数 m 和 n 或波长 λ。")
    else:
        term_D11_sq_for_uR = (mean_D11 * u_total_mean_D11)**2
        term_D1_sq_for_uR = (mean_D1 * u_total_mean_D1)**2
        u_R = (1 / denominator_uR_factor) * math.sqrt(term_D11_sq_for_uR + term_D1_sq_for_uR)

    # --- 结果输出 ---
    print(f"--- 实验数据处理结果 (N = {N} 组) ---")
    print(f"常数: λ = {lambda_nm} nm, Δ_ins = {delta_ins_mm} mm, m = {m_ring}, n = {n_ring}")
    print("-" * 40)

    print("D1 (第1暗环直径) 计算:")
    print(f"  各组 D1 测量值 (mm): {[f'{val:.4f}' for val in D1_values]}")
    print(f"  平均值 D1_avg = {mean_D1:.4f} mm")
    print(f"  D1 值的标准差 S_D1 = {std_dev_D1:.4f} mm")
    print(f"  D1_avg 的 A 类不确定度 uA(D1_avg) = {uA_mean_D1:.4f} mm")
    print(f"  单次 Dk 测量的 B 类不确定度 uB(Dk_instr) = {uB_instr_Dk:.4f} mm")
    print(f"  D1_avg 的合成不确定度 u(D1_avg) = {u_total_mean_D1:.4f} mm")
    print(f"  因此, D1 = ({mean_D1:.4f} ± {u_total_mean_D1:.4f}) mm (未考虑有效数字)")
    print("-" * 40)

    print("D11 (第11暗环直径) 计算:")
    print(f"  各组 D11 测量值 (mm): {[f'{val:.4f}' for val in D11_values]}")
    print(f"  平均值 D11_avg = {mean_D11:.4f} mm")
    print(f"  D11 值的标准差 S_D11 = {std_dev_D11:.4f} mm")
    print(f"  D11_avg 的 A 类不确定度 uA(D11_avg) = {uA_mean_D11:.4f} mm")
    print(f"  D11_avg 的合成不确定度 u(D11_avg) = {u_total_mean_D11:.4f} mm")
    print(f"  因此, D11 = ({mean_D11:.4f} ± {u_total_mean_D11:.4f}) mm (未考虑有效数字)")
    print("-" * 40)

    print("牛顿环曲率半径 R 计算:")
    # 根据不确定度位数调整R的报告位数。通常不确定度取1-2位有效数字。
    # 这里简单用固定小数位，具体报告时应手动调整。
    # 例如，如果 u_R = 15.3 mm，则报告 u_R = 15 mm 或 u_R = 20mm。R的值保留到相应小数位。
    # 如果 u_R = 0.53 mm，则报告 u_R = 0.5 mm。R的值保留到0.1 mm。
    # 这是一个粗略的显示，精确的有效数字处理比较复杂。
    
    num_decimals_uR = 0
    if not math.isnan(u_R) and u_R != 0:
        if u_R >= 1: # e.g. u_R = 15.3 -> 0 decimals for R if u_R -> 15 or 20. u_R = 1.53 -> 1 decimal.
            # A simple rule: if u_R's first sig fig is >=3, use 1 sig fig for u_R. Else use 2.
            # Then match R's decimal places. For simplicity here, fixed decimals.
            # Let's try to estimate decimals for R and u_R.
            # For u_R, usually 1 or 2 significant figures.
            # Example: u_R = 23.45 -> 23. u_R = 2.345 -> 2.3. u_R = 0.2345 -> 0.23
            if u_R < 0.1: num_decimals_uR = 3 # e.g. 0.023
            elif u_R < 1: num_decimals_uR = 2 # e.g. 0.23
            elif u_R < 10: num_decimals_uR = 2 # e.g. 2.3
            elif u_R < 100: num_decimals_uR = 1 # e.g. 23
            else: num_decimals_uR = 0 # e.g. 123
    else: # u_R is NaN or 0
        num_decimals_uR = 2 # Default if cannot determine

    # Ensure R_calculated and u_R are not NaN before formatting
    r_val_str = f"{R_calculated:.{num_decimals_uR}f}" if not math.isnan(R_calculated) else "NaN"
    u_r_val_str = f"{u_R:.{num_decimals_uR}f}" if not math.isnan(u_R) else "NaN"

    print(f"  计算得到的 R = {r_val_str} mm")
    print(f"  R 的不确定度 u_R = {u_r_val_str} mm")
    print("-" * 40)

    print("最终结果表达式 (R = R_avg ± u_R):")
    print(f"  R = ({r_val_str} ± {u_r_val_str}) mm")
    print("注意: 上述输出中 R 和 u_R 的小数位数是初步估计，实际报告时请根据不确定度 u_R 的有效数字位数 (通常1-2位) 来调整 R 和 u_R 的表示。")
