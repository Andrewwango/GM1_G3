import numpy 
import pandas as pd 
import datetime
import matplotlib as plt
import ApiTest




def calInfo(code, wieght):
	df = pd.read_excel ('Nutritional_info.xlsx')
	info= df.loc[df['Food code'] == code]
	cal = info.iloc[0,-1]
	return cal*wieght 


class Patient:
	def __init__(self, name, age):
		self.name = name 
		self.age = age
		self.info = pd.DataFrame()


	def getInfo(self):
		df = pd.read_excel ('Dummy_L2S2.xlsx')
		#print(df)
		self.info = df
		#print(self.info)
		#should be api stuff to get info from L2S2 but now it is just demo with excel

	#give date time as %d-%m-%Y %H:%M:%S string
	def addMeal(self, code, weight, datetime):
		dtime = pd.to_datetime(datetime,format="%d-%m-%Y %H:%M:%S")
		new_row = pd.Series( [datetime, code, weight,calInfo(code,weight)], index=self.info.columns )
		df3 = self.info.append(new_row, ignore_index=True)
		#print(df3)
		df3.to_excel('Dummy_L2S2.xlsx', index=False)


		
		return

		#upload meal onto L2S2

	def analysis(self):
		#do some analysis
		return
	def printMeals(self):
		return



# p1 = Patient("Rodger", 36)
# p1.getInfo()
# datetime ='22-03-2018 15:16:46'
# p1.addMeal(1,30,datetime)





