import requests
from bs4 import BeautifulSoup
import os


def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get(url,headers=headers)
    r.encoding=r.apparent_encoding
    return r.text

def get_pic_list1(url,html):
    soup=BeautifulSoup(html,'lxml')
    pic_list=soup.find('div',class_='postlist')
    pic_list=pic_list.find_all('li')
    b=[]
    name=[]
    for i in pic_list:
        temp1=i.find('a')
        b.append(url+temp1.get('href'))
        temp2=i.find('img')
        name.append(temp2.get('alt'))
    for i in range(len(b)):
        get_pic_list2(b[i],name[i])

def get_pic_list2(url,name):
    for i in range(1,10):
        if i==2:
            url=url[:-5]+'_{}'.format(i)+'.html'
        elif i!=1 and i!=2:
            url=url[:-7]+'_{}'.format(i)+'.html'
        r=requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"})
        r.encoding=r.apparent_encoding
        soup=BeautifulSoup(r.text,'lxml')
        pic_list=soup.find('div',class_='main-image').find('img')
        link=pic_list.get('src')
        get_pic(link,name,i)

def get_pic(link,name,i):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get(link,headers=headers)
    create_dir('link/{}'.format(name))
    with open('link/{}/{}.png'.format(name,i),'wb')as f:
        f.write(r.content)


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def execute(url):
    page_html=download_page(url)
    get_pic_list1(url,page_html)

def main():
    create_dir('pic')
    url='https://www.youmzi.com/'
    execute(url)

if __name__=='__main__':
    main()
