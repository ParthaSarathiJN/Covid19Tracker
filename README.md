# Covid19Tracker

Currently displays a .csv file with Date, Confirmed cases, Deaths, Active cases in India which 
	can be easily repurposed to any country.

1.) Open the LinkGetter.py and run it. It creates a LinkOfList.json.

2.) Then switch over to DownloadLink.py which in my case I had kept it in a different folder to get not cramped by 
	  the sheer amount of csv files. Then copy the result(list) of the LinkOFList.json and paste it in the urls
	  variable. Run the DownloadLink.py and it'll proceed to download csv files from the url given.

3.) Lastly open the MainCovidComputationFile.py and run it and it should create 2 json files and 1 csv files.
		  
The FileNamesWithCsv.json contains a list of all the path of the csv files.
		  
The DateOfAllDates.json holds a list of dates in the csv files and is needed for appending the first 
	    coulumn of the data with the dates as the date formats are bad in original csv file.
		  
At the last path everything gets sorted and appended and is stored in the Covid19Result.csv.
