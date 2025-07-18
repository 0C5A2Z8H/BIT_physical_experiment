# 北理工大学物理实验指导V1.0

​	北京理工大学大一上开设有《大学物理实验Ⅰ》课程，学生须在[选课网站](https://webvpn.bit.edu.cn/https/77726476706e69737468656265737421e8fc0f9e2e2426557a1dc7af96/xsxkapp/sys/xsxkapp/*default/index.do)上选修十门物理实验课程，并根据课后提交的实验报告评分。

>实验报告 = 预习报告 + 原始数据 + 数据处理 + 思考题

## 实验报告格式

### 1 预习报告

​	部分实验用教材，部分实验用[讲义](https://pan.baidu.com/share/init?surl=EkUYU9W9eLU8YB8oUVNc8g?pwd=2fkz)。

​	用教材预习的实验项目：力学基本量的测量、示波器实验、转动惯量实验、分光计调整、杨氏模量实验（其中序号为1-16号的同学做动态法测杨氏模量、序号为17-30号的同学做静态法测杨氏模量，预习报告只写自己需要做的部分。序号在已选课程中查看。）

​	用讲义预习的实验项目：太阳能电池实验、热机循环实验、光的干涉、薄透镜焦距的测量、直流双臂电桥实验、迈克尔逊干涉仪。

​	预习报告仅需抄写教材或讲义的内容。

​	实验课后找老师盖章。

### 2 原始数据

​	实验课上记录后找老师盖章。

### 3 数据处理

#### 不确定度的计算

在物理实验中，任何测量都存在不确定度。不确定度是表征测量结果分散性的一个参数，它反映了我们对被测量真值所处范围的认识。

##### 1. A类不确定度 (统计不确定度)

A类不确定度由测量数据在重复观测条件下的随机变化所引起，可以通过对多次测量结果进行统计分析来评定。

对于n次重复测量得到的测量值 $x_1, x_2, ..., x_n$：

1.  **计算算术平均值 (最佳估计值):**
<div align="center">
<img src="https://latex.codecogs.com/svg.latex?%5Clarge%20%5Cbar%7Bx%7D%20%3D%20%5Cfrac%7B%5Csum%20x_i%7D%7Bn%7D" />
</div>

2.  **计算单次测量的标准差 (实验标准差):**
<div align="center">
<img src="https://latex.codecogs.com/svg.latex?%5Clarge%20s(x_i)%20%3D%20%5Csqrt%7B%5Cfrac%7B%5Csum%20(x_i%20-%20%5Cbar%7Bx%7D)%5E2%7D%7Bn-1%7D%7D" />
</div>

3.  **计算A类不确定度:**
<div align="center">
<img src="https://latex.codecogs.com/svg.latex?%5Clarge%20u_A%20%3D%20%5Cfrac%7Bs(x_i)%7D%7B%5Csqrt%7Bn%7D%7D" />
</div>

##### 2. B类不确定度 (系统不确定度)

B类不确定度由非统计因素引起，如仪器误差、环境因素等。其评定需要基于经验、仪器说明书、校准证书等信息。

*   **仪器误差:** 通常取仪器最小分度值的一半。例如，对于最小分度值为0.1mm的刻度尺，其B类不确定度为 $u_B = 0.1 / 2 = 0.05 \text{ mm}$。
*   **数字显示仪器:** B类不确定度通常取最后一位的半个字。

##### 3. 合成不确定度

当测量结果由多个独立的物理量 $x, y, ...$ 通过函数 $f(x, y, ...)$ 计算得到时，其合成不确定度 $u_c$ 的计算公式如下：

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?%5Clarge%20u_c%20%3D%20%5Csqrt%7B(%5Cfrac%7B%5Cpartial%20f%7D%7B%5Cpartial%20x%7D)%5E2%20u(x)%5E2%20%2B%20(%5Cfrac%7B%5Cpartial%20f%7D%7B%5Cpartial%20y%7D)%5E2%20u(y)%5E2%20%2B%20...%7D" />
</div>

其中 $u(x)$ 和 $u(y)$ 分别是 $x$ 和 $y$ 的总不确定度 (如果同时存在A类和B类不确定度，则下式成立)：
<div align="center">
<img src="https://latex.codecogs.com/svg.latex?%5Clarge%20u(x)%20%3D%20%5Csqrt%7Bu_A(x)%5E2%20%2B%20u_B(x)%5E2%7D" />
</div>

##### 4. 最终结果表示

物理实验的最终结果应表示为：

结果 = 最佳估计值 ± 合成不确定度

例如： $L = (10.5 \pm 0.1) \text{ cm}$ 

