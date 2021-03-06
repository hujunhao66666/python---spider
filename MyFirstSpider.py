import requests
from bs4 import BeautifulSoup

def download_page(url):
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r=requests.get(url,headers=headers)
    return r.text

def get_content(html,page):
    output="第{}页 作者：{} 性别：{} 年龄：{} 点赞：{} 评论：{} \n{}\n----------\n"
    soup=BeautifulSoup(html,'lxml')
    con=soup.find('div',id='content')
    con=con.find('div',class_='col1 old-style-col1')
    con=con.find_all('div',class_='article')
    for i in con:
        author=i.find('div',class_='author clearfix').find('a').string
        vote=i.find('span',class_='stats-vote').find('i').string
        comment=i.find('span',class_='stats-comments').find('i').string
        content=i.find('div',class_='content').get_text()
        author_info=i.find('div',class_='articleGender')
        if author_info is not  None:
            class_list=author_info['class']
            if 'womenIcon' in class_list:
                gender='女'
            elif 'manIcon' in class_list:
                gender='男'
            else:
                gender=''
            age=author_info.string
        else:
            gender=''
            age=''

        save_txt(output.format(page,author,gender,age,vote,comment,content))

def save_txt(*arg):
    for i in arg:
        with open('qiubaike.txt','a',encoding='utf-8') as f :
            f.write(i)
def main():
    for i in range(1,14):
        url='https://qiushibaike.com/text/page/{}'.format(i)
        html=download_page(url)
        get_content(html,i)
        
if __name__=='__main__':
    main()
        
    
    
