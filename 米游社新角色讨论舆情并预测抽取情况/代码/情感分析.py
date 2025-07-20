import pandas as pd
import re
from transformers import pipeline
from itertools import islice


df=pd.read_csv('miyoushe_comments.csv')
comments=df['评论内容']

# 删除空行
comments=comments.dropna()
#重置索引
comments=comments.reset_index(drop=True)

# 清洗文本
def clean_text(text):
    text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    return text

# 使用 HuggingFace 的中文情感分析模型
classifier = pipeline("text-classification", model="models")

# 分段函数（按字符切分更适用于中文）
def chunk_text(text, max_len=512):
    for i in range(0, len(text), max_len):
        yield text[i:i + max_len]

# 存储每条评论的最终情感结果
final_labels = []
final_scores = []

# 对每条评论进行处理
for comment in comments:
    cleaned_comment = clean_text(comment)

    # 如果评论长度 <= 512，直接分析
    if len(cleaned_comment) <= 512:
        result = classifier(cleaned_comment, truncation=True,max_length=510,padding=False,add_special_tokens=True)
        final_labels.append(result[0]['label'])
        final_scores.append(result[0]['score'])

    # 如果长度 > 512，则分段处理，取平均或多数投票
    else:
        chunks = list(chunk_text(cleaned_comment, 512))
        chunk_results = classifier(chunks, truncation=True,max_length=510)

        # 多数投票（标签）
        labels = [res['label'] for res in chunk_results]
        label = max(set(labels), key=labels.count)  # 多数投票

        # 平均得分
        score = sum(res['score'] for res in chunk_results) / len(chunk_results)

        final_labels.append(label)
        final_scores.append(score)
# 将结果保存为 DataFrame
result_df = pd.DataFrame({
    '评论': comments,          # 原始评论
    '标签': final_labels,     # 情感标签
    '得分': final_scores      # 情感得分
})

# 保存为 CSV 文件
result_df.to_csv('情感分析.csv', index=False, encoding='utf-8-sig')

print("情感分析结果已保存到 '情感分析.csv'")