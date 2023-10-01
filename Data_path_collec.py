# experiment_config.py

# 实验数据路径字典
experiment_data_paths = {
    "20230511": "/Users/xiaoyanyu/Desktop/Data /20230511",
    "20230525": "/Users/xiaoyanyu/Desktop/Data /20230525",
    "20230605": "/Users/xiaoyanyu/Desktop/Data /20230605",
    "20230808": "/Users/xiaoyanyu/Desktop/Data /20230808"
    # 添加更多日期和路径
}

# 经处理后的数据保存路径
summary_data_path = "/Users/xiaoyanyu/Desktop/Data /Summary/Data_Summary"

# 绘图输出保存路径
plot_output_path = "/Users/xiaoyanyu/Desktop/Data /Summary/Plot"

# 待处理数据
experiment_csv_analysis_config = {
    'sorbent_3': {
        '3_1': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230808/proccessed_data/2023-08-08_09-00-45_1.csv",
                'Date': '2023-08-08', 'StartTime': '10:29:29'},
        '3_2': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230808/proccessed_data/2023-08-08_10-51-29_1.csv",
                'Date': '2023-08-08', 'StartTime': '11:28:57'},
        '3_3': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230808/proccessed_data/2023-08-08_11-52-22_1.csv",
                'Date': '2023-08-8', 'StartTime': '12:24:43'},
        '3_4': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230808/proccessed_data/2023-08-08_14-31-29_1.csv",
                'Date': '2023-08-08', 'StartTime': '14:32:09'},
        '3_5': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230808/proccessed_data/2023-08-08_14-56-28_1.csv",
                'Date': '2023-08-08', 'StartTime': '15:31:56'},
        '3_6': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230605/proccessed_data/2023-06-05_08-49-00_3.csv",
                'Date': '2023-06-05', 'StartTime': '11:58:34'},
        '3_7': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230605/proccessed_data/2023-06-05_13-20-10_1.csv",
                'Date': '2023-06-05', 'StartTime': '13:57:35'},
        '3_8': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230605/proccessed_data/2023-06-05_14-26-33_1.csv",
                'Date': '2023-06-05', 'StartTime': '15:59:23'}

    },

    'sorbent_2': {
        '2_1': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_09-07-18_1.csv",
                'Date': '2023-05-25', 'StartTime': '12:19:43'},
        '2_2': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_11-01-42_1.csv",
                'Date': '2023-05-25', 'StartTime': '11:07:27'},
        '2_3': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_11-01-42_2.csv",
                'Date': '2023-05-25', 'StartTime': '12:21:16'},
    },

    'sorbent_1': {
        '1_1': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230511/proccessed_data/2023-05-11_11-31-18_1.csv",
                'Date': '2023-05-11', 'StartTime': '11:47:43'},
        '1_2': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230511/proccessed_data/2023-05-11_11-31-18_2.csv",
                'Date': '2023-05-11', 'StartTime': '14:26:40'},
        '1_3': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230511/proccessed_data/2023-05-11_11-31-18_3.csv",
                'Date': '2023-05-11', 'StartTime': '15:44:51'}
        },

    'sorbent_4': {
        '4_1': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_13-30-36_2.csv",
                'Date': '2023-05-25', 'StartTime': '14:51:15'},
        '4_2': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_15-27-30_1.csv",
                'Date': '2023-05-25', 'StartTime': '15:46:38'},
        '4_3': {'File_parth': "/Users/xiaoyanyu/Desktop/Data /20230525/proccessed_data/2023-05-25_16-24-19_1.csv",
                'Date': '2023-05-25', 'StartTime': '16:47:22'}
    }

}
