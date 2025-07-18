import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.interpolate import CubicSpline # 导入 CubicSpline

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# --- 请在这里输入您的实验数据 ---
# 电流数据 (单位: mA)，请按照电压从0V到5V，每隔0.5V的顺序输入11个电流值
# 例如: current_mA = [0.1, 0.5, 1.2, ...]
current_mA_input = [0.443, 0.470, 0.545, 0.582, 0.658, 0.816, 0.899, 0.963, 0.997, 1.099, 1.224]  # <--- 在这里填写您的11个电流数据
current_mA = np.array(current_mA_input) # 转换为numpy array，后续直接使用current_mA

# 实验时的环境温度 (单位: 开尔文 K)
# 例如: T = 298.15  (对应 25°C)
# T = None  # <--- 在这里填写您的实验温度 (K)  <- 温度输入被移除
# --- 数据输入结束 ---

# 物理常数
q = 1.602e-19  # 基本电荷 (C)
k = 1.38e-23   # 玻尔兹曼常数 (J/K)

# 检查数据完整性
if len(current_mA) != 11:
    print("错误：电流数据应为11个点！请检查输入。")
    exit()
# if T is None or T <= 0:  <- 温度校验被移除
#     print("错误：请输入有效的实验温度 (K)！")
#     exit()

# 电压数据 (V)
voltage = np.arange(0, 5.1, 0.5)

# 将电流从mA转换为A  <- 此步骤移除，直接使用mA单位
# current_A = np.array(current_mA) / 1000.0

# --- 绘制 I-U 曲线 ---
fig1, ax1 = plt.subplots(figsize=(10, 6)) # 获取figure和axes对象
ax1.plot(voltage, current_mA, 'o-', label='实验数据') # 使用 current_mA
ax1.set_xlabel('电压 U (V)')
ax1.set_ylabel('电流 I (mA)') # Y轴单位改为mA
ax1.set_title('太阳能电池伏安特性曲线 (I-U)')
ax1.grid(True)
ax1.legend()

# I-U 曲线: 突出X和Y轴, 原点在左下角 (0,0)
# ax1.spines['bottom'].set_position(('data', 0)) # 保持注释或移除，使用默认的轴线位置
# ax1.spines['left'].set_position(('data', 0))   # 保持注释或移除，使用默认的轴线位置

ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_color('black')
ax1.spines['left'].set_color('black') # 确保Y轴也是黑色
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# 强制x轴和y轴的下限为0
ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)

# 设置Y轴刻度从0开始，间隔0.1 (或根据数据调整)
# 找到电流最大值，并向上取到0.1的整数倍作为刻度上限
if len(current_mA) > 0:
    max_current = np.max(current_mA)
    y_tick_upper_limit = np.ceil(max_current / 0.1) * 0.1
    # 确保上限至少是0.1，避免最大电流很小时出现问题
    y_tick_upper_limit = max(y_tick_upper_limit, 0.1) 
    # 如果最大电流就是0.1的倍数，可能需要再加一个间隔，确保最大点可见
    if np.isclose(max_current, y_tick_upper_limit) and max_current > 0:
        y_tick_upper_limit += 0.1
    ax1.set_yticks(np.arange(0, y_tick_upper_limit + 0.01, 0.1)) # +0.01 确保上限包含在内

plt.savefig('I_U_curve.png')
print("I-U 曲线已保存为 I_U_curve.png")
# plt.show() # 如果需要直接显示图像，取消此行注释

# --- 计算 ln(I) 并处理电流为0或负值的情况 ---
valid_indices = current_mA > 0 # 基于 current_mA
voltage_fit = voltage[valid_indices]
current_mA_fit = current_mA[valid_indices] # 使用 current_mA_fit

if len(current_mA_fit) < 2:
    print("\n警告：有效电流数据点不足 (小于2个)，无法进行ln(I)-U拟合。")
    Is = np.nan
    # beta_eff = np.nan # 旧变量名
    beta_formula = np.nan # 新变量名，代表用户公式中的beta
    r_squared = np.nan
    print(f"Is = {Is}")
    # print(f"β*T = {beta_eff}") # 旧输出
    print(f"β (根据提供公式) = {beta_formula}") # 新输出
    print(f"R^2 (相关系数平方) = {r_squared}")

else:
    ln_current = np.log(current_mA_fit) # 对 current_mA_fit 取对数

    # --- 绘制 ln(I)-U 曲线并进行线性拟合 ---
    # 线性拟合: ln(I) = β*U + ln(Is) (根据用户公式)
    # 斜率 slope = β
    # 截距 intercept = ln(Is)
    slope, intercept, r_value, p_value, std_err = stats.linregress(voltage_fit, ln_current)
    r_squared = r_value**2

    # 计算拟合直线上的点
    ln_current_fit_line = slope * voltage_fit + intercept

    fig2, ax2 = plt.subplots(figsize=(10, 6)) # 获取figure和axes对象
    ax2.plot(voltage_fit, ln_current, 'o', label='实验数据 ln(I)') # 原始数据点
    ax2.plot(voltage_fit, ln_current_fit_line, 'r-', label=f'线性拟合: y={slope:.4f}x + {intercept:.4f}\nR$^2$ = {r_squared:.4f}')

    # --- 添加通过数据点的平滑连接曲线 (样条插值) ---
    if len(voltage_fit) >= 2: # 确保至少有两个点可以进行插值
        # 创建样条插值函数
        cs = CubicSpline(voltage_fit, ln_current)
        # 生成更密集的电压点用于绘制平滑曲线
        voltage_smooth = np.linspace(voltage_fit.min(), voltage_fit.max(), 300)
        # 计算平滑曲线上的ln(I)值
        ln_current_smooth = cs(voltage_smooth)
        ax2.plot(voltage_smooth, ln_current_smooth, 'b--', label='数据点平滑连接 (样条插值)')
    # --- 平滑连接结束 ---

    ax2.set_xlabel('电压 U (V)')
    ax2.set_ylabel('ln(电流 I (mA))') # Y轴单位改为ln(mA)
    ax2.set_title('太阳能电池 ln(I)-U 特性曲线及线性拟合')
    ax2.grid(True)
    ax2.legend()

    # 突出X和Y轴, 并将交点设置在(0,0)
    ax2.spines['bottom'].set_position(('data', 0))
    ax2.spines['left'].set_position(('data', 0))
    ax2.spines['bottom'].set_linewidth(1.5)
    ax2.spines['left'].set_linewidth(1.5)
    ax2.spines['bottom'].set_color('black')
    ax2.spines['left'].set_color('black')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.savefig('lnI_U_curve.png')
    print("\nln(I)-U 曲线已保存为 lnI_U_curve.png")
    # plt.show() # 如果需要直接显示图像，取消此行注释

    # --- 计算常数 β 和 Is (根据用户提供的公式体系) ---
    # 根据用户公式 ln(I) = β*U + ln(Is)，斜率 slope 即为 β
    beta_formula = slope  # β 直接就是拟合得到的斜率
    
    # if slope == 0: # 此部分不再需要，因为 beta_formula = slope 自然处理 slope = 0 的情况
    #     beta_eff = np.inf # 斜率为0，beta_eff趋于无穷大
    #     print("\n警告：拟合曲线斜率为0，无法精确计算 β_eff。")
    # else:
    #     # beta_eff = q / (slope * k)    # 旧计算公式，不依赖T
    
    Is = np.exp(intercept) # Is = e^(intercept)，单位现在是 mA

    print("\n拟合结果 (基于用户提供公式 lnI = βU + lnIs)：")
    print(f"线性拟合方程: ln(I) = {slope:.4f} * U + {intercept:.4f}")
    print(f"相关系数平方 (R^2): {r_squared:.4f}")
    print(f"计算得到的反向饱和电流 Is: {Is:.4e} mA") # Is 单位改为 mA
    # print(f"计算得到的有效 β (β*T): {beta_eff:.4f} K") # 旧输出
    print(f"计算得到的常数 β (斜率): {beta_formula:.4f} V^-1") # beta 单位不变

print("\n--- 分析完成 ---")
