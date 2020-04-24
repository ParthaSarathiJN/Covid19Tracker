# Covid19Tracker

Displays a graph and creates a `csv` file with Date, Confirmed cases, Deaths, Active cases in India which can be modified to other country.

## Working

Open the `MainCovidComputationFile.py` and run it. After running it will create `LinksOfList.txt`, `FilesNamesWithCsv.txt`, `DatesOfAllDatesJsonHolder.json`,  `Covid19Result.csv` and finally displays a graph.

`LinksOfList.txt` gets the links of all the csv files from [csse_covid_19_daily_reports](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) and downloads those files.

The `FileNamesWithCsv.json` contains a list of all the path directories of the csv files.
		  
The `DateOfAllDates.json` holds a list of dates in the `csv` files and is needed for appending the first coulumn of the data with the dates as the date formats are bad in original csv file.
		  
All the data gets sorted and is stored in the `Covid19Result.csv`.

From this sorted data in `Covid19Result.csv` it displays a graph of those values.


## Source: [John Hopkins University CSSE](https://github.com/CSSEGISandData/COVID-19)
