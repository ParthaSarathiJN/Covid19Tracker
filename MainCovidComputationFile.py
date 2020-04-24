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

# Change CountryName variable to the country you want.
CountryName = 'India'

	# 1 ----> -------------------------------------------------------------------------------#



LinksOfListOpen = open('LinksOfList.txt', 'w')

mainList = []
temporaryList = []


URL = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


for link in soup.find_all('a'):
    mainList.append(link.get('href')) 


for hrefs in mainList:
	
	if "csse_covid_19_data/csse_covid_19_daily_reports" in hrefs and ".csv" in hrefs:
		temporaryList.append(hrefs)

mainList = [] # mainList to clear list


for partialLink in temporaryList:

	added_raw = "https://raw.githubusercontent.com" + partialLink
	removed_blob = added_raw.replace('/blob', "")
	mainList.append(removed_blob)

for file in mainList:

	LinksOfListOpen.write(str(file + "\n"))


LinksOfListOpen.close()



	# 2 ----> -------------------------------------------------------------------------------------#



f = open('LinksOfList.txt', 'r')
urls = f.read().splitlines()


global urlStrippedForPrint

def download_url(url):
	global urlStrippedForPrint
	urlStrippedForPrint = url.lstrip('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/').rstrip('.csv')
	print(f'Downloading: {urlStrippedForPrint}.csv')
	file_name_start_pos = url.rfind("/") + 1
	file_name = url[file_name_start_pos:]

	r = requests.get(url, stream=True)
	if r.status_code == requests.codes.ok:
		with open(file_name, 'wb') as f:
			for data in r:
				f.write(data)
	return url


results = ThreadPool(8).imap_unordered(download_url, urls)


for r in results:
	pass
	# If  you want to show which one is currently being downloaded uncomment the next line
	#print(f'{urlStrippedForPrint}.csv')
	

f.close()

print('All the latest csv files have been downloaded!')



	# 3A  ----> -----------------------------------------------------------------------------------#



fileNameCsvJson = open('FileNamesWithCsv.json', 'w')


for file in glob.glob('*2020.csv'):

	fileNameCsvJson.write(str((file + "\n")))

fileNameCsvJson.close()



	# 3B ---> 



with open('FileNamesWithCsv.json', 'r+') as file:
	fileList = [line.rstrip('\n') for line in file]
	#print(fileList)
	jsonDumpsFileList = (json.dumps(fileList)) 

	file.seek(0) # Goes back to the start after keeping the correct list in memory

	file.write(jsonDumpsFileList) #Prints the correct list in the specified File



	# 4 ----> ----------------------------------------------------------------------------------------#



lineLast_Update = 58 # Change 58 with the first appearance of Last_Update

with open('FileNamesWithCsv.json','r') as jsonFile:
	jsonFileActiveNames = json.load(jsonFile)

	for files in range(lineLast_Update,len(jsonFileActiveNames)): # lineLastUpdate is the line of Last_Update App

		for line in fileinput.input(jsonFileActiveNames[files], inplace=True):

			if fileinput.isfirstline(): #Changes the first line to the following names
				print('FIPS,Admin2,Province_State,Country_Region,Last Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key')
			else:
				print(line)


		df = pd.read_csv(jsonFileActiveNames[files])
		df.to_csv(jsonFileActiveNames[files], index=False)



	# 5A ----> -------------------------------------------------------------------------------------------#



dateOfDatesJsonHolderJson = open('DatesOfAllDatesJsonHolder.json', 'w')

for file in glob.glob('*2020.csv'):

	file = file.rstrip('.csv')
	dateOfDatesJsonHolderJson.write(str(file + "\n")) 

dateOfDatesJsonHolderJson.close()



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
	dateFromDateList = -1 # Change to -1 if the starting date is from the first date


	for files in activeNamesJsonFiles:
		dateFromDateList += 1		# Needed to go through the datelistjson one by one to append to the Date in result
		

		with open(files, 'r') as activeFile:
			activeFile1 = csv.DictReader(activeFile)


			for line in activeFile1:

				if 'Country/Region' in line:
					if line['Country/Region'] == CountryName:
						correct_order_list = line
						break

					elif line['Country/Region'] != CountryName:		# Checks if India is in the list, if not adds 0 to all list values
						correct_order_list = {'Last Update': 'x', 'Confirmed': '0', 'Deaths': '0', 'Recovered': '0', 'Active': '0'}

				elif 'Country_Region' in line:
					if line['Country_Region'] == CountryName:
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


				# Use if you want to remove the rows with ,,, values ie when removing the values with 1-3 cases
				# Else comment out the rest of the lines from 277 to 279. 

			noValueDeleter = ['Confirmed']

			with open('Covid19Result.csv', 'a+', newline='') as writeFile:
				fieldnames = ['Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Active']
				
				csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)


					# Takes out the ROWs with 0,1,2,3 in them and replaces with empty('') values.
					# If you want to filter out the days with set amount of cases, add the number and they'll be ignored.
					# And uncomment the lines 282 to 284.

				#for noValue in noValueDeleter:
				#	if resultList[noValue] == '0' or resultList[noValue] == '1' or resultList[noValue] == '2' or resultList[noValue] == '3':
				#		resultList.clear()


				csv_writer.writerow(resultList)

			#print(resultList) # Shows the result which is getting appended to csv file
			#print(len(resultList)) # Shows the number of colums in the CovidResult

jsonFile.close()


	# Takes out all the empty('') values if 0-3 cases filtered out and adds x.0 at the end
df = pd.read_csv("Covid19Result.csv")
##checking the number of empty rows in th csv file
#print (df.isnull().sum())
##Droping the empty rows
modifiedDF = df.dropna()
##Saving it to the csv file 
modifiedDF.to_csv('Covid19Result.csv',index=False)



	# 7 ----> MatPlot code below--------------------------------------------------------------------------#



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

ax.set_title(f'Covid19 in {CountryName}')
ax.set_xlabel('Number of People')
ax.set_yticks(x)
ax.set_yticklabels(labels)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=4)


fig.tight_layout()

plt.show()

