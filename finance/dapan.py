import tushare as ts

df = ts.get_index()
print df

df = ts.get_today_ticks('601333')
print df.head(10)
