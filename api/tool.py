import numpy 
import pandas as pd 
import datetime
import matplotlib as plt
from .ApiTest import *



def calInfo(code, wieght):
	df = pd.read_excel ('Nutritional_info.xlsx')
	info= df.loc[df['Food code'] == code]
	cal = info.iloc[0,-1]
	return cal*wieght 


class Patient:
	def __init__(self, name, age, tid):
		self.name = name 
		self.age = age
		self.info = pd.DataFrame()
		self.tid = tid

	def sendAl(self, TorF):
		values = [
       # {'name': 'Date1', 'value': to_long_time(datetime.now())},
    	#{'id': 7, 'value':  to_long_time(dtime)},
		
        #{'id': 8, 'value': ''  },
        {'id': 6, 'value': TorF}
       

       # {'name': 'Chart1', 'value': 'somefile.json', 'attachments': [{'description': 'Some description', 'key': file_key, 'original_file_name': 'somefile.json', 'saved_date_time': to_long_time(datetime(2018, 3, 7))}]},
   		]	
   		
		#_key_plate_template_id = "5f422db9-3c0f-491f-8c88-1d6c55f1733a"

		test_plate_template_name = 'nevill_alarm_plate'
		template = template_read_active_full(test_plate_template_name)
	
		template_id = template["id"]
		#template_id = _key_plate_template_id
		data_create(self.tid, template_id, values)
		return



	def getInfo(self):
		df = pd.read_excel ('Dummy_L2S2.xlsx')
		#print(df)
		self.info = df
		#print(self.info)
		#should be api stuff to get info from L2S2 but now it is just demo with excel

	#give date time as %d-%m-%Y %H:%M:%S string
	def addMeal(self, code, dessert_w, main_w, datetime):
		#dtime = pd.to_datetime(datetime,format="%d-%m-%Y %H:%M:%S")
		# new_row = pd.Series( [datetime, code, weight,calInfo(code,weight)], index=self.info.columns )
		# df3 = self.info.append(new_row, ignore_index=True)
		# #print(df3)
		# df3.to_excel('Dummy_L2S2.xlsx', index=False)

		values = [
       # {'name': 'Date1', 'value': to_long_time(datetime.now())},
    	#{'id': 7, 'value':  to_long_time(dtime)},
		
        {'id': 16, 'value': str(dessert_w)  },
        {'id': 10, 'value': str(main_w)}
       

       # {'name': 'Chart1', 'value': 'somefile.json', 'attachments': [{'description': 'Some description', 'key': file_key, 'original_file_name': 'somefile.json', 'saved_date_time': to_long_time(datetime(2018, 3, 7))}]},
   		]	
   		
		#_key_plate_template_id = "5f422db9-3c0f-491f-8c88-1d6c55f1733a"

		test_plate_template_name = 'Measurement_Plate'
		template = template_read_active_full(test_plate_template_name)
	
		template_id = template["id"]
		#template_id = _key_plate_template_id
		data_create(self.tid, template_id, values)

		
		return

		#upload meal onto L2S2

	def analysis(self):
		#do some analysis
		return
	def printMeals(self):
		return



#p1 = Patient("Rodger", 38.00,33)
#p1.getInfo()
<<<<<<< HEAD
datetime ='22-03-2018 15:16:46'
#p1.addMeal(1,40,datetime)
p1.sendAl(True)
=======
#datetime ='22-03-2018 15:16:46'
#p1.addMeal(1,40,datetime)
#p1.sendAl(False)
>>>>>>> 13e526522510d46cbbb5bff082c66890fe83b73f



# template = template_read_active_full(test_plate_template_name)
# pprint(template)
# template_id = template["id"]
# template_id = _key_plate_template_id

# print(template_id)
# with open('/Users/admin/Documents/GM1_G3/api/somefile.json', 'rb') as content_file:
#    content = content_file.read()

#    file_key = file_create(content, 'image/png')

#    dob = datetime(1988, 1, 22, 12, 34)

#    print(f'File key = {file_key}  DOB={dob} ({to_long_time(dob)})  template_name={test_plate_template_name}')


# data_create(33, template_id, values)
# data_read_newest(33, template_id, "")


