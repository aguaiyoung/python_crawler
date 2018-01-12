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
import codecs
import json
import unicodecsv
#import pandas
import sys,getopt

data=[]
class item:
   def __init__(self):
        self.name = ''     
        self.url = ''
        self.end_date = ''
        self.output = '0'
        self.num = ''
        self.location = ''
  
class bcolors:
   HEADER = '\033[95m'
   RED = '\033[1;31;40m'
   BLUE = '\033[1;34;40m'
   GREEN = '\033[1;32;40m'
   YELLOW = '\033[1;33;40m'
   FAIL = '\033[5;31;40m'
   ENDC = '\033[0m'

def disable(self):
   self.HEADER = ''
   self.BLUE = ''
   self.GREEN = ''
   self.WARNING = ''
   self.FAIL = ''
   self.ENDC = ''

def writeToCsv(title, houseinfo, position, unitprice, totalprice, dealprice, dealDate):
    #data_str = data.encode('utf8')
    
    data = u''.join(title)
    #data += u''.join(houseinfo)
    #data += u''.join(position)
    #data += u''.join(unitprice)
    #data += u''.join(totalprice)
    #data += u''.join(dealprice)
    #data_str = data.encode('ascii', 'ignore').decode('ascii')
    print data
    
    #writer.writerow([title, houseinfo , position , unitprice, totalprice, dealprice])
    writer.writerow(data)
    return

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

def posthtml(url, page, location):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #data = {'startIssue' : start_date, 'endIssue' : end_date,'pageSize' : "30",'currentPage':page}
    data_encoded = urllib.urlencode(data)
    response = opener.open(url,data_encoded)
    html_string = response.read()
    return html_string

def lianjia_caputure(soup):
    tradedHouseList = soup.find("ul", class_="listContent").find_all('li')
    if not tradedHouseList:
       return 
    #print tradedHouseList
    for item in tradedHouseList:
        title = item.find("div", class_="title").string
        #print item
        houseinfo = item.find("div",class_="houseInfo").text
        position  = item.find("div",class_="positionInfo").text
        unitprice = item.find("div",class_="unitPrice").text
        totalprice = item.find("div",class_ ="totalPrice").text
        dealDate = item.find("div",class_ ="dealDate").text
        #print totalprice
        deal_price = item.find("div",class_ ="dealCycleeInfo")
        if not deal_price:
           dealprice= '--'
        else:
           dealprice=deal_price.text
        print (bcolors.YELLOW + title +bcolors.ENDC +' ' +houseinfo + ' ' + position +' ' +bcolors.GREEN + unitprice + bcolors.ENDC + bcolors.RED  + u' 挂牌 ' +totalprice + bcolors.ENDC +' ' + bcolors.GREEN + dealprice + bcolors.ENDC + ' ' + dealDate)
        if int(a.output) is 1:
           writeToCsv(title, houseinfo, position, unitprice, totalprice, dealprice, dealDate)
    return

def usage():
    print (" -r rent ")
    print (" -e end_date ")
    print (" -l location")
    print (" -v output file ")
    print (" -x pagenum ")
    print (" -h help ")
    print (" example: python *.py -s 2017001 -e 2017151 ")
    return

def parsecmd(a):
    opts, args = getopt.getopt(sys.argv[1:], "hr:e:x:v:l:")
    for op, value in opts:
        if op == "-r":
            a.url = url_rent
        elif op == "-e":
            a.end_date = value
        elif op == "-x":
            a.num = value
        elif op == "-v":
            a.output = value
        elif op == "-l":
            a.location = value
        elif op == "-h":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()
    return

url_deal = 'https://bj.lianjia.com/chengjiao/'
url_rent = 'https://bj.lianjia.com/zufang/'
max = 29
index = 29

a = item()
a.name ='lianjia'
a.url = url_deal
if len(sys.argv) < 2:
    a.num = '2'
    a.location = 'yayuncun'
    a.output = '0'
else:  
    parsecmd(a)
    if a.num is '':
       a.num = '2'
    if a.location is '':
       a.location = 'yayuncun'

print a.url 
if int(a.output) is 1:
   csvfile = file('lianjia.csv', 'wb')
   #csvfile = codecs.open('temp.csv', 'w', 'utf_8_sig')  
   #writer = unicodecsv.writer(csvfile,encoding='utf-8-sig')
   csvfile.write(codecs.BOM_UTF8)
   writer = csv.writer(csvfile)
   writer.writerow(['地址', ' 房屋信息 ', ' 位置 ', ' 挂牌价 ', ' 成交价格 '])

for i in range(1, int(a.num)):
    if a.end_date is '':
        lianjia = a.url + a.location + '/pg' + str(i)
        print lianjia 
        html_doc = gethtml(lianjia)
    else:
        html_doc = posthtml(a.url, i, a.location)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    #print soup
    lianjia_caputure(soup)

if int(a.output) is 1:
    csvfile.close()
print 'done'
