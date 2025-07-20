import requests
import csv
import time
import random
import re

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'Referer': 'https://www.miyoushe.com/',
    'X-Requested-With': 'XMLHttpRequest'
}

# 评论接口
api_url = 'https://bbs-api.miyoushe.com/post/wapi/getPostReplies'

# 请求参数
params = {
    'post_id': '65375740',
    'gid':6,
    'last_id':0,
    'is_hot': 'true',
    'size': 20
}

# CSV 文件写入准备
csv_file = open('miyoushe_comments.csv', mode='a', newline='', encoding='utf-8-sig')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['用户名', 'UID', 'IP归属地', '楼层','时间','评论内容'])


# 迭代爬取
try:
    while True:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            print("请求失败，状态码：", response.status_code)
            break

        data = response.json()
        comments = data.get('data', {}).get('list', [])

        if not comments:
            print("没有更多评论了。")
            break

        for i in comments:
            reply = i.get('reply')
            if not reply:
                continue

            # 提取评论内容并清洗
            content_first = reply.get('content', '')
            cleaned_comment = re.sub(r'<img[^>]*>', '', content_first).strip()
            content = cleaned_comment.split('_', 1)[0]

            # 时间处理
            data_time = reply.get('created_at', 0)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_time))

            floor_id = reply.get('floor_id', '')
            user = i.get('user', {})
            uid = user.get('uid', '')
            nickname = user.get('nickname', '')
            ip = user.get('ip_region', '')

            # 写入 CSV
            csv_writer.writerow([nickname, uid, ip, floor_id, date, content])

            # 打印输出
            # print(f'{date} {floor_id} {nickname} {uid} {ip} {content}')

        # 更新 last_id，继续下一页
        params['last_id'] += params['size']

        #设定退出机制
        if params['last_id'] > 11340:
            break

        print(f'已爬取 {params["last_id"]} 条评论。')

        # 随机延迟，防止被封
        time.sleep(random.uniform(2, 5))

except Exception as e:
    print("发生异常：", e)

finally:
    csv_file.close()
    print("CSV 文件已关闭。")
