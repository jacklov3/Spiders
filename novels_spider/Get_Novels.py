import requests
from pyquery import PyQuery as pq
import csv
from urllib.parse import urljoin

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',

}

#根据书名或者作者名列出笔趣阁网站的所有相关小说
def find_by_name(name):
    params = {
        'keyword':name,
    }
    try:
        results = requests.get('https://www.biquge.com.cn/search.php',params=params,headers=headers)
        # print(results.url)
        if results.status_code==200:
            return results
    except requests.ConnectionError:
        print('Request Failed!')

#列出根据关键词查询到的书列表
def parse_html(html):
    if html:
        doc = pq(html.content)
        booklist = doc('.result-game-item-detail')
        for item in booklist.items():
            print(item('a').attr('href'))
            print(item('a').text())
            print(item('.result-game-item-desc').text())
            for i in item('.result-game-item-info-tag').items():
                print(i.text())
        # print(next(items).text())
        # index=1
        # booklist=['0']
        # for item in items:
        #     print('%d.'%index,item.text())
        #     url = item('.s2 a').attr('href')
        #     booklist.append(url)
        #     index +=1
        # return booklist
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

    return booklist[index]

#获取目录和章节url
def getchapter(bookurl):
        response = requests.get(bookurl,headers=headers)
        baseurl = bookurl+'/'
        if response.status_code==200:
            doc = pq(response.content)
            chapters = doc('dd')
            bookname = doc('h1')
            with open('data.csv','w',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile,delimiter=' ')
                writer.writerow(['章节名','url'])
                joined=[]
                for item in chapters.items():
                    url = item('a').attr('href')
                    url = urljoin(baseurl,url)
                    if url not in joined:
                        writer.writerow([item.text(),url])
                        joined.append(url)
                for i in sorted(joined):
                    print(i)


if __name__ == '__main__':
    print('请输入你需要查询的小说书名关键词或者作者名字：')
    name = str(input())
    results =find_by_name(name)
    # booklist = parse_html(results)
    # bookurl =detail_novel(booklist)
    # getchapter(bookurl)
    parse_html(results)