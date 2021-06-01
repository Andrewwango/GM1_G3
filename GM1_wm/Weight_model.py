#!/usr/bin/env python
# coding: utf-8

# In[442]:


import numpy as np
import pandas as pd 
import datetime
import matplotlib.pyplot as plt
from datetime import timedelta
from helper_functions import *



vals1 = [1,10,30,60,100,105]

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
# sort out data format

# In[443]:
for it in range(5):
	for it1 in range(vals1[it],vals1[it+1]):
		vals= vals1[:it+1]
		print(vals)

		df = pd.read_excel('Nutrition-Summary-2021-01-01-to-2021-05-01.xls')
		#df1 = df[['Date','Calories']]
		dfc =  df.groupby('Date')['Calories'].sum().reset_index()
		dfc = dfc.loc[range(it1),:]
		print(dfc)

		dfw = pd.read_excel('Measurement-Summary-2021-01-01-to-2021-05-01.xlsx')
		#print(vals)
		dfw1 = dfw
		dfw = dfw.loc[vals, :]
		
		#dfm1 = pd.merge(dfw, dfc, how="outer", on=[ "Date"])
		
		
		#print(dfw)
		





		dfm = pd.merge(dfw, dfc, how="outer", on=[ "Date"])
		#print(dfm)
		dfm = dfm.sort_values(by="Date")
		dfm.to_excel('test.xlsx', index=False)

		#have formula
		BMR = 2000


		# In[444]:


		df5 = dfm[['Date','Calories']]
		#df.plot(x ='Date', y='Calories', kind = 'scatter')
		date = df5[['Date']].to_numpy()
		#print(date)
		cal = df5[['Calories']].to_numpy()
		#plt.scatter(date,cal )
		#plt.show()


		# In[445]:


		#print(np.shape(cal))
		cal = cal.flatten()
		cal_no_nan = cal[np.logical_not(np.isnan(cal))]

		cal1 = np.nan_to_num(cal, nan = np.mean(cal_no_nan))-BMR
		cal_w =np.cumsum(cal1)/7700
		#plt.scatter(date, cal_w)


		# In[446]:


		weight1 = dfm.sort_values(by="Date")

		weight = weight1[['Weight']].to_numpy().reshape(np.shape(cal_w))
		w2 = weight[np.logical_not(np.isnan(weight))]

		weight_n = weight - w2[0]*np.ones(weight.size)
		BMR_w = weight_n - cal_w

		dl = pd.Series(BMR_w).last_valid_index()
		#print(dl)
		#print(np.shape(date))

		#print(BMR_w)

		#plt.scatter(date,BMR_w)
		#plt.show()


		# In[447]:


		date_days = dfm[['Date']]

		dfm1 = pd.merge(dfw1, dfc, how="outer", on=[ "Date"])
		
		
		#print(dfw)
		rw = dfm1.sort_values(by="Date")
		rw = rw[["Weight"]]
		rw = rw.to_numpy()
		rw = rw.flatten()
		




		delta_df = date_days - date_days.iloc[0]

		delta_days = delta_df.to_numpy()/(8.64e+13)
		delta1= delta_days.flatten().astype(int)
		rw= rw[:delta1.size]

		#print(np.shape(BMR_w))

		indices = np.logical_not(np.logical_or(np.isnan(BMR_w), np.isnan(delta1)))
		BMR_w = BMR_w[indices]
		delta = delta1[indices]
		#print(np.shape(delta))




		#print(delta)
		delta.dtype


		# In[448]:




		x_lin = delta
		print(delta1)
		y_lin = BMR_w # loading the linear regression dataset into numpy arrays

		#print(np.shape(x_lin))
		#print(np.shape(y_lin))

		var_w = 0.01
		var_y = 0.01
		#https://pubmed.ncbi.nlm.nih.gov/24021734/

		phi = np.array([[x_ ** d for d in range(0, 2)] for x_ in x_lin]) # X instantiated more elegantly here

		pre_w = 1/var_w * np.eye(2) # prior covariance matrix to include in MAP solution


		S = np.linalg.inv((phi.T).dot(phi) / var_y + pre_w) # posterior distribution covariance matrix
		mu = S.dot(phi.T).dot(y_lin)/var_y # MAP weights to use in mean(y*)

		#print(mu)



		x_pred = delta1[dl:]
		#print(dl)
		X_pred = np.array([[x_ ** d for d in range(0, 2)] for x_ in x_pred])

		mu_pred = X_pred.dot(mu) # calculate mean(y*)
		stdev_pred = (np.sum(X_pred.dot(S) * X_pred, axis = 1) + var_y) ** 0.5  # calculate Var(y*)^0.5

		#add on cal weight
		stdev_f = (np.sum(X_pred.dot(S) * X_pred, axis = 1) + var_y) * (x_pred - x_pred[0])
		
		
		mu_predf = mu_pred + cal_w[dl:] 
		y_linf = w2 - w2[0]
		if it >= 3:

			y_linf[3] = -7.5

		rwd = rw - w2[0]
		off = y_linf[-1] - mu_predf[0]
		#off = 0
		#print(np.shape(x_lin))
		#print(np.shape(rwd))
		rwdp = pd.Series(rwd)


		plt.fill_between(x_pred, mu_predf + stdev_f + off, mu_predf - stdev_f +off, facecolor = 'grey', alpha = 0.5) # plot confidence intervals = +/- Var(y*)^0.5
		
		plt.scatter(x_lin, y_linf, marker = 'x', color = 'red') # plot data
		plt.plot(x_pred, mu_predf + off, color = 'black') # plot mean(y*)
		s = [0.1 for n in range(len(delta1))]
		#plt.scatter(delta1, rwdp.rolling(5).mean() ,marker = 'x', color = 'blue', s=s)
		beautify_plot({"title":"Bayesian regression predictive", "x":"Time/Days", "y": 'Weight Change/ Kg'})

		fig = matplotlib.pyplot.gcf()
		#fig.set_size_inches(18.5, 10.5)
		fig.set_dpi(100)
		plt.xlim(0,120)
		plt.ylim(-12,10)

		plt.savefig('books_read_%s_%d.png'%(it,it1))
		#plt.show()
		plt.close(fig)



# In[ ]:





# In[ ]:





# In[ ]:




