import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# 读取数据
df = pd.read_csv('特征数据.csv')

# 构造抽取标签（示例：评论中包含“抽”或“十连”则标记为1）
df['是否抽取'] = df['评论'].str.contains('抽|十连|必抽|卡|抽卡', case=False).astype(int)

# 特征选择
X = df[['情感数值', '讨论量', '文本长度']]
y = df['是否抽取']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练随机森林模型
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 评估模型
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 获取特征重要性
feature_importance = model.feature_importances_
feature_names = X.columns

# 显示特征重要性
importance_df = pd.DataFrame({'特征': feature_names, '重要性': feature_importance})
importance_df = importance_df.sort_values(by='重要性', ascending=False)
print(importance_df)
