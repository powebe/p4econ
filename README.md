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
* \**kwargs:加上這關鍵字參數 robust='HAC'，可以改用穩健標準誤估計 OLS
### 回傳值
* 與 statsmodels.api 的 .fit() 回傳值相同
### 輸出
* 迴歸結果 .summary(2)
* White test
* ARCH Q2 檢定
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
