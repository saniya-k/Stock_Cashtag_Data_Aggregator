# Stock & Cashtag Data Aggregator

![banner](/images/banner.png) <br/>

This is a scraping tool that can be used to get stock market and twitter mentions relating to a company. Here we've focussed on Technology Companies in S&P500.

## Generate S&P 500 companies (**S&P Top 500 companies.ipynb**)  

The first part of this project is to find out which companies are in S&P Top500 and figure out their tickers and industries that they are in for the further use. Then, all the information found in the last step is save in **S&P 500 companies.csv** file. The process to run the file is - 

Take a look on the source code of a page. To do that, you should right click on the Wikipedia page and select the option *View Page Source*. After that, you can find the *html* code of the page. The table is under the *table* tag having *wikitable sortable as class: 

1. Install beautifulsoup4 package (and other dependencies) using: 

    > pip install beautifulsoup4 

    > Dependencies: 
    ```
    import bs4 as bs
    ```
    ```
    import requests
    ```
    ```
    import pandas as pd
    ```

2. Run the code on jupyter notebook. 

This module generates one file which includes the basic information of companies in S&P Top500, such as company name, ticker and industry, named **S&P 500 companies.csv** file. 



## Yahoo Finance Data Scraping (**YahooFinance_WebScrape.ipynb**)  

The goal of this part is to find the information of all S&P500 companies. Then extract the list of Technology companies and the historical data of their stocks for recent 5 years. The process to run the file is - 

1. Install selenium package (and other dependencies) using: 

    > pip install selenium 

    > Dependencies: 
    ```
    from selenium import webdriver
    ```
    ```
    import time
    ```
    ``` 
    import pandas as pd
    ```
    ```
    from bs4 import BeautifulSoup
    ```


2. Selenium requires a driver to interface with the chosen browser. Here we use Chrome. There are two ways to use the driver.  

    a. Find the file called **chromedriver.exe** in your computer. (The path we use here is C:\Users\name\Anaconda3\Lib\site-packages\chromedriver_binary\chromedriver.exe. You may find the file in a similar path) 

    b. If you are not able to find the file, you may need to download a new one (https://chromedriver.chromium.org/downloads). Then find the path of the file into the script. 

3. The Chrome will be automatically opened when you run the script. Don’t close it. 

This module generates three files – the first one contains all the information, includes company address, sector, industry, website, etc, called **SP500_allInfo.csv**. The second one extracts the list of companies in certain sector, here is technology, which is **FinalList_Tech.csv**. The third one is the historical Data of their stocks for recent 5 years which can be found in **StockPrice_Tech_FiveYear.csv**. 

### Limitations -  

The search bar of the web may not be stable to get the accurate target stock especially when the loop is large.   

 

## Twitter Data Extraction (**TwitterDataExtraction.ipynb**)  

The third part of this project deals with extracting Tweets from Twitter for the list of Tech companies mentioned in the **FinalList_Tech.csv** file. The process to run the file is - 

1. Apply for a developer account on Twitter (https://developer.twitter.com/en/apply-for-access) 

2. Get the API key, API secret key, access token, access token secret from twitter and update these in the **authentication.txt** file. 

    > api_key
    > api_secret_key
    > access_token
    > access_token_secret

3. Install tweepy (and other dependencies) using: 

    > pip install tweepy 

    > Dependencies: 
    ```
    import tweetpy
    ```
    ```
    import pandas as pd
    ```
    ```
    import time
    ```
    ```
    from datetime import date, timedelta
    ```
    ```
    from pprint import pprint
    ```

4. Keep the files **FinalList_Tech.csv, authentication.txt, TwitterDataExtraction.ipynb** in the same folder. 

5. Run the code from notebook. 

This module generates three files – One, the actual tweets for each of the companies (**Twitter_Tech_data_{current_date}.csv**) made in the past two days, Two, it appends a column the number of tweets made for list of companies in the FinalList_Tech.csv and saves it as **FinalList_Tech _{current_date}.csv**. Third, it generates a script which contains the entire notebook code (**getTwitterData.py**) which can be automated by adding it to the crontab: 

> @daily python3 /complete path to /getTwitterData.py 

### Limitations - 

1. We can only fetch data for past 7 days from the Twitter API.  

2. Rate limits:  900 request / 15 min PER USER AUTH & 300 request / 15 min PER APP AUTH  

3. Sometimes you might face ConnectionReset/Read limits Exceptions for some companies. There is code which retries getting data for the skipped companies. The maximum number of retries is set to 3. Also, for companies which you are retrying, only 300 tweets are fetched. 