import requests
from pyquery import PyQuery as pq
import pprint

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',

}
#根据书名或者作者名列出笔趣阁网站的所有相关小说
def find_by_name(name):
    params = {
        'siteid':'qula',
        'q':name,
    }
    try:
        results = requests.get('https://sou.xanbhx.com/search',params=params,headers=headers,verify=False)
        print(results.url)
        if results.status_code==200:
            return results
    except requests.ConnectionError:
        print('Request Failed!')

def parse_html(html):
    if html:
        doc = pq(html.content)
        items = doc('ul li').items()
        print(next(items).text())
        index=1
        booklist=['0']
        for item in items:
            print('%d.'%index,item.text())
            url = item('.s2 a').attr('href')
            booklist.append(url)
            index +=1
        return booklist
    else:
        print('没有返回结果!')

#下载本小说
def detail_novel(booklist):
    if booklist:
        while True:
            print('请输入您想获取的小说前面的序号：')
            index = int(input())
            if index in range(1,len(booklist)):
                break
            else:
                print('您输入的序号错误，请重新输入:')
    print('您将下载%d'%index)

if __name__ == '__main__':
    print('请输入你需要查询的小说书名关键词或者作者名字：')
    name = str(input())
    results =find_by_name(name)
    booklist = parse_html(results)
    detail_novel(booklist)
