# -*- coding: utf-8 -*-  
__author__ = 'aguai'
from bs4 import BeautifulSoup

#import urllib.request
#import urllib.parse
import re
#import urllib.request, urllib.parse, http.cookiejar
import urllib2
import urllib
from cookielib import CookieJar
import csv
import sys,getopt

class item:
   def __init__(self):
        self.name = ''     
        self.start_date = ''
        self.end_date = ''
        self.output = '0'
        self.num = ''
        self.date = ''
  
class bcolors:
   HEADER = '\033[95m'
   RED = '\033[1;31;40m'
   BLUE = '\033[1;34;40m'
   GREEN = '\033[1;32;40m'
   WARNING = '\033[1;33;40m'
   FAIL = '\033[5;31;40m'
   ENDC = '\033[0m'

def disable(self):
   self.HEADER = ''
   self.BLUE = ''
   self.GREEN = ''
   self.WARNING = ''
   self.FAIL = ''
   self.ENDC = ''

def writeToCsv(date, opennum, reds, blue, writer):
    vol = opennum
    red = reds
    data = [int(vol)]
    for item in red:
        data.append(int(item))
    data.append(int(blue))
    writer.writerow(data)

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

def posthtml(url, page, start_date, end_date):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    data = {'startIssue' : start_date, 'endIssue' : end_date,'pageSize' : "30",'currentPage':page}
    data_encoded = urllib.urlencode(data)
    response = opener.open(url,data_encoded)
    html_string = response.read()
    return html_string

def lottery(index,soup):
    while (index >=0):
        tr = soup.find_all('tr',onmouseout=re.compile("background"))
        tds = tr[max-index].find_all('td')
        opennum = tds[0].get_text()
        date = tds[1].get_text()
        reds = []
        for i in  range(2,8):
            reds.append(tds[i].get_text())
        blue = tds[8].get_text()
        class1_num = tds[10].get_text()
        class1_bonus = tds[11].get_text()
        if a.date is '':
            print(date + ' ' + opennum +u'期开奖号码：'+ bcolors.RED +(',').join(reds) + bcolors.ENDC + ','+ bcolors.BLUE +u' 蓝球：'+ blue + bcolors.ENDC +u' 一等奖 注数: '+class1_num +u' 奖金 :' + bcolors.GREEN + class1_bonus + bcolors.ENDC)
        elif a.date == opennum:
            print(date + ' ' + opennum +u'期开奖号码：'+ bcolors.RED +(',').join(reds) + bcolors.ENDC + ','+ bcolors.BLUE +u' 蓝球：'+ blue + bcolors.ENDC +u' 一等奖 注数: '+class1_num +u' 奖金 :' + bcolors.GREEN + class1_bonus + bcolors.ENDC)
        if int(a.output) is 1:
           writeToCsv(date, opennum, reds, blue, writer)
        index -= 1
    return

def usage():
    print (" -s start_date ")
    print (" -e end_date ")
    print (" -c choose date ")
    print (" -v output file ")
    print (" -x num ")
    print (" -h help ")
    print (" example: python *.py -s 2017001 -e 2017151 ")
    return

def parsecmd(a):
    opts, args = getopt.getopt(sys.argv[1:], "hs:e:x:v:c:")
    for op, value in opts:
        if op == "-s":
            a.start_date = value
        elif op == "-e":
            a.end_date = value
        elif op == "-x":
            a.num = value
        elif op == "-v":
            a.output = value
        elif op == "-c":
            a.date = value
        elif op == "-h":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()
    return

url = 'http://zst.aicai.com/ssq/openInfo/'
max = 29
index = 29
print url 

a = item()
a.name ='lottery'
if len(sys.argv) < 2:
    a.num = '2'
    a.output = '0'
else:  
    parsecmd(a)
    if a.num is '':
       a.num = '2'
    if a.start_date is '' or a.end_date is '' or int(a.start_date) > int(a.end_date) :
        print u'请输入正确的日期'
        sys.exit()

if int(a.output) is 1:
   csvfile = file('lottery.csv', 'wb')
   writer = csv.writer(csvfile)
   writer.writerow(['期号', '   红1 ', ' 红2 ', ' 红3 ', ' 红4 ', ' 红5 ', ' 红6 ', ' 蓝1 '])

for i in range(1, int(a.num)):
    if len(sys.argv) < 2:
        html_doc = gethtml(url)
    else:
        html_doc = posthtml(url, i, a.start_date, a.end_date)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    lottery(index,soup)

if int(a.output) is 1:
    csvfile.close()
print 'done'
