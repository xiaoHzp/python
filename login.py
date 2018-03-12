import urllib.request
import urllib.parse
import http.cookiejar
import re

info = open("info.ini", "r")
strlist = info.readlines()
name = strlist[0].split(":")[1].strip()
pwd = strlist[1].split(":")[1].strip()
info.close()

def is_login():
    url = "http://202.117.144.205:8601/snnuportal/login.jsp"
    file = urllib.request.urlopen(url)
    data = file.read().decode('gbk')
    format_match = re.search('src="image/denglu01.gif"', data)
    if format_match == None:
        return True
    else:
        return False


if is_login() == False:
    url = "http://202.117.144.205:8601/snnuportal/login"
    postdata = urllib.parse.urlencode({"account":name, "password":pwd}).encode("utf-8")
    req = urllib.request.Request(url, postdata)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299" )
    file = urllib.request.urlopen(req)

else:
    url = "http://202.117.144.205:8602/snnuportal/logoff"
    req = urllib.request.Request(url)
    postdata = urllib.parse.urlencode({"account":name, "password":pwd}).encode("utf-8")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299")
    file = urllib.request.urlopen(req)

