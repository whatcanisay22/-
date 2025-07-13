import mysql.connector
from mysql.connector import Error



#去重和入库
def remove_duplicates_and_save(cleaned_df):

    # 1. 数据去重（基于三个关键字段）
    deduplicated_df = cleaned_df.drop_duplicates(
        subset=['job_name', 'district', 'company_name'],
        keep='first'
    )
    print(f"去重结果: 原始 {len(cleaned_df)} 条 → 去重后 {len(deduplicated_df)} 条")

    # 2. MySQL入库
    try:
        # 数据库连接配置
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='241015',
            database='find_job'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 3. 智能创建表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_positions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_name VARCHAR(100) NOT NULL,
                city VARCHAR(50),
                district VARCHAR(50),
                salary_min DECIMAL(10,2),
                salary_max DECIMAL(10,2),
                experience VARCHAR(50),
                education VARCHAR(50),
                company_name VARCHAR(100) NOT NULL,
                company_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_job (job_name, city, company_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 4. 准备批量插入
            insert_sql = """
            INSERT IGNORE INTO job_positions
            (job_name, city, district, salary_min, salary_max, 
             experience, education, company_name, company_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 5. 转换数据格式,列表中的每一个元素是一行数据的元组
            records = []
            for _, row in deduplicated_df.iterrows():
                records.append((
                    row['job_name'],
                    row.get('city') or row.get('district'),  # 优先使用city字段
                    row.get('district'),
                    row.get('salary_min'),
                    row.get('salary_max'),
                    row.get('experience'),
                    row.get('education'),
                    row['company_name'],  # 必填字段
                    str(row.get('company_info', ''))[:2000]  # 限制长度防止溢出
                ))

            # 6. 执行批量插入
            cursor.executemany(insert_sql, records)
            connection.commit()
            print(f"成功入库 {cursor.rowcount} 条非重复记录")

    except Error as e:
        print(f"数据库操作失败: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return deduplicated_df

# 执行去重和入库
final_df = remove_duplicates_and_save(cleaned_df)

# 查看去重结果
print("\n去重后的数据样例:")
print(final_df[['job_name', 'district', 'company_name']])