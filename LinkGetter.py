	# 	This code needs to be in another file(LinkGetter.py) because, it gets the link of the files(csvs) which need to
	#		be downloaded in order to analyze the data, but it can't automatically call each of the links in 
	#		the next process. 
	#
	#	So you need to run this code first individually, later go for the file - LinksOfList.json where all the 
	#		links get stored. Then you have to manually copy the whole list present in LinksOfList.json and 
	#		paste them in the urls variable in the next file that is, DownloadLink.py.


from bs4 import BeautifulSoup
import requests
import json


LinksOfListOpen = open('LinksOfList.json', 'w')

mainList = []
temporaryList = []

#Need to change URL to CSSEGISandData for latest data
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



with open('LinksOfList.json', 'r+') as file:
	myList = [line.rstrip('\n') for line in file]
	#print(myList)
	temp = (json.dumps(myList)) 

	file.seek(0) # Goes back to the start after keeping the myList in memory

	file.write(temp) #Prints the myList in the specified File
