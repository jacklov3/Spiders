import grequests
import requests
from pyquery import PyQuery as pq
import csv
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from utils import fn_timer



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',

}


# 根据书名或者作者名列出笔趣阁网站的所有相关小说
def find_by_name(name):
    params = {
        'keyword': name,
    }
    try:
        results = requests.get('https://www.biquge.com.cn/search.php', params=params, headers=headers)
        # print(results.url)
        if results.status_code == 200:
            return results
    except requests.ConnectionError:
        print('Request Failed!')


# 列出根据关键词查询到的书列表
def parse_html(html):
    if html:
        doc = pq(html.content)
        booklist = doc('.result-game-item-detail')
        bookdict = [0]
        resultindex = 1
        for item in booklist.items():
            print(resultindex)
            url = item('a').attr('href')
            name = item('a').text()
            bookdict.append({'name': name.split(' ')[0], 'url': url})
            # print(url)
            print(name)
            print(item('.result-game-item-desc').text())
            for i in item('.result-game-item-info-tag').items():
                print(i.text())
            print('\n')
            print('-' * 20)
            print('\n')
            resultindex += 1
        print('请输入你想爬取的小说序号(例如1、2...等):')
        while True:
            index = int(input())
            if index in range(1, len(bookdict)):
                break
            else:
                print('没有您需要的小说序号，请检查输入后重新输入序号！')
        try:
            print('您即将下载小说  <<' + bookdict[index]['name'] + '>>')
            return bookdict[index]
        except IndexError as e:
            print(e)
    else:
        print('没有返回结果!')


# 获取目录和章节url
# axel -n 10
def getchapter(bookinfo):
    response = requests.get(bookinfo['url'], headers=headers)
    baseurl = bookinfo['url'] + '/'
    if response.status_code == 200:
        doc = pq(response.content)
        chapters = doc('dd')
        bookname = bookinfo['name'] + '.csv'
        with open(bookname, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['chapter', 'url'])
            joined = []
            for item in chapters.items():
                url = item('a').attr('href')
                url = urljoin(baseurl, url)
                if url not in joined:
                    writer.writerow([item.text(), url])
                    joined.append(url)
        return bookname, len(joined)
    else:
        print('connection error!')


#获取单章节内容,用于多线程下载
def getsinglepage(url):
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        doc=pq(response.content)
        chaptername = doc('.bookname h1').text()
        content = doc('#content').text()
        return {'chapter':chaptername,'content':content}
    else:
        print('请求失败!')


#异步下载测试
@fn_timer
def asyncdown(bookcsv,size):
    #将下载链接导入到urls列表中
    urls = []
    with open(bookcsv, 'r', encoding='utf-8') as book:
        reader = csv.reader(book)
        next(reader)  # 跳过文件头
        for row in reader:
            urls.append(row[1])
    #异步请求
    ru = (grequests.get(u) for u in urls)
    responses =grequests.map(ru)
    bookname = bookcsv.split('.')[0] + '.txt'
    with open(bookname, 'a', encoding='utf-8') as writebook:
        completed = 0.0
        count = 1
        for response in responses:
            if response.status_code == 200:
                doc = pq(response.content)
                chaptername = doc('.bookname h1').text()
                content = doc('#content').text()
            # print(future)
                try:
                    writebook.write(chaptername)
                    writebook.write('\n\n')
                    writebook.write(content)
                    writebook.write('\n\n')
                    completed = count / size * 100
                    print('目前已经完成了%0.2f%%' % completed)
                    count += 1
                except Exception as exc:
                    print('写入失败')
            else:
                print('请求失败')


# 线程池下载测试
@fn_timer
def downloadbook(bookcsv, size):
    urls=[]
    with open(bookcsv, 'r', encoding='utf-8') as book:
        reader = csv.reader(book)
        next(reader)#跳过文件头
        for row in reader:
            urls.append(row[1])
    with ThreadPoolExecutor(max_workers=64) as executor:
        bookname = bookcsv.split('.')[0] + '.txt'
        #线程池map映射
        future_to_url = executor.map(getsinglepage,urls)
        with open(bookname, 'a', encoding='utf-8') as writebook:
            completed = 0.0
            count = 1
            for future in future_to_url:
                # print(future)
                try:
                    writebook.write(future['chapter'])
                    writebook.write('\n\n')
                    writebook.write(future['content'])
                    writebook.write('\n\n')
                    completed = count / size * 100
                    print('目前已经完成了%0.2f%%' % completed)
                    count += 1
                except Exception as exc:
                    print('写入失败')


if __name__ == '__main__':
    print('请输入你需要查询的小说书名关键词或者作者名字：')
    name = str(input())
    # 获取根据关键词查询的响应
    results = find_by_name(name)
    # 解析响应文本，返回用户想下载的小说url
    bookinfo = parse_html(results)
    # 根据小说url获取章节和目录信息
    bookcsv, size = getchapter(bookinfo)
    # downloadbook(bookcsv, size)
    asyncdown(bookcsv,size)
