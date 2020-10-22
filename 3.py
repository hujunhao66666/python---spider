import requests
from bs4 import BeautifulSoup
import random
import time
from openpyxl import Workbook
import json

def get_json(url_start,url_parser,page,lang_name):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    data={'first':'true',
          'pn':str(page),
          'kd':lang_name}
    s=requests.Session()
    s.get(url_start,headers=headers,timeout=3)
    cookie=s.cookies
    response=s.post(url_parser,data=data,headers=headers,cookies=cookie,timeout=3)
    time.sleep(5)
    response.encoding=response.apparent_encoding
    text=json.loads(response.text)
    list_con=text['content']['positionResult']['result']
    info_list=[]
    for i in list_con:
        info=[]
        info.append(i['companyShortName'])
        info.append(i['companyFullName'])
        info.append(i['industryField'])
        info.append(i['companySize'])
        info.append(i['salary'])
        info.append(i['city'])
        info.append(i['education'])
        print(1)
        info_list.append(info)
    return info_list

def main():
    lang_name='python'
    wb=Workbook()
    for i in ['南京','深圳','上海']:
        page=1
        ws1=wb.active
        ws1.title=lang_name
        url_start='https://www.lagou.com/jobs/list_python?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput='
        url_parser= "https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false".format(i)
        while page<11:
            info=get_json(url_start,url_parser,page,lang_name)
            page+=1
            time.sleep(random.randint(10,20))
            for row in info:
                ws1.append(row)
    wb.save('{}职位信息.xlsx'.format(lang_name))

if __name__=='__main__':
    main()

