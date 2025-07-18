import math

# --- 输入实验数据 ---
# 重物质量 (单位: 克 g)
mass_g = 25
# 塔轮半径 (单位: 毫米 mm)
radius_mm = 25
# 加速阶段的平均角加速度 (单位: 弧度/秒平方 rad/s²)
avg_angular_accel = 2.70786

# 重力加速度 (标准值 m/s²)
g = 9.8

# --- 数据有效性检查 ---
if mass_g <= 0 or radius_mm <= 0 or avg_angular_accel == 0:
    print("错误：质量(g)、半径(mm)必须大于0，加速阶段角加速度不能是0！请检查输入数据。")
else:
    # --- 开始计算 ---

    # 0. 单位换算：克转千克
    mass_kg = mass_g / 1000.0
    print(f"重物质量: {mass_g} g = {mass_kg:.4f} kg")

    # 1. 单位换算：毫米转米
    radius_m = radius_mm / 1000.0
    print(f"塔轮半径: {radius_mm} mm = {radius_m:.4f} m")

    # 2. 计算驱动力矩 τ = m(g - αr)r
    try:
        torque = mass_kg * (g - avg_angular_accel * radius_m) * radius_m
        
        # 检查力矩是否为负
        if torque < 0:
             print("\n警告：计算得到的驱动力矩为负值！")
             print(f"τ = {torque:.4e} N·m")
             print("这通常意味着 g < αr (即 α > g/r)。")
             print("可能原因：")
             print("  1. 测量数据有误，特别是角加速度或半径")
             print("  2. 摩擦力较大，被忽略了")
             print("  3. 理论模型不适用于当前实验装置")
             print("请检查数据和实验设置！")
        else:
            print(f"\n计算得到的驱动力矩 (τ): {torque:.4e} N·m")

        # 3. 计算总转动惯量 I_total = τ / α
        if avg_angular_accel == 0:
             print("角加速度为0，无法计算转动惯量！请检查数据。")
             moment_of_inertia = float('nan')
        else:
             moment_of_inertia = torque / avg_angular_accel
             print(f"计算得到的总转动惯量 (I_total): {moment_of_inertia:.4e} kg·m²")

    except Exception as e:
        print(f"\n计算出错！请检查输入数据是否为有效数字。错误信息：{e}")
        moment_of_inertia = float('nan')

    print("\n计算完成！")
