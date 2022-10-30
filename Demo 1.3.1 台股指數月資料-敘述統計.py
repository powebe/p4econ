# Demo 1.3.1 計算台股指數月資料之連續複利報酬率
!pip install yfinance
!pip install numpy
!pip install pandas
!pip install --upgrade xlrd 
import yfinance as yf
import numpy as np
import pandas as pd

def ldiff(x):
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff


# 從讀放在雲端的 Excel 檔
url = 'http://gretlcycu.files.wordpress.com/2022/05/fe-all.xls'
sheet_name = 'FE-ex1'
data = pd.read_excel(url,sheet_name)
print(data)
print(data.head(63))
print(data.tail(30))

# 計算連續複利報酬, 放在 df1
df1 = pd.DataFrame({'r_twi':ldiff(data['twi']),
             'r_twpl':ldiff(data['twpl']),
             'r_twir':ldiff(data['twir']),
             'r_twee':ldiff(data['twee']),
             'r_twfi':ldiff(data['twfi']),
             'r_sp500':ldiff(data['sp500'])}
             )

# 檢查內容
print(df1)
print(df1.head(63))
print(df1.tail(30))

# 選擇子樣本 (2000:01 - 2006:12)，放到 df1_sub
df1_sub=df1.iloc[59:143,:] # 往前移

# 列印敘述統計
df1_sub.describe().round(4)

df1_sub_summary = df1_sub.describe()

# 更名引用 scipy.stats 來使用 .skew() 抓偏態係數和 .kurtosis() 抓超峰態係數
import scipy.stats as scs
sk = scs.skew(df1_sub)
ek = scs.kurtosis(df1_sub)

# 看 sk、ek 的內容
# .round(4) 用來取小數點後4位
print(sk.round(4))
print(ek.round(4))

# -----------------------------------------------------------
# 以下為進階 dataframe 表格合併之處理

# 將 sk、ek 轉成 dataframe 用來合併在 df1_sub_summary
dfsk = pd.DataFrame(sk).T
dfek = pd.DataFrame(ek).T

# 將 df1_sub_summary 的欄位名稱，放在 dfsk、dfek 中
dfsk.columns=df1_sub_summary.columns
dfek.columns=df1_sub_summary.columns

# 將 dfsk、dfek 的 index 名稱，改成 'Skew'、'ExcsKurt'
dfsk = dfsk.rename(index={0:'Skew'})
dfek = dfek.rename(index={0:'ExcsKurt'})

# 查看 dfsk
dfsk

# 欄名、欄位數要相同，pd.concat() 才能順利合併
df1_sub_summary = pd.concat([df1_sub_summary,dfsk,dfek])

# 查看 df1_sub_summary
df1_sub_summary

# 將 df1_sub_summary 表格轉置
# .T 用來轉置 dataframe; .round(4) 用來取小數點後4位
df1_sub_summary.T.round(4)
