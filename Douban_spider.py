import urllib.request
import re
import json


class DouBanSpider:

    def __init__(self, url, start=100, end=90): # start和end用于控制预筛选对象
        self.url = url
        s = "interval_id={0}%3A{1}".format(start, end)
        self.count_url = "https://movie.douban.com/j/chart/top_list_count?type=4&" + s
        self.tmp_url = "https://movie.douban.com/j/chart/top_list?type=4&" + s

    def __get_type(self): # 获取相应url中对应的type类型
        re_type_pattern = r'type=(\d*)'
        type = re.search(re_type_pattern, self.url)
        return type.group(1)

    def __get_count(self): # 获取总的电影数
        url = re.sub('type=(\d*)', 'type=' + str(self.__get_type()), self.count_url)
        file = urllib.request.urlopen(url)
        data = json.loads(file.read().decode('utf-8'))
        return data['total']

    def __get_item(self): # 获取每个电影项目
        url = re.sub('type=(\d*)', 'type='+str(self.__get_type()), self.tmp_url)
        post_param = {'action': '', 'start': '0', 'limit': str(self.__get_count())}
        file = urllib.request.urlopen(url, data=urllib.parse.urlencode(post_param).encode('utf-8'))
        data = json.loads(file.read().decode())
        print(data)
        return data

    def write_all(self):
        data = self.__get_item()
        with open("moive.txt", "w") as f:
            for item in data:
                result = str(item['title']) + '\t' + str(item['regions']) + '\t' + str(item['score']) + '\t' + str(item['vote_count']) + '\n'
                f.write(result)

test = DouBanSpider("https://movie.douban.com/typerank?type_name=喜剧片&type=24&interval_id=100:90&action=") # 把想要查询的分类的网址传入就行，自己设定相应的预筛选
test.write_all()




