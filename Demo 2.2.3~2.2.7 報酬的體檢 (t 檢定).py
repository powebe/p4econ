# Demo 2.2.3~2.2.7 報酬的體檢
!pip install yfinance
!pip install numpy
!pip install pandas
import yfinance as yf
import numpy as np
import pandas as pd

def ldiff(x):
  x_diff = np.log(x/x.shift(1))
  x_diff=x_diff.dropna()
  return x_diff

# Pearson's correlation coefficient follows Student's t-distribution with degrees of freedom n − 2. For determining the critical values for r the inverse function is needed: 
# (see [wiki](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#Testing_using_Student's_t-distribution)) 
# <img src="https://latex.codecogs.com/svg.image?r=\frac{t}{\sqrt{n-2&plus;t^2}}" title="https://latex.codecogs.com/svg.image?r=\frac{t}{\sqrt{n-2+t^2}}" />

def pearson_cv(_alpha,_n):
    import scipy.stats as scs
    # 老師寫的自訂函數，計算 pearson 相關係數檢定臨界值
    # 參數1：顯著水準; 參數2: 樣本數
    _dof = _n-2
    _t =scs.t.ppf(q=(1-_alpha/2),df=_dof)
    _cv = _t/(_dof+_t**2)**0.5
    print('===Pearson 相關係數臨界值===')
    print(f'{_alpha*100:.0f}% critical value (two-tailed) = {_cv:.4f}, for n = {_n:.0f}')
    return _cv

# 從讀放在雲端的 Excel 檔
url = 'https://github.com/powebe/p4econ/raw/main/fe-all.xlsx'
sheet_name = 'FE-ex1'
data = pd.read_excel(url,sheet_name)

# 計算連續複利報酬
df1 = pd.DataFrame({'r_tw':ldiff(data['twi']),
             'r_twpl':ldiff(data['twpl']),
             'r_twir':ldiff(data['twir']),
             'r_twee':ldiff(data['twee']),
             'r_twfi':ldiff(data['twfi']),
             'r_sp500':ldiff(data['sp500'])}
             )

# 更改子樣本範圍為 2000-2006年
df1_sub=df1.iloc[59:143,:] # 往前移
# df1_sub.describe()

# Demo 2.2.3 常態母體樣本均數之檢定(t 檢定)
import scipy.stats as scs
dat1 = df1_sub['r_tw']
mean = 0.0017
t_test=scs.ttest_1samp(dat1, mean)

print('===常態母體樣本均數檢定===')
print('t-值 = %.4f, ' % t_test.statistic, 'p-value = %.4f' % t_test.pvalue)

# Demo 2.2.4 兩常態母體樣本均數差之檢定(t 檢定)
dat1 = df1_sub['r_twee']
dat2 = df1_sub['r_twpl']
t_test = scs.ttest_ind(dat1, dat2, equal_var = True)
print('===兩獨立常態母體樣本均數檢定===')
print('t-值 = %.4f, ' % t_test.statistic, 'p-value = %.4f' % t_test.pvalue)

# Demo 2.2.5 不獨立常態母體樣本均數之檢定(t 檢定)
dat1 = df1_sub['r_twee']
dat2 = df1_sub['r_twpl']
_di = dat1 - dat2
t_test = scs.pearsonr(dat1, dat2)
t_test
print('===相關性檢定===')
print('t-值 = %.4f, ' % t_test[0].round(4), 'p-value = %.4f' % t_test[1].round(4))

mean = 0
t_test=scs.ttest_1samp(_di, mean)
print('===不獨立常態母體樣本均數檢定===')
print('t-值 = %.4f, ' % t_test.statistic, 'p-value = %.4f' % t_test.pvalue)

# Demo 2.2.6 報酬率變數之相關係數矩陣與檢定
# Pearson 相關係數
df1_sub.corr().round(4) 

# 老師寫的自訂函數，計算 pearson 相關係數檢定臨界值
# 參數1：顯著水準; 參數2: 樣本數
cv = pearson_cv(0.05,84)

# Demo 2.2.7 金融類股和傳產類股的風險相同嗎?
dat1 = df1_sub['r_twpl']
dat2 = df1_sub['r_twfi']

var1 = dat1.var()
var2 = dat2.var()
f_stat = var1 / var2
dof1 = len(dat1) - 1
dof2 = len(dat2) - 1
# F 分配的
f_cdf = scs.f.cdf(f_stat, dof1, dof2)
f_pv = 1-f_cdf
f_pv_2tailed = f_pv*2
print('===二常態母體變異數相等 F 檢定===')
print('F-值 = %.4f' % f_stat)
print('Two-tailed p-value = %.4f' % f_pv_2tailed)
print('(One-tailed p-value = %.4f)' % f_pv)


var1,var2,f_stat,dof1,dof2

# 使用 f-字串 語法來輸出
print('===二常態母體變異數相等 F 檢定===')
print(f'F({dof1},{dof2})-值 = {f_stat:.4f}' )
print(f'two-tailed p-value =  {f_pv*2:.4f}' )
print(f'(one-tailed p-value =  {f_pv:.4f})' )

# 另一種變異數檢定：Bartlett 變異數相同檢定
scs.bartlett(dat1, dat2)
