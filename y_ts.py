def diff(y):
	import numpy as np
	d_y = y-y.shift(1)
	return d_y
def ldiff(y):
	import numpy as np
	ld_y = np.log(y/y.shift(1))
	return ld_y
def tscorrel(y,lags=None):
	import pandas as pd
	import statsmodels.tsa.api as smt
	acf,q,pval=smt.acf(y,nlags=lags,fft=True,qstat=True)
	pacf=smt.acf(y,nlags=lags)
	ts_correl=pd.DataFrame({'acf':acf[1:],'pacf':pacf[1:],'Q':q,'p-val':pval}) 
	return ts_correl
def tsplot(y, lags=None, figsize=(10, 8)):
	import pandas as pd
	import numpy as np
	import seaborn as sns
	import matplotlib.pyplot as plt
	import statsmodels.tsa.api as smt

	fig = plt.figure(figsize=figsize)
	layout = (2, 2)
	ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
	acf_ax = plt.subplot2grid(layout, (1, 0))
	pacf_ax = plt.subplot2grid(layout, (1, 1))

	y.plot(ax=ts_ax)
	smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
	smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
	[ax.set_xlim(1.5) for ax in [acf_ax, pacf_ax]]
	sns.despine()
	plt.tight_layout()
	return ts_ax, acf_ax, pacf_ax
