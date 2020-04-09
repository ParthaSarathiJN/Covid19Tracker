from bs4 import BeautifulSoup
import requests
import csv
import json
from multiprocessing.pool import ThreadPool
import os
import glob
import fileinput
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import numpy as np


csvClear = "Covid19Result.csv"
# opening the file with w+ mode truncates the file
f = open(csvClear, "w+")
f.close()


	# 1 ----> -------------------------------------------------------------------------------#

	# 	This needs to be in another file because once it's run, it gets the file links but it can't automatically 
	# 		call each of the links in the next process. 
	#	So you need to run this file first then go for the file where all the links get printed. Then you should 
	#		manually copy them and place them in the urls variable in the next 2nd thing.

#LinksOfListOpen = open('LinksOfList.json', 'w')
#
#correct_list = []
#throwaway_list = []
#
#	#	Need to get the links from the CSSEGISand for latest updated data.
#URL = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
#page = requests.get(URL)
#
#soup = BeautifulSoup(page.content, 'html.parser')
#
#
#
#for link in soup.find_all('a'):
#    correct_list.append(link.get('href')) # Prints all the things with href in the page
#
#
#for i in correct_list:
#	
#	if "csse_covid_19_data/csse_covid_19_daily_reports" in i and ".csv" in i:
#		throwaway_list.append(i)
#
#correct_list = [] # New correct blank list
#
#for i in throwaway_list:
#
#	added_raw = "https://raw.githubusercontent.com" + i
#	removed_blob = added_raw.replace('/blob', "")
#	correct_list.append(removed_blob)
#
#for file in correct_list:
#
#	LinksOfListOpen.write(str(file + "\n"))
#
#
#LinksOfListOpen.close()
#
#
#
#with open('LinksOfList.json', 'r+') as file:
#	mylist = [line.rstrip('\n') for line in file]
#	#print(mylist)
#	temp = (json.dumps(mylist)) 
#
#	file.seek(0) # Goes back to the start after keeping the correct list in memory
#
#	file.write(temp) #Prints the correct list in the specified File



	# 2 ----> -------------------------------------------------------------------------------------#
	#	 This is the 2nd thing which is also in another file which is needed to be run alone wihtout the rest of the
	#		code below. 
	#	Copy the urls which get downloaded by running the above command in another file, and paste them in the urls 
	#		variable, and it should start downloading by itself, and if you re-run this same file, the .csv files gets 
	#		overwritten with newest data.


#def download_url(url):
#
#	print("Downloading: ", url)
#	file_name_start_pos = url.rfind("/") + 1
#	file_name = url[file_name_start_pos:]
#
#	r = requests.get(url, stream=True)
#	if r.status_code == requests.codes.ok:
#		with open(file_name, 'wb') as f:
#			for data in r:
#				f.write(data)
#	return url
#
#	# Paste the links that got downloaded in the urls below along with the square brackets.
#urls = ["https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-22-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-23-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-24-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-25-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-26-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-27-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-28-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-29-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-30-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-31-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-01-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-02-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-03-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-04-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-05-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-06-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-07-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-08-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-09-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-10-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-11-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-12-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-13-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-14-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-15-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-16-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-17-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-18-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-19-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-20-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-21-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-22-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-23-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-24-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-25-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-26-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-27-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-28-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-29-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-01-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-02-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-03-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-04-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-05-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-06-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-07-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-08-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-09-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-10-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-11-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-12-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-13-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-14-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-15-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-16-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-17-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-18-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-19-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-20-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-21-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-22-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-23-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-24-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-25-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-27-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-28-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-29-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-30-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-31-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-01-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-02-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-04-2020.csv", "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-05-2020.csv"]
#
#	# Increase the number to increase the simultaneous downloads 
#results = ThreadPool(5).imap_unordered(download_url, urls)
#
#
#for r in results:
#	print(r)



	# 3A  ----> -----------------------------------------------------------------------------------#
	#	From here om out you can run the whole code by itself after following the above 2 procedures.


fileNameCsvJson = open('FileNamesWithCsv.json', 'w')
os.chdir('Your/Path/Followed/With/Downloads/Of/CsvFiles/')


for file in glob.glob('*2020.csv'):

	fileNameCsvJson.write(str(('Your/Path/Followed/With/Downloads/Of/CsvFiles/' + file + "\n")))

fileNameCsvJson.close()
	#Needed to change the directory because I downloaded the files in another file so as not to cramp my actual working directory.
os.chdir('Your/Path/Followed/With/Back/To/Main/Working/Directory/')



	# 3B ---> 

	

with open('FileNamesWithCsv.json', 'r+') as file:
	fileList = [line.rstrip('\n') for line in file]
	#print(fileList)
	jsonDumpsFileList = (json.dumps(fileList)) 

	file.seek(0) # Goes back to the start after keeping the correct list in memory

	file.write(jsonDumpsFileList) #Prints the correct list in the specified File



	# 4 ----> ----------------------------------------------------------------------------------------#



lineLast_Update = 58 # Change the number as per the number of l

with open('FileNamesWithCsv.json','r') as jsonFile:
	jsonFileActiveNames = json.load(jsonFile)

	for files in range(lineLast_Update,len(jsonFileActiveNames)): # lineLastUpdate is the line of Last_Update App

		for line in fileinput.input(jsonFileActiveNames[files], inplace=True):

			if fileinput.isfirstline(): #Changes the first line to the following names
				print('FIPS,Admin2,Province_State,Country_Region,Last Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key')
			else:
				print(line)

		#New Line Added here

		df = pd.read_csv(jsonFileActiveNames[files])
		df.to_csv(jsonFileActiveNames[files], index=False)



	# 5A ----> -------------------------------------------------------------------------------------------#



dateOfDatesJsonHolderJson = open('DatesOfAllDatesJsonHolder.json', 'w')
os.chdir('Your/Path/Followed/With/Downloads/Of/CsvFiles/')

for file in glob.glob('*2020.csv'):

	file = file.rstrip('.csv')
	dateOfDatesJsonHolderJson.write(str(file + "\n")) 

dateOfDatesJsonHolderJson.close()

os.chdir('Your/Path/Followed/With/Back/To/Main/Working/Directory/')



	# 5B --->



with open('DatesOfAllDatesJsonHolder.json', 'r+') as file:
	dateList = [line.rstrip('\n') for line in file]
	#print(dateList)
	jsonDumpsDateList = (json.dumps(dateList)) 

	file.seek(0) # Goes back to the start after keeping the correct list in memory

	file.write(jsonDumpsDateList) #Prints the correct list in the specified File



	# 6 ----> ---------------------------------------------------------------------------------------#



headerList = ["Date", "Confirmed", "Deaths", "Recovered", "Active"] # Creates the header list in the result list which is actually needed

statsOpen = open('Covid19Result.csv', 'a+')
headerWriter = csv.writer(statsOpen)
headerWriter.writerow(i for i in headerList)
statsOpen.close()

jsonFile = open('DatesOfAllDatesJsonHolder.json', 'r')
dateJsonFile = json.load(jsonFile)


with open('FileNamesWithCsv.json','r') as jsonFile:
	activeNamesJsonFiles = json.load(jsonFile)
	dateFromDateList = -1 # Change to -1 if the start date is form the first date (n-1)


	for files in activeNamesJsonFiles:
		dateFromDateList += 1		# Needed to go through the datelistjson one by one to append to the Date in result
		

		with open(files, 'r') as activeFile:
			activeFile1 = csv.DictReader(activeFile)


			for line in activeFile1:

				if 'Country/Region' in line:
					if line['Country/Region'] == "India":
						correct_order_list = line
						break

					elif line['Country/Region'] != 'India':		# Checks if India is in the list, if not adds 0 to all list values
						correct_order_list = {'Last Update': 'x', 'Confirmed': '0', 'Deaths': '0', 'Recovered': '0', 'Active': '0'}

				elif 'Country_Region' in line:
					if line['Country_Region'] == 'India':
						correct_order_list = line


			takeoutList = ['Country/Region','ï»¿FIPS','Province/State','Country_Region','Province_State','ï»¿Province/State','Admin2','FIPS','Long_','Lat','Combined_Key','Latitude','Longitude']
			missingZeroList = ['Recovered','Deaths']


			def RemoveUseless(useless_items):


				for takeouts in takeoutList:

					if takeouts in correct_order_list:
						del correct_order_list[takeouts]


				for missing in missingZeroList:

					if correct_order_list[missing] == '':
						correct_order_list.update({missing:'0'})

				if 'Active' not in correct_order_list:
					active_number = int(correct_order_list.get('Confirmed')) - int(correct_order_list.get('Deaths')) - int(correct_order_list.get('Recovered'))
					correct_order_list.update({'Active': active_number})

				if 'Last Update' in correct_order_list:
					correct_order_list.update({'Last Update': dateJsonFile[dateFromDateList]})
					

				#print(correct_order_list)
				return correct_order_list


			resultList = RemoveUseless(correct_order_list)
			
			#Use if you want to remove the rows with ,,, values ie when removing the values with 1-3 cases
			noValueDeleter = ['Confirmed']			

			with open('Covid19Result.csv', 'a+', newline='') as writeFile:
				fieldnames = ['Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Active']
				
				csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)


					#Takes out the ROWs with 0,1,2,3 in them and replaces with empty('') values.	
				for noValue in noValueDeleter:
					if resultList[noValue] == '0' or resultList[noValue] == '1' or resultList[noValue] == '2' or resultList[noValue] == '3':
						resultList.clear()
						
						
				csv_writer.writerow(resultList)

			#print(resultList) # Shows the result which is getting appended to csv file
			#print(len(resultList)) # Shows the number of colums in the result == 5

jsonFile.close()


	# Takes out all the empty('') values if 0-3 cases filtered out and adds x.0 at the end
df = pd.read_csv("Covid19Result.csv")
##checking the number of empty rows in th csv file
print (df.isnull().sum())
##Droping the empty rows
modifiedDF = df.dropna()
##Saving it to the csv file 
modifiedDF.to_csv('Covid19Result.csv',index=False)




plt.style.use('seaborn')

ResultData = pd.read_csv('Covid19Result.csv')


labels = ResultData['Date'] #x-values


ResultDataConfirm = ResultData['Confirmed']
ResultDataDeath = ResultData['Deaths']
ResultDataRecover = ResultData['Recovered']
ResultDataAct = ResultData['Active']


x = np.arange(len(labels))
barWidth = 0.4


fig, ax = plt.subplots()


rects1 = ax.barh(x + barWidth / 2, ResultDataConfirm, barWidth, color='#204051', label='Confirmed')
rects2 = ax.barh(x - barWidth / 2, ResultDataAct, barWidth, color='#1eb2a6', label='Active')
rects3 = ax.barh(x + barWidth / 4, ResultDataRecover, barWidth, color='#ffb0cd', label='Recovered')
rects4 = ax.barh(x - barWidth / 4, ResultDataDeath, barWidth, color='#dd2c00', label='Deaths') #3b6978

ax.set_title('Covid19 in India')
ax.set_xlabel('Number of People')
ax.set_yticks(x)
ax.set_yticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=4)


fig.tight_layout()

plt.show()

