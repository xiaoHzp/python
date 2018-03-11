import urllib.request
import urllib.parse
import http.cookiejar

info = open("info.ini", "r")
strlist = info.readlines()
name = strlist[0].split(":")[1].strip()
pwd = strlist[1].split(":")[1].strip()

info.close()
if strlist[2] == "0":
    url = "http://202.117.144.205:8601/snnuportal/login"
    postdata = urllib.parse.urlencode({"account":name, "password":pwd}).encode("utf-8")
    req = urllib.request.Request(url, postdata)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299" )
    file = urllib.request.urlopen(req)
    strlist[2] = "1"
else:
    url = "http://202.117.144.205:8602/snnuportal/logoff"
    req = urllib.request.Request(url)
    postdata = urllib.parse.urlencode({"account":name, "password":pwd}).encode("utf-8")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299")
    file = urllib.request.urlopen(req)
    strlist[2] = "0"

with open("info.ini","w") as f:
    for i in range(0,3):
        f.writelines(strlist[i])


"""
fhandle = open("1.html", "wb")
fhandle.write(data)
fhandle.close()
"""