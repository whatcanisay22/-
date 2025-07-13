import pandas as pd
import re
from typing import List, Dict, Optional


#薪水
def parse_salary(salary_str: str) -> Dict[str, Optional[float]]:
    """解析薪资字符串为数值字典"""
    if not salary_str or not isinstance(salary_str, str):
        return {'min': None, 'max': None}

    salary_str = salary_str.lower()
    multiplier = 10 if '万' in salary_str else 1  # 万转换为千元单位

    numbers = re.findall(r'(\d+\.?\d*)', salary_str)

    if len(numbers) >= 2:
        return {'min': float(numbers[0]) * multiplier, 'max': float(numbers[1]) * multiplier}
    elif len(numbers) == 1:
        return {'min': float(numbers[0]) * multiplier, 'max': float(numbers[0]) * multiplier}
    return {'min': None, 'max': None}

#教育和经验
def split_exp_edu(exp_edu_str: str) -> Dict[str, Optional[str]]:
    """拆分经验/学历字符串"""
    if not exp_edu_str:
        return {'experience': None, 'education': None}

    parts = [p.strip() for p in exp_edu_str.split('/')]
    return {
        'experience': parts[0] if len(parts) > 0 else None,
        'education': parts[1] if len(parts) > 1 else None
    }

#数据清洗
def clean_and_merge_data(raw_data: List[List[str]]) -> pd.DataFrame:
    """
    清洗并重组数据：
    - 前五列单独拆分
    - 后面列合并为company_info
    """
    processed_data = []

    for row in raw_data:
        # 解析前五列
        record = {
            'job_name': row[0] if len(row) > 0 else None,
            'district': row[1].strip('[]') if len(row) > 1 else None,
            'exp_education': row[3] if len(row) > 3 else None,
            'company_name': row[4] if len(row) > 4 else None
        }

        # 解析薪资
        if len(row) > 2:
            salary = parse_salary(row[2])
            record.update({
                'salary_min': salary['min'],
                'salary_max': salary['max']
            })

        # 合并剩余列为company_info
        company_info_parts = []
        for i in range(5, len(row)):
            item = row[i]
            if isinstance(item, str):
                # 去除福利的引号
                if item.startswith(('"', '“')) and item.endswith(('"', '”')):
                    item = item.strip('"“”')
                company_info_parts.append(item)

        record['company_info'] = ' | '.join(company_info_parts) if company_info_parts else None

        # 拆分经验/学历
        if record['exp_education']:
            exp_edu = split_exp_edu(record['exp_education'])
            record.update(exp_edu)

        processed_data.append(record)

    # 转换为DataFrame
    df = pd.DataFrame(processed_data)

    # 列顺序调整
    final_columns = [
        'job_name', 'district', 'salary_min', 'salary_max',
        'experience', 'education', 'company_name', 'company_info'
    ]
    return df[final_columns]

cleaned_df = clean_and_merge_data(data)
cleaned_df.insert(1, 'city', city)