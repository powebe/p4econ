### 範例1.2.1-1.2.2 計算台股指數月資料之簡單淨報酬率、連續複利報酬
#1. 安裝所需套件
#2. 定義自訂函數：「取對數再一階差分」 ldiff()
#3. 從雲端抓示範資料檔
#4. 抓出台股指數 twi，並計算簡單淨報酬率、連續複利報酬

!pip install yfinance
!pip install numpy
!pip install pandas
!pip install --upgrade xlrd
import yfinance as yf
import numpy as np
import pandas as pd

# 本課程常用的「自訂函數」
def ldiff(x):
  x_diff = 100*np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff

# 從雲端抓示範資料檔
url = 'http://gretlcycu.files.wordpress.com/2022/05/fe-all.xls'
sheet_name = 'FE-ex1'
data = pd.read_excel(url,sheet_name)
print(data.head())

# 抓出台股指數 twi
twi = data['twi']

# 計算簡單淨報酬
R_tw = twi/twi.shift(1)-1

# 計算連續複利報酬
r_tw = np.log(twi/twi.shift(1))

# 列印出數據
print(twi)
print(R_tw)
print(r_tw)

# 將 twi 和 r_tw 合併成 dataframe
df2 = pd.DataFrame({'twi':twi,'r_twi':r_tw,'R_tw':R_tw})

# 將缺漏值去掉、並列印出檢示
# df2 = df2.dropna()
df2

# 列印敘述統計(全樣本)
df2.describe()
