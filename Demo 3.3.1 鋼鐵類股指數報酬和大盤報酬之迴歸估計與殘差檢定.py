# Demo 3.3.1 鋼鐵類股指數報酬和大盤報酬之迴歸估計與殘差檢定
!pip install yfinance
!pip install numpy
!pip install pandas
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.tsa.api as smt

def ldiff(x):
  import numpy as np
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff
def Q_test(_Y,_nlag):
  import statsmodels.tsa.api as smt
  # =====Q 檢定=====
  acf, q, pval = smt.acf(_Y, nlags=_nlag, qstat=True,fft=False)
  pacf=smt.acf(_Y,nlags=_nlag)
  ts_correl=pd.DataFrame({'LAG':range(1,_nlag+1),'acf':acf[1:],'pacf':pacf[1:],'Q':q,'p-val':pval},index=range(1,_nlag+1))
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

model=smf.ols(eq,df1_sub)
result=model.fit()

# 印出迴歸估計結果
print(result.summary())

# White 檢定方法二：利用 ssd 子套件+格式化輸出
import statsmodels.stats.diagnostic as ssd
# 定義White's test 輸出欄名稱 
rname = ['Test Statistic', 'Test Statistic p-value', 'F-Statistic', 'F-Test p-value']
# 進行 White's test
White = pd.DataFrame(ssd.het_white(result.resid, result.model.exog), index=rname)
White.columns = ['White-Test']
print(White[:2].round(4)) #只印前兩個 row

# 從 model 中取得殘差平方 usq，殘差 u
usq = result.resid**2
u = result.resid
# 取得樣本數
nobs = model.nobs
dof = model.df_resid

# 方法二：使用老師撰寫的自訂函數 Q_test()
# 進行 Q2 檢定
import statsmodels.tsa.api as smt
# 只要改等號後面的變數
Q_test(usq,16)


# 方法二：使用老師撰寫的自訂函數 Q_test()
# 進行 Q 檢定
import statsmodels.tsa.api as smt
Q_test(u,16)

$JB值=\frac{T-n}{6}\left ( SK^2 +\frac{1}{4}(KT-3)^2\right )～\chi_{(3)}^{2}$

# 方法二：用 sms 子套件+格式化輸出 
import statsmodels.stats.api as sms
import scipy.stats as scs
u = result.resid
SK = scs.skew(u)
KT = scs.kurtosis(u)+3
rname=['Jarque-Bera', 'JB right-tail pv.', 'Skewness', 'Kurtosis']
JB = pd.DataFrame(sms.jarque_bera(u), index=rname)
# print("Dataframe columns:", JB.columns)
JB.columns = ['JB-stat.']
nobs=result.nobs # T = 84
# 從 result1 抓自由度 degree of freedom (dof) = 84-2 (待估參數個數 n=2)
dof=result.df_resid
JB_adj = sms.jarque_bera(u)[0]/nobs*dof
JB_adj_pv = 1-scs.chi2.cdf(sms.jarque_bera(u)[0]/nobs*dof,2)
JB['JB-adj'] = pd.DataFrame((JB_adj,JB_adj_pv,SK,KT),index=rname)
print(JB.round(4))

# 以穩健標準誤估計迴歸模型
# OLS with Robust Standard Error
eq = 'r_twir~r_twi'

model0=smf.ols(eq,df1_sub)
# _maxlag as recommended by Stock and Watson (2003)
_maxlag = int(nobs**(1/3)*0.75)
result0=model0.fit(cov_type='HAC',cov_kwds={'maxlags':_maxlag})

# 印出迴歸估計結果
print(f'HAC standard errors, bandwidth {_maxlag} (bartlett kernel)')
print(result0.summary2())

# 下載本書自訂套件
!wget 'https://github.com/powebe/p4econ/raw/main/y_ts.py'
# 啟用本書自訂套件中的函數 ldiff、mktm
import y_ts as yts
from y_ts import mktm

# 使用穩健標準誤進行估計，新增參數 robust='HAC'
result1 = mktm(df1['r_twir'],df1['r_twi'],60,144,6,robust='HAC')
