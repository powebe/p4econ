# Demo 4.1.1 台灣鋼鐵類股報酬市場模型係數檢定
!pip install yfinance
!pip install numpy
!pip install pandas
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.tsa.api as smt
import statsmodels.stats.api as sms
import scipy.stats as scs

def ldiff(x):
  import numpy as np
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff
def Q_test(_Y,_nlag):
  # 函數用法：_Y 欲檢定變數; _nlag 落後期數
  import statsmodels.tsa.api as smt
  # =====Q 檢定=====
  acf, q, pval = smt.acf(_Y, nlags=_nlag, qstat=True,fft=False)
  pacf=smt.acf(_Y,nlags=_nlag)
  ts_correl=pd.DataFrame({'LAG':range(1,_nlag+1),'acf':acf[1:],'pacf':pacf[1:], 
                          'Q':q,'p-val':pval},index=range(1,_nlag+1))
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
# 設定迴歸方程式：r_twir = b1 + b2*r_twi
# 以字串形式放在 eq 文字變數中
eq = 'r_twir~r_twi'

model1=smf.ols(eq,df1_sub)
result1=model1.fit()

# 印出迴歸估計結果
print(result1.summary2())

# --- 抓係數，將 result1.params[0],result1.params[1] 中的數據，
# 分別放在 b1, b2 當中
b1, b2 = result1.params[0],result1.params[1]
b1_stderr, b2_stderr = result1.bse[0],result1.bse[1]

# 取得模型殘差的自由度
dof = result1.df_resid

# H0: b2 = 1 (是否為保守型)
mean =1

# HA: b2>1 (右尾)
import scipy.stats as scs
# scipy.stats.t.cdf(abs(t_score), df=degree_of_freedom)
t_H0_b2_pv = 1-scs.t.cdf(abs((b2-mean)/b2_stderr), df=dof)

print('===迴歸係數檢定===')
print('H0: b2 = 1')
print('t-值 = %.4f, ' % ((b2-mean)/b2_stderr), 
      '雙尾 p-value = %.4f' % (t_H0_b2_pv*2))
print('t-值 = %.4f, ' % ((b2-mean)/b2_stderr), 
      '單尾 p-value = %.4f' % t_H0_b2_pv)
