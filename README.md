# Covid19Tracker

Displays a graph and creates a `csv` file with Date, Confirmed cases, Deaths, Active cases in India which can be easily changed to any country.

1.) Firstly open the `LinkGetter.py` and run it. It creates a `LinkOfList.json` which is a list of links from the first recorded date of the virus till the last updated date from [CSSEGISandData](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports).

2.) Then switch over to `DownloadLink.py` and run it(in my case, I had kept `DownloadLink.py` in a different folder to get not filled with the `csv` files). Then copy the `list` from the `LinkOFList.json` and paste it in the `urls` variable. Run the `DownloadLink.py` and it'll proceed to download `csv` files from the given urls.

3.) Lastly open the MainCovidComputationFile.py and run it and it should create 2 `json` files and 1 `csv` files and also should display a graph.
		  
The `FileNamesWithCsv.json` contains a list of all the path directories of the csv files.
		  
The `DateOfAllDates.json` holds a list of dates in the `csv` files and is needed for appending the first coulumn of the data with the dates as the date formats are bad in original csv file.
		  
All the data gets sorted and is stored in the `Covid19Result.csv`.


*There is also a `MatPlotLibPlotGraph.py` file which can be used to mess around with the styles and if needed more data can be displayed. But it is not needed to be run.*

## Source: [John Hopkins University CSSE](https://github.com/CSSEGISandData/COVID-19)
