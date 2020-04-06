	# 	This needs to be in another file because once it's run, it gets the file links but it can't automatically 
	# 		call each of the links in the next process. 
	#	So you need to run this file first then go for the file where all the links get printed. Then you should 
	#		manually copy them and place them in the urls variable in the next 2nd thing.



LinksOfListOpen = open('LinksOfList.json', 'w')

correct_list = []
throwaway_list = []

	#	Need to get the links from the CSSEGISand for latest updated data.
URL = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')



for link in soup.find_all('a'):
    correct_list.append(link.get('href')) # Prints all the things with href in the page


for i in correct_list:
	
	if "csse_covid_19_data/csse_covid_19_daily_reports" in i and ".csv" in i:
		throwaway_list.append(i)

correct_list = [] # New correct blank list

for i in throwaway_list:

	added_raw = "https://raw.githubusercontent.com" + i
	removed_blob = added_raw.replace('/blob', "")
	correct_list.append(removed_blob)

for file in correct_list:

	LinksOfListOpen.write(str(file + "\n"))


LinksOfListOpen.close()



with open('LinksOfList.json', 'r+') as file:
	mylist = [line.rstrip('\n') for line in file]
	#print(mylist)
	temp = (json.dumps(mylist)) 

	file.seek(0) # Goes back to the start after keeping the correct list in memory

	file.write(temp) #Prints the correct list in the specified File


