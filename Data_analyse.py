import os
import pdb
import re

import numpy as np
import pandas as pd
import scipy.signal as sig

from Data_Import import define_off_set_time
from Fig_Plot import find_offset_time_plot


def find_offset_time(df, index_1, index_2, plot_output_path, id):

    while True:
        choice = input(f'Do you want to find the offset time of {id}? (Y/N)')
        if choice == 'Y':

            offset_time, df_Gasout_2, time_start_dosing, time_end_dosing, dosing_duration = define_off_set_time(
                df,
                index_1,
                index_2)

            find_offset_time_plot(df_Gasout_2, time_start_dosing, time_end_dosing, offset_time, plot_output_path,
                                  id)

        elif choice == 'N':
            print(f'you have already find the offset time {offset_time}')
            break
        else:
            print("Invalid choice. Please enter 'Y' or 'N'.")

        df_Result = pd.DataFrame()
        df_Result['offset time'] = [offset_time]
        df_Result['time start dosing'] = [str(time_start_dosing).split()[1]]
        df_Result['time end dosing'] = [str(time_end_dosing).split()[1]]
        df_Result['dosing duration'] = [dosing_duration]

    return df_Gasout_2, offset_time, df_Result


def T_P_calc(df_1,df_2, df_Result):

    df_P = df_1.drop('Zeit', axis=1)
    P_mean = df_P.mean()
    P_max = P_mean.max()
    P_min_1 = P_mean.min()
    P_mean_2 = P_mean[:-2]
    P_min_2 = P_mean_2.min()

    df_2 = df_2.drop('Zeit', axis=1)
    T_mean = df_2.mean()
    T_mean_mean = T_mean.mean()
    T_max = T_mean.max()
    T_min = T_mean.min()

    df_Result['P_max'] = P_max
    df_Result['P_min_1'] = P_min_1
    df_Result['P_min_2'] = P_min_2
    df_Result['T_mean_mean'] = T_mean_mean
    df_Result['T_max'] = T_max
    df_Result['T_min'] = T_min

    return df_Result


# df_1: df_Sorbent, df_2: df_Gasout_2, df_3: df_Gasin
def conversion_calc_1(df_1, df_2, df_3, df_Result):

    df_1['Waage_abs_kg'] = df_1['Waage_abs g'] / 1000

    # df_1['Waage_abs_kg_movingAVG'] = df_1["Waage_abs_kg"].rolling(window=60).mean()
    #尝试不同的window
    df_1['Waage_abs_fil'] = sig.savgol_filter(df_1["Waage_abs_kg"], 100, 2)  # kg
    # 提取平滑后的数据，并保存在新的dataframe中
    df_1['mass_change_per_second'] = -df_1['Waage_abs_kg'].diff()
    df_1['mass_change_per_hour'] = df_1['mass_change_per_second'] * 3600
    df_1['mass_change_per_hour'] = df_1['mass_change_per_hour'].fillna(-999)

    df_1['Sorbent mass flow_1 kg/h'] = sig.savgol_filter(df_1['mass_change_per_hour'], 100, 2)

    df_1['Sorbent mass flow_2 kg/h'] = sig.savgol_filter(df_1['Sorbent mass flow_1 kg/h'], 100, 2)

    df_1 = df_1[120: -120]
    df_1 = df_1.reset_index(drop=True)

    sorbent_mass_flow_mean = df_1['Sorbent mass flow_2 kg/h'][180:-180].mean()  # kg/h

    # 计算相对于第一个时间戳的时间间隔
    df_1['TimeDelta'] = df_1['Zeit'] - df_1['Zeit'].iloc[0]
    # 将时间间隔转换为分钟，并以 "hh:mm" 的格式表示
    df_1['Time'] = df_1['TimeDelta'].dt.total_seconds().astype(int)
    df_1['Time'] = df_1['Time'].apply(lambda x: f"{x // 3600:02d}:{(x % 3600) // 60:02d}:{x % 60:02d}")
    df_1['Time'] = pd.to_datetime(df_1['Time'], format='%H:%M:%S')

    # 首先合并 df_1 和 df_2
    df_merged_1 = pd.merge(df_1, df_2, on='Zeit', how='inner')
    # 然后再与 df_3 合并
    df_plot_1 = pd.merge(df_merged_1, df_3, on='Zeit', how='inner')

    filename = f'histogram_data.xlsx'
    export_path = "/Users/xiaoyanyu/Desktop/Data /Summary/Data_Summary"
    export_path = os.path.join(export_path, filename)
    df_plot_1.to_excel(export_path, index=True, header=False)



    Dosierer_Prozent_mean = df_plot_1['Dosierer Prozent %'][180:-180].mean()
    df_Result['Dosing speed %'] = [Dosierer_Prozent_mean]
    df_Result['Sorbent mass flow mean 1 kg/h'] = [sorbent_mass_flow_mean] # kg/h 基于平滑后的数据 dosing时的平均质量变化率

    return df_plot_1, df_Result


# df: df_plot_1
def conversion_calc_2(df_1, df_Result):
    MM_Ca_OH_2 = 74.10  # g/mol
    CO2_soll = df_1['Durchfluess CO2_1 F203_Nm3h'][:180].mean()  # Nm3/h
    CO2_soll_mole = CO2_soll / 22.41  # kmol/h
    total_flow_input = CO2_soll / (df_1['Abgas CO2 Vol %'][:180].mean() / 100)  # Nm3/h
    total_N2_flow = total_flow_input - CO2_soll  # Nm3/h
    N_CO2_input = df_1['Durchfluess CO2_1 F203_Nm3h'][180:-180].sum() / 3600 / 22.41  # kmol
    # N_CO2_input_2 = CO2_soll_mole * (df_1['Zeit'].iloc[-181] - df_1['Zeit'].iloc[180]).total_seconds() / 3600  # kmol

    # TOdO:
    df_1['total flow out'] = total_N2_flow / (1 - df_1['Abgas CO2 Vol %'] / 100)
    df_1['CO2 removal Nm3/h'] = total_flow_input - df_1['total flow out']
    F_CO2_i = df_1['total flow out'] - total_N2_flow
    df_1['E_CO2'] = 1 - F_CO2_i / CO2_soll

    # TODO:check if index is correct
    Sum_sorbent = (df_1['Waage_abs_fil'][: 180].mean() -
                   df_1['Waage_abs_fil'][-180:].mean())  # kg sorbent
    sorbent_begin = df_1['Waage_abs_fil'][:180].mean()
    sorbent_end = df_1['Waage_abs_fil'][-180:].mean()
    Sorbent_mass_flow_mean_2 = Sum_sorbent / (df_1['Zeit'].iloc[-181] - df_1['Zeit'].iloc[180]).total_seconds() * 3600

    # sample 1 available Ca(OH)2 93.43 wt.%，计算投入的Ca(OH)2的kmol数
    N_Ca = Sum_sorbent * 0.9343 / MM_Ca_OH_2  # total input Ca(OH)2 kmol
    N_CO2_captured = df_1['CO2 removal Nm3/h'][
                     180:-180].sum() / 3600 / 22.41  # kmol
    E_CO2_mean = df_1['E_CO2'][180:-180].mean()
    Xcarb = N_CO2_captured / N_Ca  # kmol CO2/kmol Ca
    Ca_CO2_ratio = N_Ca / N_CO2_input
    # Cs_CO2_ratio_2 = N_Ca / N_CO2_input_2

    df_plot_2 = df_1

    df_Result['Total Sorbent input mass kg'] = [Sum_sorbent]
    df_Result['Sorbent input begin mass kg'] = [sorbent_begin]
    df_Result['Sorbent input end mass kg'] = [sorbent_end]
    df_Result['Sorbent feed rate mean 2 kg/h'] = [Sorbent_mass_flow_mean_2]
    df_Result['Total input gas flow Nm3/h'] = [total_flow_input]
    df_Result['CO2 flow in Nm3/h'] = [CO2_soll]
    df_Result['Total N2 flow in Nm3/h'] = [total_N2_flow]
    df_Result['Total CO2 input kmol'] = [N_CO2_input]
    df_Result['Total input Ca(OH)2 kmol'] = [N_Ca]
    df_Result['CO2 captured kmol'] = [N_CO2_captured]
    df_Result['E_carb mean '] = [E_CO2_mean]
    df_Result['Xcarb'] = [Xcarb]
    df_Result['Ca_CO2_ratio'] = [Ca_CO2_ratio]


    return df_plot_2, Xcarb, df_Result


def data_summary(sorbent,id,date, export_path,df_Result):

    df_Result['Sorbent name'] = [sorbent]
    df_Result['vp'] = [id]
    df_Result['Date'] = [date]

    x= df_Result['offset time'][0]

    df_Result_export = df_Result.T

    filename = f'{id}_{x}.xlsx'
    export_path = os.path.join(export_path, filename)
    df_Result_export.to_excel(export_path, index=True, header=False)


    # Result_collection = [
    #     {"name": "Experiment id", "value": id, "unit": "--"},
    #     {"name": "Date", "value": date, "unit": " "},
    #     {"name": "Gas superficial velocity ", "value": id, "unit": "m/s"},
    #     {"name": "Solid mass flow", "value": id, "unit": "kg/h"},
    #     {"name": "Target Temperature  ", "value": id, "unit": "℃"},
    #     {"name": "Average Temperature ", "value": id, "unit": "℃"},
    #     {"name": "Time range of experiment ", "value": id, "unit": "hh:mm:ss"},
    #     {"name": "Duration of experiment ", "value": id, "unit": " hh:mm:ss"},
    #     {"name": "Time range of dosing ", "value": id, "unit": "hh:mm:ss"},
    #     {"name": "Duration of dosing ", "value": id, "unit": "hh:mm:ss"},
    #     {"name": "Offset time", "value": id, "unit": "s"},
    #     {"name": "Average dosing speed", "value": id, "unit": "%"},
    #     {"name": "Total Sorbent input mass 1", "value": id, "unit": "kg"},
    #     {"name": "Total Sorbent input mass 2", "value": id, "unit": "kg"},
    #     {"name": "Total Ca(OH)2 input mole ", "value": id, "unit": "kmol"},
    #     {"name": "Total Ca(OH)2 input mass", "value": id, "unit": "kg"},
    #     {"name": "Total CO2 input mole", "value": id, "unit": "kmol"},
    #     {"name": "Total CO2 input mass", "value": id, "unit": "kg"},
    #     {"name": "Total CO2 captured mole", "value": id, "unit": "kmol"},
    #     {"name": "Total CO2 captured mass", "value": id, "unit": "kg"},
    #     {"name": "CO2 capture efficiency", "value": id, "unit": "%"},
    #     {"name": "Ca conversion", "value": id, "unit": "%"},
    #
    # ]


def conversion_calc(file_name, offset_time, start_dosierer_index, end_dosierer_index, filtered_data, temp_column,
                    Abgas_o2_column, delta_time):
    # Molar mass
    MM_Ca_OH_2 = 74.10  # g/mol
    MM_CO2 = 44.01  # g/mol

    pattern = r'(\d{4}-\d{2}-\d{2})'
    match = re.search(pattern, file_name)
    date = match.group(1)

    Date = date

    Time = str(filtered_data["Time"][filtered_data.index[0]])[11:]

    Avg_Temp = temp_column.iloc[start_dosierer_index:end_dosierer_index + 1].mean().mean()
    start_index = start_dosierer_index - 180  # 3 mins before dosing start
    end_index = end_dosierer_index + 180  # 3 mins after dosing end
    Time_range = str(filtered_data["Time"][start_index])[11:] + "-" + str(filtered_data["Time"][end_index])[11:]

    # O2 correction(considering false gas input)
    # O2 data meassured in MGS-B ,3 min mean value before
    o2_ref = Abgas_o2_column[start_index: start_dosierer_index].mean()

    # 将abgas co2 , abgas o2 的数据，根据offset time 进行平移
    filtered_data['Abgas CO2 Vol shift'] = filtered_data['Abgas CO2 Vol'].shift(-offset_time)
    filtered_data['Abgas O2 Vol real'] = filtered_data['Abgas O2 Vol'].shift(-offset_time)

    # 填充Nan值
    # TODO: 为什么要填充Nan值
    filtered_data['Abgas CO2 Vol shift'].fillna(method='ffill', inplace=True)
    filtered_data['Abgas O2 Vol real'].fillna(method='ffill', inplace=True)

    # O2 correction(considering false gas input)
    filtered_data['Dilution_Factor'] = (20.95 - o2_ref) / (
            20.95 - filtered_data['Abgas O2 Vol real'])  # 20.95% is the O2 concentration in
    filtered_data['corrected_CO2'] = filtered_data['Dilution_Factor'] * filtered_data['Abgas CO2 Vol shift']

    # 前三分钟的平均稳态CO2input
    CO2_soll_2 = filtered_data["Durchfluess MFC Dosierer F211_Nm3h"][start_index:start_dosierer_index].mean()  # Nm3/h
    CO2_soll_2_mole = CO2_soll_2 / 22.41  # kmol/h

    # print(f'CO2_soll_2: {CO2_soll_2}')
    total_flow_input = CO2_soll_2 / (filtered_data['corrected_CO2'][start_index:start_dosierer_index].mean() / 100)
    # print(f'total_flow_input is {total_flow_input}')
    total_N2_flow = total_flow_input - CO2_soll_2  # Nm3/h
    # print(f'total_N2_flow is {total_N2_flow}' )
    filtered_data['total flow out'] = total_N2_flow / (1 - filtered_data['corrected_CO2'] / 100)
    # print(f'Total flow out flow is {filtered_data["total flow out"]}')
    filtered_data['CO2 out flow'] = filtered_data['total flow out'] - total_N2_flow
    filtered_data['CO2 removal Nm3/h'] = (CO2_soll_2 - filtered_data['CO2 out flow'])
    pdb.set_trace()

    print(f'CO2 removal kmol/h is {filtered_data["CO2 removal kmol/h"][start_dosierer_index:end_dosierer_index + 1]}')
    filtered_data['Eco2_2'] = 1 - filtered_data['CO2 out flow'] / CO2_soll_2
    Eco2_2_mean = filtered_data['Eco2_2'][start_dosierer_index: end_dosierer_index + 1].mean()

    # TODO: why end_dosierer_index+1, the results are uncorrect
    # Avg_Dosingspeed = filtered_data['Dosierer Prozent %'][start_dosierer_index: end_dosierer_index+1].mean()
    Avg_Dosingspeed = filtered_data['Dosierer Prozent %'][start_dosierer_index: end_dosierer_index].mean()
    # initial 3mins and last 3mins mean values subtract,通过计算稳定状态下的质量变化量，计算出吸附剂的质量
    # TODO: check 是否这种方式计算Sorbent input mass是正确的?
    Sum_sorbent = (filtered_data['Waage_abs g'][start_dosierer_index - 180: start_dosierer_index].mean() -
                   filtered_data['Waage_abs g'][
                   end_dosierer_index + 1:end_dosierer_index + 181].mean()) / 1000  # kg sorbent

    # #sample 1 available Ca(OH)2 93.43 wt.%，计算投入的Ca(OH)2的kmol数
    N_Ca = Sum_sorbent * 0.9343 / MM_Ca_OH_2  # total input Ca(OH)2 kmol

    # Avg_N_Ca = N_Ca/(end_dosierer_index - start_dosierer_index + 1) *3600 # kmol/h
    # print(f'Avg_N_Ca is {Avg_N_Ca}')
    N_CO2_captured = filtered_data['CO2 removal kmol/h'][
                     start_dosierer_index:end_dosierer_index + 1].sum() / 3600  # kmol

    Xcarb = N_CO2_captured / N_Ca  # kmol CO2/kmol Ca

    # sorbent input per unit time.
    Avg_sorbent_input = 3600 * Sum_sorbent / delta_time  # kg/h
    Sum_m_CO2_captured = filtered_data['CO2 removal kmol/h'][
                         start_dosierer_index:end_dosierer_index + 1].sum() / 3600 * 1 * 44.01  # kg total CO2 kg captured
    # Total amount of CO2 captured
    Sum_N_CO2_captured = filtered_data['CO2 removal kmol/h'][
                         start_dosierer_index:end_dosierer_index + 1].sum() / 3600  # kmol total CO2 Kmol captured
    Sum_m_CO2_input = filtered_data['CO2 input mole flow'][
                      start_dosierer_index:end_dosierer_index + 1].sum() / 3600 * 44.01  # kg total CO2 kg input
    M_CO2_input = filtered_data['CO2 input mole flow'][
                  start_dosierer_index:end_dosierer_index + 1].sum() / 3600  # kmol total CO2 Kmol input

    Xcarb = Sum_N_CO2_captured / N_Ca  # kmol CO2/kmol Ca

    # 25-75% range of the time frame between Start_index and End_index, then make average.
    High_index_Start = int(round(start_dosierer_index + 0.25 * delta_time))
    High_index_End = int(round(start_dosierer_index + 0.75 * delta_time))

    High_delta_time = High_index_End - High_index_Start + 1

    High_Time_range = str(filtered_data["Time"][High_index_Start])[11:] + "-" + str(
        filtered_data["Time"][High_index_End])[11:]

    Sum_m_CO2_high = filtered_data["CO2 removal kmol/h"][
                     High_index_Start:High_index_End + 1].sum() / 3600 * 44.01  # kg total CO2 kg

    M_CO2_high = filtered_data["CO2 removal kmol/h"][High_index_Start:High_index_End + 1].sum() / 3600  # kmol

    High_E_co2 = filtered_data["CO2 removal kmol/h"][High_index_Start:High_index_End].sum() / \
                 filtered_data["CO2 input mole flow"][High_index_Start:High_index_End + 1].sum() * 100

    filtered_data['Eco2_i_high'] = filtered_data["CO2 removal kmol/h"][High_index_Start:High_index_End + 1] / \
                                   filtered_data["CO2 input mole flow"][High_index_Start:High_index_End + 1]

    High_E_co2_i_mean = filtered_data['Eco2_i_high'][High_index_Start:High_index_End + 1].mean() * 100
    filtered_data["Waage_abs_fil"] = sig.savgol_filter(filtered_data["Waage_abs g"], 200, 2)  # in g
    filtered_data["Waage_abs_fil"] = filtered_data["Waage_abs g"]
    Sum_Sorbent_High = (filtered_data["Waage_abs_fil"][High_index_Start - High_delta_time] -
                        filtered_data["Waage_abs_fil"][High_index_End - High_delta_time]) / 1000  # in kg
    M_Ca_High = Sum_Sorbent_High * 0.9343 / MM_Ca_OH_2  # kmol
    Avg_sorbent_input_High = Sum_Sorbent_High / (High_index_End - High_index_Start) * 3600
    Xcarb_High = M_CO2_high / M_Ca_High  # kmol/kmol
    Sorbent_input_per_CO2_High = Sum_Sorbent_High / Sum_m_CO2_high * 100  # kg/kg %
    df_plot = filtered_data

    Result_collection = [

        {"name": "Date", "value": Date, "unit": "yyyy-mm-dd"},
        {"name": "Time", "value": Time, "unit": "hh:mm:ss"},
        {"name": "Dosing_Duration", "value": delta_time, "unit": "s"},
        {"name": "Time range I", "value": Time_range, "unit": "-"},
        {"name": "Time range II", "value": High_Time_range, "unit": "-"},
        {"name": "Duration Max", "value": High_delta_time, "unit": "s"},
        {"name": "Offset time", "value": offset_time, "unit": "s"},
        {"name": "Average Temperature", "value": round(Avg_Temp, 2), "unit": "degree Celcius"},
        {"name": "Average Dosing speed", "value": round(Avg_Dosingspeed, 2), "unit": "%"},
        {"name": "Total Sorbent input mass I", "value": round(Sum_sorbent, 2), "unit": "kg"},
        {"name": "Average Sorbent input I", "value": round(Avg_sorbent_input, 2), "unit": "kg/h"},
        {"name": "Total Ca(OH)2 input mole I", "value": round(N_Ca, 4), "unit": "kmol"},
        {"name": "Total CO2 input mass I", "value": round(Sum_m_CO2_input, 2), "unit": "kg CO2"},
        {"name": "Total CO2 input mole I", "value": round(M_CO2_input, 4), "unit": "kmol"},
        {"name": "Total CO2 removal mole I", "value": round(Sum_N_CO2_captured, 4), "unit": "kmol"},
        # {"name": "CO2 capture efficiency I ", "value": round(Eco2, 2), "unit": "%"},
        {"name": "CO2 capture efficiency I (mean)", "value": round(Eco2_2_mean, 2), "unit": "%"},
        {"name": "Ca conversion I Xcarb", "value": round(Xcarb, 4), "unit": "kmol CO2/kmol Ca %"},
        # {"name": "Sorbent input % I", "value": round(Sorbent_input_per_CO2, 2), "unit": "%"},
        {"name": "Total Sorbent input mass II", "value": round(Sum_Sorbent_High, 2), "unit": "kg"},
        {"name": "Average Sorbent input II", "value": round(Avg_sorbent_input_High, 2), "unit": "kg/h"},
        {"name": "Total Ca(OH)2 input mole II", "value": round(M_Ca_High, 4), "unit": "kmol"},
        {"name": "Total CO2 removal mass II", "value": round(Sum_m_CO2_high, 2), "unit": "kg CO2"},
        {"name": "Total CO2 removal mole II", "value": round(M_CO2_high, 4), "unit": "kmol"},
        {"name": "CO2 capture efficiency II", "value": round(High_E_co2, 2), "unit": "%"},
        {"name": "CO2 capture efficiency II (mean)", "value": round(High_E_co2_i_mean, 2), "unit": "%"},
        {"name": "Ca conversion II Xcarb", "value": round(Xcarb_High, 4), "unit": "kmol CO2/kmol Ca %"},
        {"name": "Sorbent input % II", "value": round(Sorbent_input_per_CO2_High, 2), "unit": "%"}

    ]

    df_Result = pd.DataFrame(Result_collection)

    return df_Result, df_plot
