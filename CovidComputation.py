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
import time


# Change CountryName to desired country.
CountryName = 'India'

DaysToBeDisplayed = 20

startTime = time.time()

with open("Covid19Result.csv", "w+") as clearFile:		# opening file with w+ mode truncates file
	pass

print(f"Time for Pre-Execution == {time.time() - startTime} == \n")



	# 1 ----> -------------------------------------------------------------------------------------#



def BeautifulSoupFunc():

	with open('LinksOfList.txt', 'w') as LinksOfListOpen:

		findAllMainList = []
		partialLinkList = []


		URL = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
		page = requests.get(URL)

		soup = BeautifulSoup(page.content, 'html.parser')


		for findAllLink in soup.find_all('a'):
		    findAllMainList.append(findAllLink.get('href')) 


		for hrefs in findAllMainList:
			
			if "csse_covid_19_data/csse_covid_19_daily_reports" in hrefs and ".csv" in hrefs:
				partialLinkList.append(hrefs)

		findAllMainList = [] # findAllMainList to clear list


		for partialLink in partialLinkList:

			added_raw = "https://raw.githubusercontent.com" + partialLink
			removed_blob = added_raw.replace('/blob', "")
			findAllMainList.append(removed_blob)

		for findAllMainListFile in findAllMainList:

			LinksOfListOpen.write(str(findAllMainListFile + "\n"))


	#print(f"Time for 1 BSoup == {time.time() - startTime} == \n")



	# 2 ----> -------------------------------------------------------------------------------------#



def DownloadsCleanerFunc():

	CsvNameList = []			# date + Csv 
	CsvNeedToDownload = []		# full Link
	with open('LinksOfList.txt', 'r') as LinksOfListChecking:
		UrlsFromLinksOfList = LinksOfListChecking.read().splitlines()

		for IndividualUrls in UrlsFromLinksOfList:

			SingleUrlCsv = IndividualUrls.lstrip('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/')

			#print(SingleUrlCsv)

			if not os.path.isfile(SingleUrlCsv):

				#print(f"Will download {SingleUrlCsv}")
				CsvNameList.append(SingleUrlCsv)
				CsvNeedToDownload.append(IndividualUrls)

				#print(f"Csv that should be downloaded are: {CsvNeedToDownload}")

		if len(CsvNeedToDownload) > 0:

			with open('LinksOfCsvToBeDownloaded.txt', 'w') as SeperateLinksToDownload:

				for IndividualCsvNeeded in CsvNeedToDownload:

					SeperateLinksToDownload.write(str(IndividualCsvNeeded + '\n'))

		else:

			with open('LinksOfCsvToBeDownloaded.txt', 'w') as blankFile:
				blankFile.truncate()

	#print(f"Time for 2 Csv Checking == {time.time() - startTime}")



	# 3 ----> -------------------------------------------------------------------------------------#



def RequestsDownloadFunc():

	with open('LinksOfCsvToBeDownloaded.txt', 'r') as fileCsvRequestDownload:
		urls = fileCsvRequestDownload.read().splitlines()

		global urlStrippedForPrint

		def download_url(url):

			global urlStrippedForPrint
			urlStrippedForPrint = url.lstrip('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/').rstrip('.csv')
			
			print(f'Downloading: {urlStrippedForPrint}.csv')
			
			fileNameStartPos = url.rfind("/") + 1
			fileNameUrl = url[fileNameStartPos:]

			requestsGetter = requests.get(url, stream=True)
			if requestsGetter.status_code == requests.codes.ok:

				with open(fileNameUrl, 'wb') as f:

					for dataRequestGetter in requestsGetter:

						f.write(dataRequestGetter)
			return url

		resultsOfThreadpool = ThreadPool(8).imap_unordered(download_url, urls)


		for resultThreadpool in resultsOfThreadpool:
			pass


	print('All the latest files are downloaded!')

	#print(f"Time for 3 Download == {time.time() - startTime} == ")



	# 4 A  ----> ----------------------------------------------------------------------------------#



def CsvDateCreatorFunc():

	fileNameCsvJson = open('FileNamesWithCsv.json', 'w')
	dateOfDatesJsonHolderJson = open('DatesOfAllDatesJsonHolder.json', 'w')


	for file in glob.glob('*2020.csv'):

		fileNameCsvJson.write(str((file + "\n")))
		
		file = file.rstrip('.csv')
		dateOfDatesJsonHolderJson.write(str(file + "\n")) 

	fileNameCsvJson.close()
	dateOfDatesJsonHolderJson.close()



	#print(f"Time for 4 A FileNameCsvJson Writing == {time.time() - startTime} == ")



	# 4 B  ----> ----------------------------------------------------------------------------------#



	fileNamesWithCsv = open('FileNamesWithCsv.json', 'r+')
	fileDateWithoutCsv = open('DatesOfAllDatesJsonHolder.json', 'r+')

	fileList = [line.rstrip('\n') for line in fileNamesWithCsv]
	dateList = [line.rstrip('\n') for line in fileDateWithoutCsv]

	jsonDumpsFileList = (json.dumps(fileList)) 
	jsonDumpsDateList = (json.dumps(dateList))

	fileNamesWithCsv.seek(0) # Goes back to the start after keeping the correct list in memory
	fileDateWithoutCsv.seek(0) # Goes back to the start after keeping the correct list in memory

	fileNamesWithCsv.write(jsonDumpsFileList) #Prints the correct list in the specified File
	fileDateWithoutCsv.write(jsonDumpsDateList) #Prints the correct list in the specified File

	#print(f"Time for 4 B FileNameCsvJson ReWriting == {time.time() - startTime} == ")
 


	# 5 ----> -------------------------------------------------------------------------------------#



def HeaderRenamerFunc():

	lineLast_Update = 58 # Change 58 with the first appearance of Last_Update
	lineLastNextUpdate = 128


	with open('FileNamesWithCsv.json','r') as jsonFile:
		jsonFileActiveNames = json.load(jsonFile)

		for files in range(lineLast_Update,lineLastNextUpdate): # lineLastUpdate is the line of Last_Update App

			for line in fileinput.input(jsonFileActiveNames[files], inplace=True):

				if fileinput.isfirstline(): #Changes the first line to the following names
					print('FIPS,Admin2,Province_State,Country_Region,Last Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key')
				else:
					print(line)


			df = pd.read_csv(jsonFileActiveNames[files])
			df.to_csv(jsonFileActiveNames[files], index=False)

		for files in range(lineLastNextUpdate, len(jsonFileActiveNames)): # lineLastUpdate is the line of Last_Update App

			for line in fileinput.input(jsonFileActiveNames[files], inplace=True):

				if fileinput.isfirstline(): #Changes the first line to the following names
					print('FIPS,Admin2,Province_State,Country_Region,Last Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key,Incidence_Rate,Case-Fatality_Ratio')
				else:
					print(line)


			df = pd.read_csv(jsonFileActiveNames[files])
			df.to_csv(jsonFileActiveNames[files], index=False)

	#print(f"Time for 5 Renaming Last Update == {time.time() - startTime} == ")



	# 6 -----> -------------------------------------------------------------------------------------#



def CovidComputation():

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

				Country_Count = 0
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
							Country_Count += 1

							if Country_Count > 2:

									multiConfirm = 0
									multiDeaths = 0
									multiRecovered = 0
									multiActive = 0

									for manyApprCtry in activeFile1:

										if manyApprCtry['Country_Region'] == CountryName:
											multiConfirm += int(manyApprCtry['Confirmed'])
											multiDeaths += int(manyApprCtry['Deaths'])
											multiRecovered += int(manyApprCtry['Recovered'])
											multiActive += int(manyApprCtry['Active'])
									#print(multiConfirm, multiDeaths, multiRecovered, multiActive)
									#print(correct_order_list)
									correct_order_list = {'Confirmed': multiConfirm, 'Deaths': multiDeaths, 'Recovered': multiRecovered, 'Active': multiActive}


				takeoutList = ['Country/Region','ï»¿FIPS','Province/State','Country_Region','Province_State','ï»¿Province/State','Admin2','FIPS','Long_','Lat','Combined_Key','Latitude','Longitude', 'Incidence_Rate', 'Case-Fatality_Ratio']
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

					if 'Last Update' not in correct_order_list:
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
					#print(resultList)


						# Takes out the ROWs with 0,1,2,3 in them and replaces with empty('') values.
						# If you want to filter out the days with set amount of cases, add the number and they'll be ignored.
						# And uncomment the lines 282 to 284.

					for noValue in noValueDeleter:
						if resultList[noValue] == '0' or resultList[noValue] == '1' or resultList[noValue] == '2' or resultList[noValue] == '3':
							resultList.clear()


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

	#print(f"Time for 6 Computation == {time.time() - startTime} == ")



	# 7 ----> -------------------------------------------------------------------------------------#



def DaysSpecifiedFunc():

	with open('Covid19Result.csv', 'r+') as CountingFileResult:
		reader = csv.DictReader(CountingFileResult)

		numberForCount = 0
		for line in reader:
			numberForCount += 1
		dayToShow = numberForCount - DaysToBeDisplayed


	with open('Covid19Result.csv', 'r+') as DaysToCounting:
		ReaderForDaysCounting = csv.DictReader(DaysToCounting)
		numberForCount = 0

		with open('ResultWhenDaysSpecified.csv', 'w+', newline='') as DaysToShowFileCsv:
			nameForFields = ['Date', 'Confirmed', 'Deaths', 'Recovered', 'Active']
			csv_writer = csv.DictWriter(DaysToShowFileCsv, fieldnames=nameForFields)
			headerCreator = csv.writer(DaysToShowFileCsv)
			headerCreator.writerow(i for i in nameForFields)

			for dayToWriteToDisplay in ReaderForDaysCounting:
				#print(dayToWriteToDisplay)
				numberForCount += 1

				if numberForCount > dayToShow:
					csv_writer.writerow(dayToWriteToDisplay)

	#print(f"Time for 7 Days Disply Creation File == {time.time() - startTime} == ")


	# 8 ----> -------------------------------------------------------------------------------------#



def MatPlotLibFunc():

	plt.style.use('seaborn')

	ResultData = pd.read_csv('ResultWhenDaysSpecified.csv')


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

	#print(f"Time for 8 MatPlot Lib == {time.time() - startTime} == ")

	plt.show()



TotalRunner = [BeautifulSoupFunc(), DownloadsCleanerFunc(), RequestsDownloadFunc(), CsvDateCreatorFunc(), HeaderRenamerFunc(), CovidComputation(), DaysSpecifiedFunc(), MatPlotLibFunc()]
