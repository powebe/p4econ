def Q_test(_Y,_nlag):
  import statsmodels.tsa.api as smt
  print('\n')
  # =====以下不用改=====
  acf, q, pval = smt.acf(_Y, nlags=_nlag, qstat=True,fft=False)
  pacf=smt.acf(_Y,nlags=_nlag)
  print(_Y.name, '的自我相關函數 (ACF)')
  '''
  print(len(acf[1:]))
  print(len(pacf[1:]))
  print(len(q))
  print(len(pval))
  '''
  _correl=pd.DataFrame({'LAG':range(1,_nlag+1),'acf':acf[1:],'pacf':pacf[1:],'Q':q,'p-val':pval},index=range(1,_nlag+1))
  print(_correl.round(4))

def mktm(_r_y, _r_x, _startobs, _endobs, _nlag):
  import numpy as np
  import pandas as pd
  import statsmodels.tsa.api as smt
  import scipy.stats as scs
  '''
  MarketM(): Market Model 估計和殘差檢定
  版本：v01
  日期：2022.7.9
  TBD：
      1. _r_x 改成三因子，允許 _r_x as pd
  '''
  # print(_r_x.name)
  _r_x_name = _r_x.name
  # 更改子樣本範圍為 2000-2006年
  _nobs = len(_r_y)
  # df_const=pd.DataFrame({'const':1},index = range(1,_nobs+1))
  df_r_yx = pd.DataFrame({'_r_y':_r_y, '_r_x':_r_x})
  df_r_yx['const']=1
  #print(df_r_yx)

# 更改子樣本範圍為 2000-2006年
  _df_sub=df_r_yx.iloc[_startobs:_endobs,:] # 往前移
  _y = _df_sub['_r_y']
  _x = pd.DataFrame(_df_sub['_r_x'])
#  print(_df_sub)
  # 在 x 這個 pd 中加入一行常數 1
  _x['const']=1
  # 改變 const 的順序
  _x=_x[['const','_r_x']]
  # 改變 _r_x 的名稱
  _x.columns=['const',_r_x_name]

#fit regression model
  import statsmodels.api as sm
  _y.name = _r_y.name
  model = sm.OLS(_y, _x).fit()
  # print(model)
  print(model.summary())

  # 從 model 中取得殘差平方 usq，殘差 u
  usq = model.resid**2
  usq.name = "usq 殘差平方"
  u = model.resid
  u.name = "u 殘差"

  import statsmodels.stats.diagnostic as ssd

# 定義White's test 輸出欄名稱 
  rname = ['Test Statistic', 'Test Statistic p-value', 'F-Statistic', 'F-Test p-value']
# 進行 White's test
  White = pd.DataFrame(ssd.het_white(model.resid,  model.model.exog), index=rname)
  White.columns = ['White-Test']
  print('\n\n')
  print(White[:2].round(4)) #只印前兩個 row
# 進行 Q2 檢定
  Q_test(usq,_nlag)
# 進行 Q 檢定
  Q_test(u,_nlag)
# Testing for non-normality
  import statsmodels.stats.api as sms
  import scipy.stats as scs
  rname=['Jarque-Bera', 'JB two-tail pv.', 'Skew', 'Kurtosis']
  _JB = pd.DataFrame(sms.jarque_bera(u), index=rname)
  _JB.columns = ['JB-stat.']
  _JB['JB-adj'] = [sms.jarque_bera(model.resid)[0]/nobs*dof,scs.chi.cdf(sms.jarque_bera(model.resid)[0]/nobs*dof,2),'','']
  print('\n')
  print(_JB)
  print('\n\n')
