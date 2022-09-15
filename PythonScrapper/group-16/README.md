# GitLab repository for CO2201 Group 16 Project

## Purpose:
This program is created to scrape certain job listing sites to collect relevant information and store it in a database. 
In the future, there will be better viewing options, and potentially the ability to manipulate the data to see only what you want.

## Features:
* Scrapers for:
  * aSwift
  * GamesJobDirect
  * GamesIndustry
  * Amiqus
  * HitMarker
* Collection of the following information:
  * Job Title
  * Location 
  * Post Date
  * Link
* Web Application Interface:
  * View the different graphs, that have been developed using the data from the database.
  * View the job-postings.
  * Search for keywords in the postings.


## Installation and Usage:
Dependencies:
1. Python 3.8
2. Flask
3. BeautifulSoup4
4. Requests
5. MatPlotLib
8. Pandas
9. SQLLite3

Installation:
1. Clone this repo to local directory.
2. Open the folder as a project in your IDE of choice. (PyCharm is recommended since it was the development environment)
3. Install the following dependencies to your Python Environment:
   1. All dependencies from above list.
   4. (There may be some others. Check the imports section at start of main Python file)

Usage:
1. Run the webscaper.py Python file. 
2. Follow any instructions in console (If any)
3. In the program you can either regenerate the sql file with the latest job postings or view them in a web application.
