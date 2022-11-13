# Demo 2.2.1 常態性檢定(JB 檢定)
# (接續 Demo 1.3.1 計算台股指數月資料之連續複利報酬率)
!pip install yfinance
!pip install numpy
!pip install pandas

# !pip install --upgrade xlrd 
import yfinance as yf
import numpy as np
import pandas as pd

def ldiff(x):
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff

# 從讀放在雲端的 Excel 檔
url = 'https://github.com/powebe/p4econ/raw/main/fe-all.xlsx'
sheet_name = 'FE-ex1'
data = pd.read_excel(url,sheet_name)

data

# 計算連續複利報酬, 放在 df1
df1 = pd.DataFrame({'obs':data['obs'],
             'r_twi':ldiff(data['twi']),
             'r_twpl':ldiff(data['twpl']),
             'r_twir':ldiff(data['twir']),
             'r_twee':ldiff(data['twee']),
             'r_twfi':ldiff(data['twfi']),
             'r_sp500':ldiff(data['sp500'])}
             )

df1

# 選擇子樣本 (2000:01 - 2006:12)，放到 df1_sub
df1_sub=df1.iloc[60:144,:] # 2000:01 的 index = 60, 2006:12 的 index =143

df1_sub

# 列印敘述統計
df1_sub.describe().round(4)

df2_sub = df1_sub.iloc[:,1:] # 取出非日期標籤的欄位

# 方法一：用 statsmodels
# Testing for non-normality, p67
import statsmodels.stats.api as sms
test = sms.jarque_bera(df2_sub)
print(test)

# 將 test (array) 轉成 dataframe 
dfTest = pd.DataFrame(test)

dfTest

# 將 dfTest 的 列 index 名稱，改成 'Skew'、'Kurt'
dfTest = dfTest.rename(index={0:'JB',1:'p-value',2:'Skew',3:'Kurt'})
dfTest

# 計算超峰態 = Kurt-3
dfTest.loc[4] = dfTest.loc['Kurt']-3
# 將欄位名稱改成 'ExcsKurt'
dfTest = dfTest.rename(index={4:'ExcsKurt'})

dfTest

dfTest.round(4).T

# -----------------------------------------------------------
# 以下為進階 dataframe 表格合併之處理 (option)
# -----------------------------------------------------------

# 將敘述統計變成 dataframe
df1_sub_summary = df1_sub.describe()

# 將 df1_sub_summary 的欄位名稱，放在 dftest 中
dfTest.columns=df1_sub_summary.columns

# 欄名、欄位數要相同，pd.concat() 才能順利合併
df1_sub_summary = pd.concat([df1_sub_summary,dfTest])
df1_sub_summary.round(4).T
