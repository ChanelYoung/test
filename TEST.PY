import numpy as np
import pandas as pd

# 读取现有的CSV文件
existing_data = pd.read_csv("existing_data.csv")

# 生成数据的数量，与已有数据的行数相同
data_size = len(existing_data)

# 生成两个符合正态分布的随机数列
mean_annual_saving, std_annual_saving = 50000, 10000
mean_salary, std_salary = 80000, 15000
annual_saving = np.random.normal(mean_annual_saving, std_annual_saving, data_size)
salary = np.random.normal(mean_salary, std_salary, data_size)

# 添加一些噪音，使数据稍微分散开来
noise = np.random.normal(0, 5000, data_size)
annual_saving += noise
salary += noise

# 确保两列之间存在一定的线性相关性
correlation = 0.8
salary = correlation * annual_saving + (1 - correlation) * salary

# 将生成的数据添加到现有的DataFrame中
existing_data['annual_saving'] = annual_saving
existing_data['salary'] = salary

# 将数据保存为新的CSV文件
existing_data.to_csv('updated_data.csv', index=False)

print("已将生成的数据添加到updated_data.csv")

import numpy as np
import pandas as pd

# 读取现有的CSV文件
existing_data = pd.read_csv("existing_data.csv")

# 生成数据的数量，与已有数据的行数相同
data_size = len(existing_data)

# 生成符合正态分布的annual_saving数据
mean_annual_saving, std_annual_saving = 50000, 10000
annual_saving = np.random.normal(mean_annual_saving, std_annual_saving, data_size)

# 添加一些噪音，使数据稍微分散开来
noise = np.random.normal(0, 5000, data_size)
annual_saving += noise

# 确保annual_saving和debt_in_track之间存在非线性相关性
correlation_annual_debt = 0.6  # 非线性相关性系数
debt_in_track = correlation_annual_debt * np.sqrt(annual_saving) + np.random.normal(0, 5000, data_size)

# 生成符合正态分布的salary数据
mean_salary, std_salary = 80000, 15000
salary = np.random.normal(mean_salary, std_salary, data_size)

# 添加一些噪音，使数据稍微分散开来
salary += noise

# 确保annual_saving和salary之间存在线性相关性
correlation_annual_salary = 0.8  # 线性相关性系数
salary = correlation_annual_salary * annual_saving + (1 - correlation_annual_salary) * salary

# 将生成的数据添加到现有的DataFrame中
existing_data['annual_saving'] = annual_saving
existing_data['salary'] = salary
existing_data['debt_in_track'] = debt_in_track

# 将数据保存为新的CSV文件
existing_data.to_csv('updated_data.csv', index=False)

print("已将生成的数据添加到updated_data.csv")

import pandas as pd

# Read the CSV file
data = pd.read_csv("your_input_file.csv")

# Find the numerical columns
numerical_columns = data.select_dtypes(include=[float, int]).columns

# Round the numerical columns to two decimal places
data[numerical_columns] = data[numerical_columns].round(2)

# Save the updated data to a new CSV file
data.to_csv("your_output_file.csv", index=False)

