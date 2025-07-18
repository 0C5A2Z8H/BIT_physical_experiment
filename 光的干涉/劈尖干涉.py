import math

# --- 用户输入区 ---
# 请将你的实验数据填入下面的列表中
# 每组数据格式为: (X_initial, X_final, L_initial, L_final) 单位: mm
# X_initial: 10条暗纹的起始位置读数
# X_final: 10条暗纹的终止位置读数 (x = |X_final - X_initial|)
# L_initial: 劈尖总长度的起始位置读数
# L_final: 劈尖总长度的终止位置读数 (L_val = |L_final - L_initial|)

user_data_groups = [
    # (X_initial, X_final, L_initial, L_final) in mm
    (24.498, 27.298, 2.492, 35.412), # 示例: x=2.31, L=50.000
    (20.301, 23.088, 2.458, 35.412),
    (16.512, 19.385, 2.435, 35.412),
    (12.428, 15.370, 2.478, 35.412),
    (8.642, 11.592, 2.408, 35.412),
]

# --- 常量定义 ---
lambda_nm = 589.3  # 光的波长 (nm)，例如钠黄光平均波长。请根据实际情况修改。
k_fringes = 10     # 测量的暗纹条数 (固定为10)
delta_ins_mm = 0.005 # 仪器允许误差极限 (mm)，例如与牛顿环实验相同。请根据实际情况修改。
# --- END 用户输入区 ---

lambda_mm = lambda_nm * 1e-6  # 波长转换为 mm

# --- 辅助计算函数 ---
def calculate_mean(values):
    """计算平均值"""
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_std_dev(values, mean_val):
    """计算样本标准差"""
    n = len(values)
    if n < 2:
        return 0.0
    return math.sqrt(sum([(x_val - mean_val)**2 for x_val in values]) / (n - 1))

def calculate_type_A_uncertainty(std_dev, num_measurements):
    """计算A类不确定度 (平均值的标准误差)"""
    if num_measurements == 0:
        return float('inf')
    if num_measurements == 1 and std_dev == 0.0:
        return 0.0
    return std_dev / math.sqrt(num_measurements) if num_measurements > 0 else float('inf')

def calculate_type_B_uncertainty_from_instrument_two_readings(delta_ins):
    """计算由两次读数确定的长度 (如 x 或 L) 因仪器误差极限引起的B类不确定度"""
    # u(Reading) = delta_ins / sqrt(3)
    # u(Length = |R2 - R1|) = sqrt(u(R1)^2 + u(R2)^2) = delta_ins * sqrt(2/3)
    return delta_ins * math.sqrt(2.0/3.0)

def calculate_combined_uncertainty_of_mean_length(type_A_uncertainty_of_mean, type_B_uncertainty_single_measurement):
    """计算平均长度 (如 x_avg 或 L_avg) 的合成不确定度"""
    # u_total(Length_avg) = sqrt( u_A(Length_avg)^2 + u_B_instrumental^2 )
    return math.sqrt(type_A_uncertainty_of_mean**2 + type_B_uncertainty_single_measurement**2)

# --- 主要数据处理逻辑 ---
if not user_data_groups:
    print("错误：用户数据列表 user_data_groups 为空，请输入数据后再运行。")
else:
    x_values = []  # 存储每组计算得到的10条暗纹长度x
    L_measurement_values = [] # 存储每组计算得到的劈尖总长度L

    for group_data in user_data_groups:
        X_init, X_fin, L_init, L_fin = group_data
        x_i = abs(X_fin - X_init)       # 计算单组的10条暗纹长度
        L_val_i = abs(L_fin - L_init) # 计算单组的劈尖总长度
        x_values.append(x_i)
        L_measurement_values.append(L_val_i)

    N = len(user_data_groups) # 测量组数

    # --- 10条暗纹长度 x 相关计算 ---
    mean_x = calculate_mean(x_values)
    std_dev_x = calculate_std_dev(x_values, mean_x)
    uA_mean_x = calculate_type_A_uncertainty(std_dev_x, N)

    # --- 劈尖总长度 L 相关计算 ---
    mean_L = calculate_mean(L_measurement_values)
    std_dev_L = calculate_std_dev(L_measurement_values, mean_L)
    uA_mean_L = calculate_type_A_uncertainty(std_dev_L, N)

    # --- B类不确定度计算 (由仪器误差极限引起，对每次x或L的测量均适用) ---
    uB_instr_length = calculate_type_B_uncertainty_from_instrument_two_readings(delta_ins_mm)

    # --- x 和 L 平均值的合成不确定度 ---
    u_total_mean_x = calculate_combined_uncertainty_of_mean_length(uA_mean_x, uB_instr_length)
    u_total_mean_L = calculate_combined_uncertainty_of_mean_length(uA_mean_L, uB_instr_length)

    # --- 计算玻璃丝直径 D --- (公式 D = L * lambda * k / (2*x))
    if mean_x == 0:
        D_calculated = float('nan')
        print("错误: 计算D时，平均x值为0，无法计算。")
    else:
        D_calculated = (mean_L * lambda_mm * k_fringes) / (2 * mean_x)

    # --- 计算 D 的不确定度 u_D ---
    # u_D = D_avg * sqrt( (u_L_avg/L_avg)^2 + (u_x_avg/x_avg)^2 )
    u_D = float('nan')
    if not math.isnan(D_calculated) and mean_L != 0 and mean_x != 0:
        term_L_rel_err_sq = (u_total_mean_L / mean_L)**2
        term_x_rel_err_sq = (u_total_mean_x / mean_x)**2
        if term_L_rel_err_sq >= 0 and term_x_rel_err_sq >=0: # Ensure non-negative before sqrt
            u_D = abs(D_calculated) * math.sqrt(term_L_rel_err_sq + term_x_rel_err_sq)
    elif math.isnan(D_calculated):
        pass # D is already NaN, u_D will remain NaN
    else:
        print("警告: 由于平均L或平均x为零，无法精确计算u_D。")

    # --- 结果输出 ---
    print(f"--- 劈尖干涉实验数据处理结果 (N = {N} 组) ---")
    print(f"常数: λ = {lambda_nm} nm, k = {k_fringes} 条暗纹, Δ_ins = {delta_ins_mm} mm")
    print("-" * 60)

    print("1. 10条暗纹总长度 x 计算 (单位: mm):")
    print(f"  各组 x 测量值: {[f'{val:.4f}' for val in x_values]}")
    print(f"  平均值 x_avg = {mean_x:.4f} mm")
    print(f"  x 值的标准差 S_x = {std_dev_x:.4f} mm")
    print(f"  x_avg 的 A 类不确定度 uA(x_avg) = {uA_mean_x:.4f} mm")
    print(f"  单次长度测量的 B 类不确定度 uB(instr) = {uB_instr_length:.4f} mm")
    print(f"  x_avg 的合成不确定度 u_c(x_avg) = {u_total_mean_x:.4f} mm")
    print(f"  因此, x = ({mean_x:.4f} ± {u_total_mean_x:.4f}) mm (未规范有效数字)")
    print("-" * 60)

    print("2. 劈尖总长度 L 计算 (单位: mm):")
    print(f"  各组 L 测量值: {[f'{val:.4f}' for val in L_measurement_values]}")
    print(f"  平均值 L_avg = {mean_L:.4f} mm")
    print(f"  L 值的标准差 S_L = {std_dev_L:.4f} mm")
    print(f"  L_avg 的 A 类不确定度 uA(L_avg) = {uA_mean_L:.4f} mm")
    print(f"  L_avg 的合成不确定度 u_c(L_avg) = {u_total_mean_L:.4f} mm")
    print(f"  因此, L = ({mean_L:.4f} ± {u_total_mean_L:.4f}) mm (未规范有效数字)")
    print("-" * 60)

    print("3. 玻璃丝直径 D 计算 (单位: mm):")
    num_decimals_uD = 0
    if not math.isnan(u_D) and u_D != 0:
        # 简单规则：u_D首位有效数字若>=3，u_D取1位有效数字，否则取2位。
        # D的小数位数与u_D对齐。
        # 此处为简化显示，具体报告时应手动调整。
        abs_u_D = abs(u_D)
        if abs_u_D == 0: # Avoid log(0)
             num_decimals_uD = 4 # Default if u_D is zero
        elif abs_u_D < 0.0001: # very small uncertainty
            num_decimals_uD = 5
        else:
            # Determine number of significant figures for u_D (1 or 2)
            # first_digit = int(str(abs_u_D).replace('.', '').lstrip('0')[0])
            # num_sig_figs_uD = 1 if first_digit >=3 else 2
            # This logic is tricky, using a simpler fixed approach for now based on magnitude
            if abs_u_D < 0.001: num_decimals_uD = 5 # e.g. 0.00023
            elif abs_u_D < 0.01: num_decimals_uD = 4 # e.g. 0.0023
            elif abs_u_D < 0.1: num_decimals_uD = 3  # e.g. 0.023
            elif abs_u_D < 1: num_decimals_uD = 3    # e.g. 0.23 (or 0.2 if 1 sig fig)
            else: num_decimals_uD = 2 # e.g. 1.2 or 12.3 (adjust D accordingly)
    else:
        num_decimals_uD = 3 # Default if u_D is NaN or zero, or cannot determine
    
    # 确保 D_calculated 和 u_D 不是 NaN
    d_val_str = f"{D_calculated:.{num_decimals_uD}f}" if not math.isnan(D_calculated) else "NaN"
    u_d_val_str = f"{abs(u_D):.{num_decimals_uD}f}" if not math.isnan(u_D) else "NaN"

    print(f"  计算得到的 D = {d_val_str} mm")
    print(f"  D 的不确定度 u_D = {u_d_val_str} mm")
    print("-" * 60)

    print("最终结果表达式 (D = D_avg ± u_D):")
    print(f"  D = ({d_val_str} ± {u_d_val_str}) mm")
    print("注意: 上述输出中 D 和 u_D 的小数位数是初步估计，实际报告时请根据不确定度 u_D 的有效数字位数 (通常1-2位) 来规范调整 D 和 u_D 的表示。")
