import requests
from lxml import etree
import time


city=None
def get_data():
    #搜索关键词
    keyword=input('请输入你想搜索的关键词：')
    # 招聘城市
    global city
    city=input('请输入你想招聘的城市：')
    #抓取页数
    pages=int(input('请输入你想抓取的页数：'))
    #定义请求头
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        'cookie':'index_location_city=%E5%85%A8%E5%9B%BD; RECOMMEND_TIP=1; user_trace_token=20250711144247-7aa15286-61f4-4046-a5de-dd7b8c01dbf6; LGUID=20250711144247-994d9131-98d0-49a0-ad94-f1b5f76f0156; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1752216169; gate_login_token=v1####0d0fc32bb4598a3b97aeb2172d46189c837bc12bf360d3849c6f3d2d226c9ac6; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; __RESUME_COMPLETE_POPOVER__=1; __lg_stoken__=c7e772c612277c73da13ee37bcb202303aa8b5ef09fbf0f88a464f2ce0f76e6fc269369bb8202be613afa59d96624ed6e01ea17316a0276ef50dedafe17a1b96164434712f56; _ga=GA1.2.861815267.1752226488; _gid=GA1.2.1946583624.1752226489; _ga_DDLTLJDLHH=GS2.2.s1752226489$o1$g1$t1752226493$j56$l0$h0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; JSESSIONID=ABAACCCABHJABDA32E7867E6B16A57F4181254554224685; WEBTJ-ID=20250712111048-197fc9d2ce89ca-077ecc4947b25a-4c657b58-1638720-197fc9d2ce91f6f; sensorsdata2015session=%7B%7D; _putrc=FD5FD3ADA213B84B123F89F2B170EADC; login=true; unick=%E7%94%A8%E6%88%B70480; X_HTTP_TOKEN=351161adc494c9ee6010922571be57c7b2fb461d6a; X_MIDDLE_TOKEN=b494148abc845c4da3bf9291f9166b0e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2227785704%22%2C%22first_id%22%3A%22197f827311e132-0e69793596203a8-4c657b58-1638720-197f827311f19ca%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22PC_SEARCH%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22138.0.0.0%22%7D%2C%22%24device_id%22%3A%22197f827311e132-0e69793596203a8-4c657b58-1638720-197f827311f19ca%22%7D'
    }
    info_list=[]
    for i in range(pages):
        url=f'https://www.lagou.com/wn/jobs?pn={i+1}&fromSearch=true&kd={keyword}&city={city}'

        respond=requests.get(url,headers=headers)
        html_tree=etree.HTML(respond.text)
        data_list=html_tree.xpath('//div[@class="list__YibNq"]/div')

        for data in data_list:
            text=data.xpath('.//text()')
            info_list.append(text)
        time.sleep(3)
    return info_list
data=get_data()