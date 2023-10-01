import os
import re
import pandas as pd


def get_data(folder_path):
    # 创建保存预处理结果的文件夹
    Proccessed_path = os.path.join(folder_path, 'proccessed_data')

    if not os.path.exists(Proccessed_path):
        os.mkdir(Proccessed_path)

    # 获取文件夹中的所有子文件夹
    xls_files = [f.path for f in os.scandir(folder_path) if f.is_file() and f.name.endswith('.xls')]

    for xls_file in xls_files:
        # 读取 XLS 文件为 DataFrame
        df = pd.read_excel(xls_file, engine='xlrd')

        # 对 DataFrame 执行处理操作
        column_indexes_to_keep = [1, 2, 4, 8, 27, 30, 34, 35, 36, 37, 38, 39, 40, 42, 46, 81, 93, 107, 173, 50, 51, 52,
                                  54, 56, 58, 59, 61, 63, 64]
        df_filtered = df.iloc[:, column_indexes_to_keep]

        column_mapping = {
            'Unnamed: 1': 'Zeit',
            'Durchfluesse': 'Fluidisierung F201_Nm3h',
            'Durchfluesse.2': 'Durchfluess CO2_1 F203_Nm3h',
            'Durchfluesse.6': 'Durchfluess MFC Dosierer F211_Nm3h',
            'Abgas.17': 'Abgas CO2 Vol',
            'Abgas.20': 'Abgas O2 Vol',
            'Druck': 'Pg201 mbar',
            'Druck.1': 'Pg202 mbar',
            'Druck.2': 'Pg203 mbar',
            'Druck.3': 'Pg204 mbar',
            'Druck.4': 'Pg205 mbar',
            'Druck.5': 'Pg206 mbar',
            'Druck.6': 'Pg207 mbar',
            'Druck.16': 'Pg233 mbar',
            'Druck.17': 'Pg234 mbar',
            'Druck.8': 'Pg208 mbar',
            'Druck.12': 'Pg221 mbar',
            'Temperatur': 'T201 RI',
            'Temperatur.1': 'T202 RI',
            'Temperatur.2': 'T204 RI',
            'Temperatur.4': 'T207 RI',
            'Temperatur.6': 'T209 RI',
            'Temperatur.8': 'T211 RI',
            'Temperatur.9': 'T212 RI',
            'Temperatur.11': 'T214 RI',
            'Temperatur.13': 'T216 RI',
            'Temperatur.14': 'T217 RI',
            'Sonstige': 'Waage_abs g',
            'Sollwerte.25': 'Dosierer Prozent %'
        }

        df_filtered = df_filtered.rename(columns=column_mapping)
        df_filtered = df_filtered.drop([0, 1]).reset_index(drop=True)

        # 构建保存预处理结果的文件路径
        filename_without_extension = os.path.splitext(os.path.basename(xls_file))[0]  # 获取文件名（不含扩展名）

        # 提取日期时间部分
        date_time_pattern = r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
        match = re.search(date_time_pattern, filename_without_extension)

        date_time_part = match.group()

        # 对处理后的xlsx文件处理
        split_data = []
        start_index = None

        for index, row in df_filtered.iterrows():

            value = row['Dosierer Prozent %']  # 假设第三列的列名为 'Dosierer Prozent'
            # 当前值从零开始变为大于零的数据，开始记录筛选数据
            if value > 0 and start_index is None:
                start_index = index
                start_dosierer_index = start_index

            # 当前值重新归零，且已经找到起始数据
            if value == 0 and start_index is not None:
                end_index = index
                end_dosierer_index = end_index

                split_data.append(df_filtered.iloc[start_index - 300:end_index + 300, :])

                # 将筛选数据,并且向前向后扩展5min
                start_index = None
                # 重置起始索引

        # 保存 split_data 中的数据为多个 CSV 文件
        for i, data_chunk in enumerate(split_data):
            csv_filename = f'{date_time_part}_{i + 1}.csv'
            csv_path = os.path.join(Proccessed_path, csv_filename)
            data_chunk.to_csv(csv_path, index=False)


# 读取数据，得到df_Temp，df_Pressure，df_Gasout,df_Gasin,df_Sorbent
def pretreat_data(csv_file_name):
    df = pd.read_csv(csv_file_name)
    df['Zeit'] = pd.to_datetime(df['Zeit'], format='%H:%M:%S')

    # start_dosierer_index, end_dosierer_index
    start_dosing_index = df.index[df['Dosierer Prozent %'] > 0][0]
    end_dosing_index = df.index[(df.index > start_dosing_index) & (df['Dosierer Prozent %'] == 0)][0] - 1

    df_Dosierer = df[['Zeit', 'Dosierer Prozent %']][start_dosing_index - 180:end_dosing_index + 181]

    # Temperature, Pressure, Gasout, Gasin, Doser data separate in each dataframe
    df_Temp = df[['Zeit', 'T201 RI', 'T202 RI', 'T204 RI', 'T207 RI', 'T209 RI', 'T211 RI',
                  'T212 RI', 'T214 RI', 'T216 RI', 'T217 RI']][start_dosing_index:end_dosing_index + 1]

    df_Pressure = df[['Zeit', 'Pg201 mbar', 'Pg202 mbar', 'Pg203 mbar', 'Pg233 mbar', 'Pg204 mbar', 'Pg234 mbar',
                      'Pg205 mbar', 'Pg206 mbar', 'Pg207 mbar', 'Pg208 mbar', 'Pg221 mbar']][
                  start_dosing_index:end_dosing_index + 1]

    df_Gasout = df[['Zeit', 'Abgas CO2 Vol', 'Abgas O2 Vol']]

    df_Sorbent = df[['Zeit', 'Waage_abs g', 'Dosierer Prozent %']]

    df_Gasin = df[
        ['Zeit', 'Fluidisierung F201_Nm3h', 'Durchfluess CO2_1 F203_Nm3h', 'Durchfluess MFC Dosierer F211_Nm3h']]

    return df_Gasin, df_Gasout, df_Pressure, df_Temp, df_Sorbent, df_Dosierer, start_dosing_index, end_dosing_index


def find_off_set_time_95(df_Gasout, start_dosing_index):
    # 95% of inital CO2 conc. is set as Starting point, save index of it.
    Start_index = df_Gasout.index[df_Gasout['Abgas CO2 Vol'] <= (0.95 * df_Gasout['Abgas CO2 Vol'][:180].mean())][0]
    offset_time = Start_index - start_dosing_index + 1

    return offset_time


def define_off_set_time(df, index_1, index_2):
    global offset_time, df_Gasout_2
    # 方法一自己定义单位时间s
    while True:
        test_offset_time = input('Please input the offset time: ')

        if test_offset_time.isdigit():
            offset_time = int(test_offset_time)
            break
        else:
            print('Invalid input. Please enter a valid numeric offset time.')

    # 方法二：定义95的吸收为起始点，当要使用这个方法时可uncoment下面的代码
    # offset_time = find_off_set_time_95(df, index_1)

    df_2 = pd.DataFrame()
    df_2['Abgas CO2 Vol %'] = df['Abgas CO2 Vol'].shift(-offset_time)
    df_2['Abgas O2 Vol %'] = df['Abgas O2 Vol'].shift(-offset_time)
    df_2['Zeit'] = df['Zeit']

    df_2 = df_2[index_1 - 180: index_2 + 181]
    df_2 = df_2.reset_index(drop=True)

    time_start_dosing = df_2['Zeit'].iloc[180]
    time_end_dosing = df_2['Zeit'].iloc[-181]
    timedelta = time_end_dosing - time_start_dosing
    total_seconds = timedelta.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    dosing_duration = f'00:{minutes:.0f}:{seconds:.0f}'

    # 此时选取新的df_2进行计算，index从0开始，此时index_1 = 301, index_2 = 301 + (index_2 - index_1)
    # O2 correction(considering false gas input),O2 data meassured in MGS-B ,3 min mean value before
    o2_ref = df_2['Abgas O2 Vol %'][: 180].mean()
    Dilution_Factor = (20.95 - o2_ref) / (20.95 - df_2['Abgas O2 Vol %'])  # 20.95% is the O2 concentration in air
    df_2['corrected CO2 Vol %'] = Dilution_Factor * df_2['Abgas CO2 Vol %']

    df_Gasout_2 = pd.DataFrame()
    df_Gasout_2['Abgas CO2 Vol %'] = df_2['corrected CO2 Vol %']
    df_Gasout_2['Zeit'] = df_2['Zeit']
    df_Gasout_2 = df_Gasout_2.reset_index(drop=True)

    df_Gasout_2['TimeDelta'] = df_Gasout_2['Zeit'] - df_Gasout_2['Zeit'].iloc[0]

    # 将时间间隔转换为分钟，并以 "hh:mm" 的格式表示
    df_Gasout_2['Time_start_from_Zero'] = df_Gasout_2['TimeDelta'].dt.total_seconds().astype(int)
    df_Gasout_2['Time_start_from_Zero'] = df_Gasout_2['Time_start_from_Zero'].apply(
        lambda x: f"{x // 3600:02d}:{(x % 3600) // 60:02d}:{x % 60:02d}")
    df_Gasout_2['Time_start_from_Zero'] = pd.to_datetime(df_Gasout_2['Time_start_from_Zero'], format='%H:%M:%S')

    # 找到异常值并用后一个值填充
    mask = df_Gasout_2['Abgas CO2 Vol %'] == 0  # 创建一个布尔掩码，标记异常值
    df_Gasout_2['Abgas CO2 Vol %'] = df_Gasout_2['Abgas CO2 Vol %'].mask(mask).fillna(method='bfill')

    return offset_time, df_Gasout_2, time_start_dosing, time_end_dosing, dosing_duration
