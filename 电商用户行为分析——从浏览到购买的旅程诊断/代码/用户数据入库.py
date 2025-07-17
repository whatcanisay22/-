import pandas as pd
import mysql.connector
from mysql.connector import Error


def import_user_behavior():
    """
    将淘宝用户行为数据导入MySQL数据库
    数据结构：user_id, behavior_type, timestamp
    """
    try:
        # 1. 读取CSV数据
        df = pd.read_csv('data_clean.csv', header=None,
                         names=['user_id', 'behavior_type', 'date'])

        # 2. 数据清洗
        valid_behaviors = ['pv', 'buy', 'cart', 'fav']
        df = df[df['behavior_type'].isin(valid_behaviors)]
        df = df.dropna()

        # 3. 数据库连接配置
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='241015',
            database='firm_data'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 4. 智能创建表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_behavior (
                user_id VARCHAR(20),
                behavior_type VARCHAR(10),
                date DATE
            ) 
            """)

            # 5. 准备批量插入SQL
            insert_sql = """
            INSERT INTO user_behavior 
            (user_id, behavior_type, date)
            VALUES (%s, %s, %s)
            """

            # 6. 转换数据格式为元组列表
            records = []
            for _, row in df.iterrows():
                records.append((
                    str(row['user_id']),
                    row['behavior_type'],
                    row['date']
                ))

            # 7. 执行批量插入（分批处理避免内存溢出）
            batch_size = 10000
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                cursor.executemany(insert_sql, batch)
                connection.commit()
                print(f"已批量插入 {len(batch)} 条记录，累计 {i + len(batch)}/{len(records)}")

            print(f"数据导入完成！总计 {len(records)} 条记录")

    except Error as e:
        print(f"数据库操作失败: {e}")
        if 'connection' in locals() and connection.is_connected():
            connection.rollback()
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


# 执行导入
if __name__ == "__main__":
    import_user_behavior()