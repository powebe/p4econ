# p4econ

# y_ts.py 套件的使用

## 下載本書自訂套件
在 colab 中下載我寫的 y_ts.py 套件
```
!wget 'https://github.com/powebe/p4econ/raw/main/y_ts.py'
```

## 啟用本書自訂套件中的市場模型函數 mktm
```
from y_ts import mktm
```
## 市場模型(market model) mktm() 函數參數說明
mktm(y,x,startobs,endobs,nlag,robust='HAC')

### 參數
* y: 個股報酬率
* x: 大盤報酬率
* startobs: 子樣本開始 index 位置(列)
* endobs: 子樣本結束 index 位置(列)
* nlag: ARCH $Q^2$ 檢定、自我相關 Q 檢定的落後期
* \**kwargs:加上這關鍵字參數 robust='HAC'，可以改用穩健標準誤估計 OLS
### 回傳值
* 與 statsmodels.api 的 .fit() 回傳值相同
### 輸出
* 迴歸結果 .summary(2)
* White test
* ARCH $Q^2$ 檢定
* 自我相關 Q 檢定
* Jarque-Bera 檢定

## 使用範例 (google colab)
```
import pandas as pd
# 下載本書自訂套件
!wget 'https://github.com/powebe/p4econ/raw/main/y_ts.py'
# 啟用本書自訂套件中的函數 mktm
from y_ts import mktm
nStart = 0
nEnd = len(data)-1
result1 = mktm(data['Ct'],data['Yt'],nStart,nEnd,4)
```
## 範例執行結果
```
樣本期間：0 至 34
                 Results: Ordinary least squares
=================================================================
Model:              OLS              Adj. R-squared:     0.996   
Dependent Variable: Ct               AIC:                466.6051
Date:               2022-12-29 04:08 BIC:                469.7158
No. Observations:   35               Log-Likelihood:     -231.30 
Df Model:           1                F-statistic:        8174.   
Df Residuals:       33               Prob (F-statistic): 4.09e-41
R-squared:          0.996            Scale:              34141.  
------------------------------------------------------------------
           Coef.    Std.Err.     t     P>|t|     [0.025    0.975] 
------------------------------------------------------------------
const    -309.3353  143.5477  -2.1549  0.0386  -601.3853  -17.2853
Yt          0.9263    0.0102  90.4086  0.0000     0.9055    0.9472
-----------------------------------------------------------------
Omnibus:               0.972        Durbin-Watson:          0.599
Prob(Omnibus):         0.615        Jarque-Bera (JB):       0.972
Skew:                  -0.260       Prob(JB):               0.615
Kurtosis:              2.371        Condition No.:          64392
=================================================================
* The condition number is large (6e+04). This might indicate
strong multicollinearity or other numerical problems.



                        White-Test
Test Statistic              4.2758
Test Statistic p-value      0.1179


usq 殘差平方 的自我相關函數 (ACF)
   LAG     acf    pacf       Q   p-val
1    1  0.1512  0.1512  0.8703  0.3509
2    2 -0.0040 -0.0040  0.8710  0.6470
3    3  0.0887  0.0887  1.1895  0.7555
4    4 -0.0818 -0.0818  1.4690  0.8321


u 殘差 的自我相關函數 (ACF)
   LAG     acf    pacf        Q   p-val
1    1  0.6234  0.6234  14.8016  0.0001
2    2  0.4530  0.4530  22.8548  0.0000
3    3  0.3384  0.3384  27.4880  0.0000
4    4  0.1778  0.1778  28.8091  0.0000


                   JB-stat.  JB-adj
Jarque-Bera          0.9720  0.9165
JB right-tail pv.    0.6151  0.6324
Skew                -0.2600 -0.2600
Kurtosis             2.3706  2.3706

```
