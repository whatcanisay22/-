import pandas as pd
import random
#导入数据
columns = ['用户ID', '商品ID', '商品类目ID', '行为类型','时间戳']
data=pd.read_csv('UserBehavior.csv',header=None,names=columns,skiprows=lambda x: x>0 and random.random() > 0.1)

# print(data.info())
# print(data.describe())

# 删除重复值
data= data.drop_duplicates()
#保留商品类目大于0的数据
data = data[data['时间戳'] > 0]

# 将时间戳转为日期格式
data['时间'] = pd.to_datetime(data['时间戳'], unit='s').dt.date
#保留关键列
data=data[['用户ID', '行为类型', '时间']]


# 检查缺失值
print(f"缺失值统计：\n{data.isnull().sum()}")

# 计算用户转化路径
user_journey = data.groupby('用户ID')['行为类型'].apply(list).reset_index()
print(user_journey.head())

# 5. 保存处理后的数据
data.to_csv('data_clean.csv', index=False)