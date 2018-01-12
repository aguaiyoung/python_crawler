# -*- coding: utf-8 -*-  
__author__ = 'aguai'
import tushare as ts

df = ts.get_realtime_quotes('300017') #Single stock symbol
print df[['code','name','price','bid','ask','volume','amount','time']]

print u'一次性获取全部日k线数据'
ab = ts.get_hist_data('300017')
print ab

print u'当日历史分笔¶'
df = ts.get_today_ticks('300017')
print df.head(10)
