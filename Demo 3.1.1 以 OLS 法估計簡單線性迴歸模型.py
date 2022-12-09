# Demo 3.1.1 以 OLS 法估計簡單線性迴歸模型
!pip install yfinance
!pip install numpy
!pip install pandas

import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.tsa.api as smt

# 本課程常用的「自訂函數」
def ldiff(x):
  # =====取對數再一階差分=====
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff

def Q_test(_Y):
  # =====Q 檢定=====
  acf, q, pval = smt.acf(_Y, nlags=20, qstat=True,fft=False)
  pacf=smt.acf(_Y,nlags=20)
  ts_correl=pd.DataFrame({'LAG':range(1,21),'acf':acf[1:],'pacf':pacf[1:],'Q':q,'p-val':pval},index=range(1,21))
  print(_Y.name, '的自我相關函數 (ACF)')
  print(ts_correl.round(4)) 

# 從讀放在雲端的 Excel 檔
url = 'https://github.com/powebe/p4econ/raw/main/fe-all.xlsx'
sheet_name = 'FE-ex1'
data = pd.read_excel(url,sheet_name)

# 計算連續複利報酬, 放在 df1
df1 = pd.DataFrame({'obs':data['obs'],
             'r_twi':ldiff(data['twi']),
             'r_twpl':ldiff(data['twpl']),
             'r_twir':ldiff(data['twir']),
             'r_twee':ldiff(data['twee']),
             'r_twfi':ldiff(data['twfi']),
             'r_sp500':ldiff(data['sp500'])}
             )

# 選擇子樣本 (2000:01 - 2006:12)，放到 df1_sub
df1_sub=df1.iloc[60:144,:] # 2000:01 的 index = 60, 2006:12 的 index =143

import statsmodels.formula.api as smf
# 設定迴歸方程式：r_twee = b1 + b2*r_twi
# 以字串形式放在 eq 文字變數中
eq = 'r_twee~r_twi'

model1=smf.ols(eq,df1_sub)
result1=model1.fit()

# 印出迴歸估計結果
print(result1.summary())
