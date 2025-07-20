import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

# 读取情感分析结果
result_df = pd.read_csv('情感分析_带时间.csv', encoding='utf-8-sig')

# 映射规则
def map_sentiment(label):
    if "positive" in label:
        return 1
    elif "negative" in label:
        return 0
    else:
        return None  # 未知情感

# 应用映射
result_df["情感数值"] = result_df["标签"].apply(map_sentiment)
# 2. 文本长度特征
result_df['文本长度'] = result_df['评论'].str.len()

# 3. 关键词特征
vectorizer = CountVectorizer(max_features=100)  # 提取100个高频词
X = vectorizer.fit_transform(result_df['评论'])
keywords_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# 合并关键词特征到主表
result_df = pd.concat([result_df.reset_index(drop=True), keywords_df], axis=1)

# 4. 时间特征
# 假设原始评论数据中包含时间列，例如 '评论时间'
try:
    # 直接使用 '情感分析_带时间.csv' 中的 '评论时间' 列
    if '评论时间' in result_df.columns:
        result_df['评论时间'] = pd.to_datetime(result_df['评论时间'])
        result_df['小时'] = result_df['评论时间'].dt.hour
        result_df['星期几'] = result_df['评论时间'].dt.weekday
        result_df['是否周末'] = result_df['星期几'].apply(lambda x: 1 if x >= 5 else 0)
except Exception as e:
    print("情感分析结果文件中的时间戳字段格式错误，跳过时间特征提取。")

# 5. 讨论热度（按天统计评论数量和情感均值）
try:
    if '评论时间' in result_df.columns:
        result_df['日期'] = result_df['评论时间'].dt.date
        daily_summary = result_df.groupby('日期').agg(
            情感均值=('情感数值', 'mean'),
            讨论量=('评论', 'count')
        ).reset_index()
        result_df = pd.merge(result_df, daily_summary, on='日期', how='left')
except Exception as e:
    print("无法进行讨论热度聚合，跳过该步骤。")

# 保存最终特征数据
result_df.to_csv('特征数据.csv', index=False, encoding='utf-8-sig')

print("特征提取完成，结果已保存到 '特征数据.csv'")
