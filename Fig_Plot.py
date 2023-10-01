import os
import statistics

import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
from scipy.stats import stats


# 因为开始dosing之后，气体的变化需要一段时间才能被检测到，所以要找这一个时间段的offset.
# index_1: start dosing index,index_2: end dosing index
def find_offset_time_plot(df, time_1, time_2, time_3, export_path, id):
    index_1 = df.index[df['Zeit'] == time_1][0]
    index_2 = df.index[df['Zeit'] == time_2][0]

    # 在dosing的时候的时间区间以及CO2浓度变化
    selected_time = df['Time_start_from_Zero'][index_1: index_2 + 1]
    selected_co2 = df['Abgas CO2 Vol %'][index_1: index_2 + 1]
    # 计算CO2的前三分钟平均值
    co2_mean = df['Abgas CO2 Vol %'][index_1 - 180:index_1].mean()

    # 整个实验的时间区间以及CO2浓度变化
    time = df['Time_start_from_Zero']
    co2 = df['Abgas CO2 Vol %']

    plot_name = f"{id}_{time_3} CO2 Vol % "

    # 设置全局字体
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial']

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(time, co2, label=r'$CO_2$ concentration in gasout')
    # 设置x轴日期间隔为3分钟

    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    # ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax.fill_between(x=selected_time, y1=selected_co2, y2=co2_mean, label=r"Captured $CO_2$")
    ax.set_ylim(3, 12)

    # 在图上标注开始和结束dossier的时间
    start_time = selected_time.iloc[0]
    end_time = selected_time.iloc[-1]

    ax.axvline(x=start_time, color='gray', linestyle='dashed', linewidth=1)
    ax.axvline(x=end_time, color='gray', linestyle='dashed', linewidth=1)

    # # 添加起始时间的标注
    # ax.annotate(f'Start Time: {start_time}', (start_time, ax.get_ylim()[0]), xytext=(10, 20),
    #             textcoords='offset points', arrowprops={'arrowstyle': '->'})
    #
    # # 添加结束时间的标注
    # ax.annotate(f'End Time: {end_time}', (end_time, ax.get_ylim()[0]), xytext=(10, 20),
    #             textcoords='offset points', arrowprops={'arrowstyle': '->'})

    # # 添加开始和结束时间的标注
    # plt.annotate(f"Begin dosing: {start_time}", xy=(start_time, df_2['Time_start_from_Zero'].iloc[0]),
    #              xytext=(start_time, df['value'].iloc[0] + 5),
    #              arrowprops=dict(facecolor='black', shrink=0.05),
    #              fontsize=10)
    #
    # plt.annotate(f"End dosing: {end_time}", xy=(end_time, df['Time_start_from_Zero'].iloc[-1]),
    #              xytext=(end_time, df['value'].iloc[-1] - 5),
    #              arrowprops=dict(facecolor='black', shrink=0.05),
    #              fontsize=10)

    ax.set_xlabel('Time in hh:mm')

    ax.set_ylabel(r'Captured $CO_2$ Vol %')
    ax.set_title(r'$CO_2$ Concentration change over time')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 显示图表
    plt.savefig("{}.png".format(os.path.join(export_path, plot_name)), dpi=400)
    plt.show()


# Analysis
# time_1 is offset time
def Mass_flow_and_feed_rate_plot(df, Export_Path, id):
    # 创建一个新的 Matplotlib 图形

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制左侧纵轴（Waage abs 和 Waage abs smoothed）的折线图
    color1 = 'tab:blue'
    color2 = 'tab:orange'
    ax1.set_xlabel('Time in hh:mm')
    ax1.set_ylabel('Mass in kg')
    # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    line1, = ax1.plot(df['Time'], df['Waage_abs_kg'], color=color1, label='Mass')
    line1.set_alpha(0.5)
    line2, = ax1.plot(df['Time'], df['Waage_abs_fil'], color=color2, label='Mass smoothed')

    # ax1.tick_params(axis='y')

    # 在图上标注开始和结束dossier的时间
    start_time = df['Time'].iloc[180]
    end_time = df['Time'].iloc[-181]
    ax1.axvline(x=start_time, color='gray', linestyle='dashed', linewidth=1)
    ax1.axvline(x=end_time, color='gray', linestyle='dashed', linewidth=1)

    ax2 = ax1.twinx()
    # 绘制右侧纵轴（feed rate）的折线图
    color = 'tab:gray'
    ax2.set_ylabel('Mass flow in kg/h')

    line3, = ax2.plot(df['Time'], df['Sorbent mass flow_1 kg/h'], color=color, label='Mass flow')
    line3.set_alpha(0.5)
    line4, = ax2.plot(df['Time'], df['Sorbent mass flow_2 kg/h'], color='tab:red', label='Mass flow smoothed')
    ax2.set_ylim(-3, 5)

    # 合并图例
    lines = [line1, line2, line3, line4]
    # lines = [line2,line4]
    labels = [line.get_label() for line in lines]

    ax1.legend(lines, labels, loc='upper right')

    # 设置 x 轴的日期格式化
    date_format = plt.matplotlib.dates.DateFormatter('%H:%M')
    ax1.xaxis.set_major_formatter(date_format)

    # 添加标题和图例
    plt.title('Mass flow and Feed rate change over time')
    # plt.legend()

    # 自动调整布局以适应标签
    plt.tight_layout()

    # 显示图形
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Mass flow and feed rate")), dpi=400)


# df_1 is df_feed_rate, df_2 is df_Gasout_2
def feed_rate_and_CO2_concentration_plot(df, Export_Path, id):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    # 绘制左侧纵轴（Waage abs 和 Waage abs smoothed）的折线图
    color1 = 'tab:blue'
    ax1.set_xlabel('Time in hh:mm')
    ax1.set_ylabel(r'$CO_2$ concentration Vol %')
    # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    line1, = ax1.plot(df['Time_start_from_Zero'], df['Abgas CO2 Vol %'], color=color1,
                      label=r'$CO_2$ concentration VOl %')
    ax1.set_ylim(3, 12)
    # ax1.tick_params(axis='y')

    # 在图上标注开始和结束dossier的时间
    start_time = df['Time_start_from_Zero'].iloc[180]
    end_time = df['Time_start_from_Zero'].iloc[-181]
    ax1.axvline(x=start_time, color='gray', linestyle='dashed', linewidth=1)
    ax1.axvline(x=end_time, color='gray', linestyle='dashed', linewidth=1)

    # TODO: 添加起始时间的标注
    ax2 = ax1.twinx()
    # 绘制右侧纵轴（feed rate）的折线图
    color = 'tab:gray'
    ax2.set_ylabel('Mass flow in kg/h')
    # line3, = ax2.plot(df['Time'], df['mass_change_per_hour'], color=color, label='Mass flow')
    line4, = ax2.plot(df['Time_start_from_Zero'], df['Sorbent mass flow_2 kg/h'], color='tab:red',
                      label='Mass flow smoothed')
    ax2.set_ylim(-1, 5)
    # ax2.tick_params(axis='y') 是 Matplotlib 中用于配置图形的刻度参数的方法之一，特别是用于配置 y 轴的刻度。这个方法允许您自定义刻度的显示方式，例如刻度的方向、颜色、标签等。
    # ax2.tick_params(axis='y')

    # 合并图例
    # lines = [line1, line3, line4]
    lines = [line1, line4]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper right')

    # 设置 x 轴的日期格式化
    date_format = plt.matplotlib.dates.DateFormatter('%H:%M')
    ax1.xaxis.set_major_formatter(date_format)

    # 添加标题和图例
    plt.title(r'$CO_2$ Concentration and Feed Rate over time')

    # 自动调整布局以适应标签
    plt.tight_layout()
    # 显示图形
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} CO2 Vol % and feed rate")), dpi=400)


def E_CO2_plot(df, Export_Path, id):
    y1 = df['E_CO2']
    y2 = df['Abgas CO2 Vol %']
    x = df['Time_start_from_Zero']
    fig, ax1 = plt.subplots(figsize=(10, 6))

    line1, = ax1.plot(x, y1, label=r'$E_{carb}$ ', color='tab:blue')
    # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax2 = ax1.twinx()
    line2, = ax2.plot(x, y2, label=r'$CO_2$ %Vol', color='tab:red')
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time in hh:mm')
    ax1.set_ylabel(r'$CO_2$ Capture Efficiency $E_{carb}$')
    ax2.set_ylabel(r'$CO_2$ Concentration %Vol')
    ax1.set_title(r'$E_{carb}$ and $CO_2$ %Vol over Time')

    # 合并图例
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper right')

    # plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} CO2 Vol % and E_carb")), dpi=400)

    plt.show()


def E_plot(df, E_CO2, Export_Path, id):
    y1 = E_CO2
    y2 = df['Abgas CO2 Vol %']
    x = df['Time_start_from_Zero']

    fig, ax1 = plt.subplots(figsize=(10, 6))

    line1, = ax1.plot(x, y1, label=r'$E_{carb}$ ', color='tab:blue')
    # ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    ax2 = ax1.twinx()
    line2, = ax2.plot(x, y2, label='Corrected CO2 %Vol', color='tab:red')
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
    ax1.set_xlabel('Time in hh:mm')
    ax1.set_ylabel(r'$CO_2$ Capture Efficiency $E_{carb}$')
    ax2.set_ylabel(r'$CO_2$ Concentration %Vol')
    ax1.set_title(r'$E_{carb}$ and $CO_2$ %Vol over Time')

    # 合并图例
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper right')

    # plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} CO2 Vol % and E_carb")), dpi=400)


def E_feed_rate_plot(df, Export_Path, id):
    # 提取数据
    y = df['E_CO2'][180:-181]
    x = df['Sorbent mass flow_2 kg/h'][180:-181]

    # 执行线性拟合
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # 创建拟合直线的x坐标值
    x_fit = np.linspace(x.min(), x.max(), 100)

    # 使用线性方程计算y坐标值
    # y_fit = slope * x_fit + intercept

    # 执行多项式拟合 (这里示范了二次多项式拟合)
    degree = 2
    coeffs = np.polyfit(x, y, degree)
    poly_eq = np.poly1d(coeffs)
    # y_poly_fit = poly_eq(x_fit)

    # 计算R²值
    # r_squared = r_value ** 2

    # 绘制散点图
    plt.scatter(x, y, label='Data Points', alpha=0.5)

    # 绘制拟合直线
    # plt.plot(x_fit, y_fit, color='red', label='Linear Fit')

    # 绘制多项式拟合曲线
    # plt.plot(x_fit, y_poly_fit, color='green', label=f'Polynomial Fit (degree {degree})')

    # 添加标签和图例
    plt.xlabel('Feed rate kg/h')
    plt.ylabel(r'$E_{carb}$')
    plt.legend()

    # 标注R²值
    # plt.annotate(f'R² = {r_squared:.4f}', (0.5, 0.95), xycoords='axes fraction', fontsize=12)
    plt.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Feed Rate and E_carb")), dpi=400)
    # 显示图形
    plt.show()


def E_X_Sorbent_plot(df, Export_Path, id):
    y1 = df['X_CO2']
    x = df['E']

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id}CO2 Vol % and E_carb")), dpi=400)


# T 的绘图
def T_H_plot(df, Export_Path, id):
    df_T = df.drop('Zeit', axis=1)
    height = [0.195, 0.705, 1.210, 2.300, 4.089, 5.4533, 6.405, 8.200, 9.965, 10.990]

    column_mean = df_T.mean(axis=0)
    df_column_mean = column_mean.to_frame()
    df_column_mean['height in m'] = height
    df_column_mean = df_column_mean.rename(columns={0: 'temperature in °C'})
    # temperature_mean = df_column_mean['temperature in °C'].mean()

    # plot temperature profile
    x = df_column_mean['temperature in °C']
    y = df_column_mean['height in m']

    # 创建一个自定义字体对象
    # font = {'family': 'Times New Roman'}

    # 创建一个新的图表并设置大小
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.plot(x, y, color='black', linewidth=1, marker='o', markersize=4)

    # 设置网格线
    plt.grid(True, alpha=0.3)

    # # 设置纵线和横线的格式
    # plt.gca().xaxis.grid(alpha=0.2)
    # plt.gca().yaxis.grid(alpha=1)

    # # 在Y轴上绘制平均刻度和小刻度
    # ax = plt.gca()
    ax.set_xlim([400, 700])
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    # ax.tick_params(axis='y', direction='in', which='minor')

    # 自定义X轴和Y轴标签
    ax.set_title('Temperature profile')
    ax.set_xlabel('Temperature in °C')
    ax.set_ylabel('Height in m')

    plt.tight_layout()
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Temperature profile")), dpi=400)


def TP_H_Plot(df_1, df_2, Export_Path, id):
    df_1 = df_1.drop('Zeit', axis=1)
    df_2 = df_2.drop('Zeit', axis=1)

    # 计算平均温度和平均压力
    Mean_Temp = df_1.mean()
    Mean_Pressure = df_2.mean()

    Max_P = Mean_Pressure.max()
    Min_P = Mean_Pressure.min()

    Mean_Temp_list = Mean_Temp.tolist()
    Mean_Pressure_list = Mean_Pressure.tolist()

    Height_T = (0.195, 0.705, 1.210, 2.300, 4.089, 5.453, 6.405, 8.200, 9.965, 10.990)
    Height_P = (0.195, 1.210, 1.900, 3.389, 4.790, 6.405, 8.200, 9.965, 10.990, 10.990, 10.990)

    x1 = Mean_Temp_list
    x2 = Mean_Pressure_list

    x1_median = statistics.median(map(float, x1))
    # x2_median = statistics.median(map(float, x2))
    x1_lim = [round((x1_median - (x1_median * 0.8)) / 50) * 50, round((x1_median + (x1_median * 0.2)) / 50) * 50]
    # x2_lim = [round((x2_median - (x2_median * 0.8)) / 5) * 5, round((x2_median + (x2_median * 0.2)) / 5) * 5]
    x2_lim = [round(Min_P) - 2, round(Max_P) + 2]

    y1 = Height_T
    y2 = Height_P

    fig, ax1 = plt.subplots(1, figsize=(5, 7))

    ax1.plot(x1, y1, color="red", ls="-", lw=1, marker='o', ms=4, label=r"Temperature")
    ax1.set_xlim(x1_lim)
    ax2 = ax1.twiny()
    ax2.plot(x2, y2, color="blue", ls="-", lw=1, marker='^', ms=4, label=r"Pressure")
    ax2.set_xlim(x2_lim)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel("Temperature in degree Celcius")
    ax2.set_xlabel("Relative Pressure in mbar")
    ax1.set_ylabel("Height in meter")
    ax1.set_title("Temperature & Pressure profile")
    ax1.legend(bbox_to_anchor=(0.35, 0.88), loc="lower left")
    ax2.legend(bbox_to_anchor=(0.35, 0.82), loc="lower left")

    # fig.tight_layout()
    plt.tight_layout()
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Temperature and Pressure profile")), dpi=400)


# 读取压力数据并绘制图表：整体平均值，不包含Pg208, Pg221
def P_plot_1(df, Export_Path, id):
    # 循环遍历每一行数据
    df = df.drop('Zeit', axis=1)
    # 'Pg201 0.195', 'Pg202 1.210', 'Pg203 1.900', 'Pg204 3.389', 'Pg234 4.790', 'Pg205 6.405',
    # 'Pg206 8.200', 'Pg207 9.965', 'Pg208 10.990', 'Pg221 10.990', 'Pg222 10.990'
    P_height = [0.195, 1.900, 4.790, 6.405, 8.200, 9.963, 10.990]

    # 指定新的列顺序
    new_columns = ['Pg201 mbar', 'Pg203 mbar', 'Pg204 mbar', 'Pg234 mbar', 'Pg205 mbar',
                   'Pg206 mbar', 'Pg207 mbar']

    df = df[new_columns]
    P_mean = df.mean(axis=0)
    df_P_mean = P_mean.to_frame()
    df_P_mean['height in m'] = P_height
    df_P_mean = df_P_mean.rename(columns={0: 'pressure in mbar'})

    x = df_P_mean['pressure in mbar']
    y = df_P_mean['height in m']

    # 创建一个自定义字体对象
    # font = {'family': 'Times New Roman'}

    # 创建一个新的图表并设置大小
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.plot(x, y, color='black', linewidth=1, marker='o', markersize=4)

    # 设置X轴尺度范围
    # TODO: 设置X轴尺度范围
    x_max = max(map(float, x))
    x_min = min(map(float, x))

    # x_median = statistics.median(map(float, x))
    # x_lim = [0, round((x_median + (x_median * 3)) / 5) * 5]
    x_lim = [round(x_min - 2), round(x_max + 2)]
    ax.set_xlim(x_lim)
    ax.set_ylim([0, 12])

    # 设置网格线
    plt.grid(True)

    # 设置纵线和横线的格式
    plt.gca().xaxis.grid(alpha=0.2)
    plt.gca().yaxis.grid(alpha=0.2)

    # 在Y轴上绘制平均刻度和小刻度
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    # ax.tick_params(axis='y', direction='in', which='minor')

    # 自定义X轴和Y轴标签
    ax.set_title('Pressure profile')
    ax.set_xlabel('Pressure in mbar')
    ax.set_ylabel('Height in m')

    # 保存图表为PNG文件
    plt.tight_layout()
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Pressure profile 1")), dpi=400)


# 读取压力数据并绘制图表：每个传感器的平均值,包含Pg208, Pg221
def P_plot_2(df, Export_Path, id):
    # 循环遍历每一行数据
    df = df.drop('Zeit', axis=1)

    # 'Pg201 0.195', 'Pg202 1.210', 'Pg203 1.900','Pg233 3.389 ' 'Pg204 4.790', 'Pg234 6.405',
    # 'Pg205 8.200', 'Pg206 9.965', 'Pg207 10.990', 'Pg208 10.990', 'Pg22 10.990'
    P_height = [0.195, 1.210, 1.900, 3.389, 4.790, 6.405, 8.200, 9.965, 10.990, 10.990, 10.990]

    # 指定新的列顺序
    new_columns = ['Pg201 mbar', 'Pg202 mbar', 'Pg203 mbar', 'Pg233 mbar', 'Pg204 mbar', 'Pg234 mbar', 'Pg205 mbar',
                   'Pg206 mbar', 'Pg207 mbar', 'Pg208 mbar', 'Pg221 mbar']

    df = df[new_columns]
    P_mean = df.mean(axis=0)
    df_P_mean = P_mean.to_frame()
    df_P_mean['height in m'] = P_height
    df_P_mean = df_P_mean.rename(columns={0: 'pressure in mbar'})

    x = df_P_mean['pressure in mbar']
    y = df_P_mean['height in m']

    # 创建一个自定义字体对象
    # font = {'family': 'Times New Roman'}

    # 创建一个新的图表并设置大小
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.plot(x, y, color='black', linewidth=1, marker='o', markersize=4)

    # 设置X轴尺度范围
    # TODO: 设置X轴尺度范围
    x_max = max(map(float, x))
    x_min = min(map(float, x))

    # x_median = statistics.median(map(float, x))
    # x_lim = [0, round((x_median + (x_median * 3)) / 5) * 5]
    x_lim = [round(x_min - 2), round(x_max + 2)]
    ax.set_xlim(x_lim)
    ax.set_ylim([0, 12])

    # 设置网格线
    plt.grid(True, alpha=0.3)

    # # 设置纵线和横线的格式
    # plt.gca().xaxis.grid(alpha=0.2)
    # plt.gca().yaxis.grid(alpha=0.2)

    # 在Y轴上绘制平均刻度和小刻度
    ax = plt.gca()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    # ax.tick_params(axis='y', direction='in', which='minor')

    # 自定义X轴和Y轴标签
    ax.set_title('Pressure profile')
    ax.set_xlabel('Pressure in mbar')
    ax.set_ylabel('Height in m')

    # 保存图表为PNG文件
    plt.tight_layout()
    plt.show()
    fig.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Pressure profile 2")), dpi=400)


# draw hisogram of feed rate
def feed_rate_histo_plot(df, Export_Path, id):
    plt.figure(figsize=(10, 6))
    # plt.hist(df['Sorbent mass flow_2 kg/h'][180:-180], density = 1, bins=50, color='blue', alpha=0.7, edgecolor='black')
    sns.histplot(df['Sorbent mass flow_2 kg/h'][180:-180], kde=True, stat='probability',  bins=50,
                 color='blue', alpha=0.7, edgecolor='black', label='ws')
    plt.title('Mass flow  histogram')
    plt.xlabel('Sorbent mass flow in kg/h')
    plt.ylabel('Percentage')
    plt.savefig("{}.png".format(os.path.join(Export_Path, f"{id} Feed rate histogram")), dpi=400)
    plt.show()

def feed_rate_histo_plot_2(df, Export_Path, id):
    pass


# 读取压力数据并绘制图表：前三分钟每个传感器的平均值,后三分钟每个传感器的平均值，不包含Pg208, Pg221
def read_pressure_and_plot_3(df, Export_Path, id):
    # 循环遍历每一行数据
    df = df.drop('Zeit', axis=1)

    height = [0.195, 1.900, 4.790, 6.405, 8.200, 9.963, 10.990]

    # 指定新的列顺序
    new_columns = ['Pg201 mbar', 'Pg203 mbar', 'Pg204 mbar', 'Pg234 mbar', 'Pg205 mbar',
                   'Pg206 mbar', 'Pg207 mbar']

    df = df[new_columns]

    # 计算每个sensor的平均值
    column_mean = df.mean(axis=0)
    selected_data_begin = df[:180]
    selected_data_end = df[180:]

    # 计算每个sensor的平均值
    average_values_begin = selected_data_begin.mean(axis=0)
    average_values_end = selected_data_end.mean(axis=0)

    df_column_mean = pd.DataFrame()
    df_column_mean['Mean pressure '] = column_mean.to_frame()
    df_column_mean['Mean pressure in first 3 mins'] = average_values_begin.to_frame()
    df_column_mean['Mean pressure in last 3 mins'] = average_values_end.to_frame()

    df_column_mean['height in m'] = height

    x1 = df_column_mean['Mean pressure in first 3 mins']
    x2 = df_column_mean['Mean pressure in last 3 mins']
    x3 = df_column_mean['Mean pressure ']

    y = df_column_mean['height in m']

    # # 创建一个自定义字体对象
    font = {'family': 'Times New Roman'}

    # 创建一个新的图表并设置大小
    fig, ax = plt.subplots(figsize=(8, 16))
    ax.plot(x1, y, color='black', linewidth=1, marker='o', markersize=6, label='Mean pressure in first 3 mins')
    ax.plot(x3, y, color='green', linewidth=1, marker='o', markersize=6, label='Mean pressure')
    ax.plot(x2, y, color='red', linewidth=1, marker='o', markersize=6, label='Mean pressure in last 3 mins')

    # 设置X轴尺度范围
    plt.xlim(-15, 15)
    plt.ylim(0, 12)

    # 设置网格线
    plt.grid(True)

    # 设置纵线和横线的格式
    plt.gca().xaxis.grid(alpha=0.2)
    plt.gca().yaxis.grid(alpha=1)

    # 在Y轴上绘制平均刻度和小刻度
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    ax.tick_params(axis='y', direction='in', which='minor')

    # 自定义X轴和Y轴标签
    ax.set_title('Pressure profile', fontweight='bold', size=24, fontdict=font)
    ax.set_xlabel('Relative Pressure in mbar', fontweight='bold', size=20, fontdict=font)
    ax.set_ylabel('Height in m', fontweight='bold', size=20, fontdict=font)
    plt.legend()


# 读取压力数据并绘制图表：前三分钟每个传感器的平均值,后三分钟每个传感器的平均值，包含Pg208, Pg221
def read_pressure_and_plot_4(file_name):
    #     file_path = file_name + '.csv'
    df = pd.read_csv(file_name)

    # 循环遍历每一行数据
    df = df.drop('Zeit', axis=1)

    height = [0.195, 1.900, 4.790, 6.405, 8.200, 9.963, 10.990, 10.990, 10.990]

    # 指定新的列顺序
    new_columns = ['Pg201 mbar', 'Pg203 mbar', 'Pg204 mbar', 'Pg234 mbar', 'Pg205 mbar',
                   'Pg206 mbar', 'Pg207 mbar', 'Pg208 mbar', 'Pg221 mbar']

    df = df[new_columns]

    # 计算每个sensor的平均值
    column_mean = df.mean(axis=0)
    selected_data_begin = df[:180]
    selected_data_end = df[180:]

    # 计算每个sensor的平均值
    average_values_begin = selected_data_begin.mean(axis=0)
    average_values_end = selected_data_end.mean(axis=0)

    df_column_mean = pd.DataFrame()
    df_column_mean['Mean pressure '] = column_mean.to_frame()
    df_column_mean['Mean pressure in first 3 mins'] = average_values_begin.to_frame()
    df_column_mean['Mean pressure in last 3 mins'] = average_values_end.to_frame()

    df_column_mean['height in m'] = height

    x1 = df_column_mean['Mean pressure in first 3 mins']
    x2 = df_column_mean['Mean pressure in last 3 mins']
    x3 = df_column_mean['Mean pressure ']

    y = df_column_mean['height in m']

    # # 创建一个自定义字体对象
    font = {'family': 'Times New Roman'}

    # 创建一个新的图表并设置大小
    fig, ax = plt.subplots(figsize=(8, 16))
    ax.plot(x1, y, color='black', linewidth=1, marker='o', markersize=6, label='Mean pressure in first 3 mins')
    ax.plot(x3, y, color='green', linewidth=1, marker='o', markersize=6, label='Mean pressure')
    ax.plot(x2, y, color='red', linewidth=1, marker='o', markersize=6, label='Mean pressure in last 3 mins')

    #
    # 设置X轴尺度范围
    plt.xlim(-15, 100)
    plt.ylim(0, 12)

    # 设置网格线
    plt.grid(True)

    # 设置纵线和横线的格式
    plt.gca().xaxis.grid(alpha=0.2)
    plt.gca().yaxis.grid(alpha=1)

    # 在Y轴上绘制平均刻度和小刻度
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    ax.tick_params(axis='y', direction='in', which='minor')

    # 自定义X轴和Y轴标签
    ax.set_title('Pressure profile', fontweight='bold', size=24, fontdict=font)
    ax.set_xlabel('Relative Pressure in mbar', fontweight='bold', size=20, fontdict=font)
    ax.set_ylabel('Height in m', fontweight='bold', size=20, fontdict=font)
    plt.legend()
    # 保存图表为PNG文件
    plt.savefig(file_name + '4 .png')
