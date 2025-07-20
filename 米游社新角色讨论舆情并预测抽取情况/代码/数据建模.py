import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re

df=pd.read_csv('特征数据.csv')

# 提取角色关键词
character_keywords = ['素裳', '希儿', '灵砂', '白露', '海瑟音', '李素裳', '刻律德拉', '赛飞儿', '缇宝', '风堇', '符华', '林朝雨', '阮梅', '黄泉', '希尔']

def extract_characters(comment):
    found = []
    for keyword in character_keywords:
        if keyword in comment:
            found.append(keyword)
    return found

df['角色'] = df['评论'].apply(extract_characters)

# 受欢迎程度评分（点赞数 + 情感分 + 评论长度）
df['受欢迎程度'] =df['得分'] + df['文本长度'] / 100

# 情感分布统计
sentiment_counts = df['情感数值'].value_counts()

# 角色提及统计
character_counter = Counter()
df['角色'].apply(lambda x: character_counter.update(x))
character_counts = pd.Series(character_counter)

# 受欢迎角色评分（按平均受欢迎评分）
popular_characters = df.explode('角色').groupby('角色')['受欢迎程度'].mean().sort_values(ascending=False)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体

# 绘图：情感分布
plt.figure(figsize=(10, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='coolwarm')
plt.title("情感分布 (Positive vs Negative)")
plt.xlabel("情感")
plt.ylabel("数量")
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.show()

# 绘图：角色提及次数
plt.figure(figsize=(12, 6))
character_counts.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title("角色提及次数")
plt.xlabel("角色")
plt.ylabel("提及次数")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 绘图：角色受欢迎评分
plt.figure(figsize=(12, 6))
popular_characters.plot(kind='bar', color='teal')
plt.title("角色受欢迎程度评分")
plt.xlabel("角色")
plt.ylabel("平均评分")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 打印统计信息
print("情感分布统计:")
print(sentiment_counts)
print("\n角色提及统计:")
print(character_counts)
print("\n角色受欢迎程度评分:")
print(popular_characters)

