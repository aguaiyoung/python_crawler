# -*- coding: utf-8 -*-  
__author__ = 'zdz8207'
from bs4 import BeautifulSoup

#import urllib.request
#import urllib.parse
import re
#import urllib.request, urllib.parse, http.cookiejar
import urllib2

def getHtml(url):
    #cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
                         ('Cookie', '4564564564564564565646540')]

    urllib.request.install_opener(opener)

    html_bytes = urllib.request.urlopen(url).read()
    html_string = html_bytes.decode('utf-8')
    return html_string

def gethtml(url):
    response = urllib2.urlopen(url)  
    html_string = response.read() 
    return html_string  

url = 'http://zst.aicai.com/ssq/openInfo/'
index = 29
print url 
html_doc = gethtml(url)
soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
#print('yg1')
#print(soup.title)
#table = soup.find_all('table', class_='fzTab nbt')
#print(table)#<tr onmouseout="this.style.background=''" 这种tr丢失了

while (index >= 0):
    #tr = soup.find('tr',attrs={"onmouseout": "this.style.background=''"})
    #tr = soup.find_all('tr',attrs={"onmouseout":"this.style.background=''"})
    #tr = soup.find_all('tr',attrs={"onmouseout":"this.style.background=''"} or {"onmouseout":"this.style.background='#eff3f7'"})
    tr = soup.find_all('tr',onmouseout=re.compile("background"))
    #print tr
    #print tr[index].get_text()
    tds = tr[29-index].find_all('td')
    opennum = tds[0].get_text()
    date = tds[1].get_text()
    #print('yg3')
    #print(opennum)
    #print(date)

    reds = []
    for i in  range(2,8):
        reds.append(tds[i].get_text())
    #print('yg4')
    #print reds
    #print (',').join(reds)
    blue = tds[8].get_text()
    #print('yg5')
    #print blue
    class1_num = tds[10].get_text()
    class1_bonus = tds[11].get_text()
    #print class1_num + ' ' +class1_bonus

    #把list转换为字符串:(',').join(list)
    #最终输出结果格式如：2015075期开奖号码：6,11,13,19,21,32, 蓝球：4
    print(date + ' ' + opennum +u'期开奖号码：'+ (',').join(reds)+u', 蓝球：'+blue +u' 一等奖 注数: '+class1_num +u' 奖金 :'+ class1_bonus)
    index -= 1

