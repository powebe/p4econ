# Demo 3.2.1 迴歸模型殘差同質性檢定 (White test)
!pip install yfinance
!pip install numpy
!pip install pandas
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.tsa.api as smt

def ldiff(x):
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff
def Q_test(_Y,_nlag):
  # =====Q 檢定=====
  acf, q, pval = smt.acf(_Y, nlags=_nlag, qstat=True,fft=False)
  pacf=smt.acf(_Y,nlags=_nlag)
  ts_correl=pd.DataFrame({'LAG':range(1,_nlag+1),'acf':acf[1:],'pacf':pacf[1:],'Q':q,'p-val':pval},index=range(1,21))
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

# White 檢定方法一：自行手動產生檢定
# 產生迴歸模型的殘差 u
u = result1.resid
usq = u**2
sq_r_twi = df1_sub['r_twi']**2
print(sq_r_twi)

# White 檢定的輔助迴歸，放在 eq2, model2
import statsmodels.formula.api as smf
# 設定輔助迴歸方程式：usq = b1 + b2*r_twi+b3*sq_r_twi
# 以字串形式放在 eq 文字變數中
eq2 = 'usq~r_twi+sq_r_twi'

model2=smf.ols(eq2,df1_sub)
result2=model2.fit()

# 印出迴歸估計結果
print(result2.summary())

# 計算 White 統計值
T = result2.nobs
R2 = result2.rsquared
T*R2

# White 檢定方法二：利用 ssd 子套件
import statsmodels.stats.diagnostic as ssd
ssd.het_white(result1.resid, result1.model.exog)

# White 檢定方法二：利用 ssd 子套件+格式化輸出
import statsmodels.stats.diagnostic as ssd

# 定義White's test 輸出欄名稱 
rname = ['Test Statistic', 'Test Statistic p-value', 'F-Statistic', 'F-Test p-value']

# 進行 White's test
White = pd.DataFrame(ssd.het_white(result1.resid, result1.model.exog), index=rname)
White.columns = ['White-Test']
print(White[:2].round(4)) #只印前兩個 row

# 範例 3.2.2 殘差自我相關異質變異檢定 (Q2 test)
# 產生殘差，再取平方 (# 只要改等號後面的變數 result1)
usq = result1.resid**2
# 方法一：利用 ssd 子套件
ssd.acorr_ljungbox(usq)

# 方法二：使用老師撰寫的自訂函數
# Q_test(x, _nlag) 的參數填寫
# 進行 Q2 檢定
Q_test(usq,20)

# 範例 3.2.３ 自我相關Q檢定 (Q test)
# 產生殘差
# 進行 Q 檢定 # Q_test(x, _nlag) 的參數填寫
# result1
u = result1.resid
Q_test(u,20)

## 範例 3.2.4 殘差是否為常態分配之檢定 (JB test)
# 方法一：自行計算
# 更名引用 scipy.stats 來使用 .skew() 抓偏態係數和 .kurtosis() 抓超峰態係數
import scipy.stats as scs
u = result1.resid
SK = scs.skew(u)
KT = scs.kurtosis(u)+3
# 從 result1 抓樣本數
nobs=result1.nobs # T = 84
# 從 result1 抓自由度 degree of freedom (dof) = 84-2 (待估參數個數 n=2)
dof=result1.df_resid
JB_adj = (dof)/6*(SK**2+(1/4)*(KT-3)**2)
print(SK,KT,JB_adj)

# 未修正自由度
(84)/6*(SK**2+(1/4)*(KT-3)**2)

# 查卡方分配的 pv
jb = 1.5131
scs.chi2.cdf(jb,2) # cdf 累積機率密度函數 = 左尾
1- scs.chi2.cdf(jb,2) # 右尾機率

jb = 1.4771
1- scs.chi2.cdf(jb,2) # 右尾機率

# 方法二：用 sms 子套件
import statsmodels.stats.api as sms
u = result1.resid
sms.jarque_bera(u)

# 方法二：用 sms 子套件+格式化輸出 
import statsmodels.stats.api as sms
import scipy.stats as scs
u = result1.resid
rname=['Jarque-Bera', 'JB right-tail pv.', 'Skew', 'Kurtosis']
JB = pd.DataFrame(sms.jarque_bera(u), index=rname)
# print("Dataframe columns:", JB.columns)
JB.columns = ['JB-stat.']
nobs=result1.nobs # T = 84
# 從 result1 抓自由度 degree of freedom (dof) = 84-2 (待估參數個數 n=2)
dof=result1.df_resid
JB_adj = sms.jarque_bera(u)[0]/nobs*dof
JB_adj_pv = 1-scs.chi2.cdf(sms.jarque_bera(u)[0]/nobs*dof,2)
JB['JB-adj'] = pd.DataFrame((JB_adj,JB_adj_pv,SK,KT),index=rname)
print(JB.round(4))
