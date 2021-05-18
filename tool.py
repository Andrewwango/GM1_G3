import numpy 
import pandas as pd 

def foodInfo(code):
	df = pd.read_excel ('Nutritional_info.xlsx')
	return df.loc[df['Food code'] == code]
	#info = df.loc['code']
	#return info
	

print(foodInfo(1))