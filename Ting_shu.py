import urllib.request
import urllib.parse
import re
import os.path
import selenium.webdriver

# <a title="第000章" href="/down/?26-0-0.html" target="_blank">第000章</a>


class TingSpider:
    def __init__(self, bookname):
        self.down_pattern = '<a title=.+? href=(.\/down.+?) target=.*?>.+?</a>'  # 匹配下载主页
        self.pattern = '<a title=.+? href=.+? target=.*?>(.+?)</a>'  # 匹配章节名称
        self.hotpattern = '<a href=(.*?) title=.*>.*</a></h2>(\d*?)<b>'  # 匹配书的热度的正则表达
        self.index_url = "http://www.520tingshu.com/search.asp?searchword="  # 搜索主页
        self.down_url_pattern = '<a href=(.+)\/.*\.mp3" target=.*?>.+?</a>'  # 下载链接的地址
        self.bookname = bookname

    def __getmax(self, result):  # 获取搜索的结果中热度最高的那本书
        max_item = None
        for i in range(len(result)):
            if max_item == None:
                max_item = result[i]
            elif int(result[i][1]) > int(max_item[1]):
                max_item = result[i]
        return max_item

    def __searchbook(self):  # 获得要搜索的书的首页地址
        file = urllib.request.urlopen(self.index_url + urllib.parse.quote(self.bookname, encoding='gb2312'))
        data = file.read().decode('gbk')
        result = re.findall(self.hotpattern, data)
        if result is None:
            raise 'No book found'
        res = self.__getmax(result)
        new_url = "http://www.520tingshu.com"+res[0].replace('"', '')
        return new_url


    def __getlist(self):  # 获得该有声小说所有的章节名，小说下载页的url
        bookurl = self.__searchbook()
        req = urllib.request.Request(bookurl)
        file = urllib.request.urlopen(req)
        data = file.read().decode('gbk')
        result = re.findall(self.pattern, data)
        tmp_url = re.search(self.down_pattern, data)
        return result, "http://www.520tingshu.com" + tmp_url.group(1).replace("'", '')

    def __getdownurl(self, downpage):  # 获取下载链接地址的除去文件名的地址
        brower = selenium.webdriver.Edge()
        brower.get(downpage)
        brower.maximize_window()
        result = re.search(self.down_url_pattern, brower.page_source)
        brower.close()
        return result.group(1).replace('"', '') + '/'

    def __getAllUrl(self):  # 获得所有的章节的下载地址
        url = []
        result, downpage = self.__getlist()
        down_url = self.__getdownurl(downpage)
        for item in result:
            tmp_url = down_url + item + ".mp3"
            url.append(urllib.request.quote(tmp_url, safe='/:?='))
        return url

    def down_file(self):  # 下载所有的文件
        result = self.__getAllUrl() # 所有的章节对应的下载地址
        for i in range(len(result)):
            s = str(i)+".mp3"
            if self.__exist(s) == False:
                self.__downfile(result[i], s)

    def __downfile(self, url, filename):  # 将文件下载到本地
        file = urllib.request.urlopen(url)
        data = file.read()
        with open(filename, "wb") as f:
            f.write(data)

    def __exist(self, s):  # 判断是否当前目录已存在某个文件
        if os.path.exists(s):
            return True
        else:
            return False


test = TingSpider("诛仙")
test.down_file()

