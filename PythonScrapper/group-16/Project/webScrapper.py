#importing modules
import math
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template,redirect,url_for, request

from Project.jobtypeGraph import jobtypeGraph
from Project.locationgraph import locationGraph
from Project.midlandsgraph import midlandsGraph

import os
import sys

#importing name of location where app is defined
app = Flask(__name__)

#function get_db creates a connection object that allows the program to interact with the database 'jobData.db'
def get_db():
    conn = sqlite3.connect('jobData.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods = ['GET', 'POST'])
def HomePage():
    con = sqlite3.connect("jobData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Jobs")
    TotalJobs = cur.fetchall()
    totalPostings = len(TotalJobs)
    return render_template("index.html", totalPostings=totalPostings)


#Rendering the output to the 'JobPosting.html' file for the job listing webpage, users can also
@app.route('/JobPostings', methods = ['POST', 'GET'])
def JobPostingsPage():
    con = sqlite3.connect("jobData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Jobs")
    TotalJobs = cur.fetchall()
    totalPostings = len(TotalJobs)

    if request.method == 'POST':
        cur = con.cursor()
        jobsForm = request.form['getJobs']
        cur.execute("SELECT * FROM Jobs WHERE JobTitle LIKE ?", ('%' + jobsForm + '%',))
        searchRows = cur.fetchall()
        totalSearchedRows = len(searchRows)
        return render_template("JobPostings.html", rows=searchRows, totalPostings = totalSearchedRows)

    return render_template("JobPostings.html", rows = TotalJobs, totalPostings = totalPostings)


#rendering the output to the 'viewGraphs.html' file for the graphs webpage
@app.route('/viewGraphs')
def GraphPage():
    return render_template("viewGraphs.html")


# Scraper for gamesjobdirect
def gamesjobdirect():
    # Code to implement the SQL database
    conn = sqlite3.connect('JobData.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Jobs')
    cur.execute('CREATE TABLE Jobs (jobTitle TEXT, location TEXT, postdate TEXT, link TEXT)')

    # Create arrays to be used later
    jobLinks = []
    pages = []

    # Request URL and parse the data with BeautifulSoup
    URL = "https://www.gamesjobsdirect.com/results?page=1&mt=2&ic=True&l=United%2520Kingdom&lid=2635167&cc=GB&age=0&sper=4&i=9"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Number of total listing being scraped to identify the number of pages.
    # This is used later to go through each available page.
    totalListings = (soup.find("p", class_="padding-t-1").get_text())
    totalListings = int(re.search(r'\d+',totalListings).group())
    numberOfPages = math.ceil(totalListings / 10) + 1
    # For loop to go through each available page.
    # This uses the variable to number of pages created earlier
    for i in range(1, numberOfPages):
        # This section determines which page to go to
        pages = i
        URL = "https://www.gamesjobsdirect.com/results?page=" + str(pages) + "&mt=2&ic=True&l=United%2520Kingdom&lid=2635167&cc=GB&age=0&sper=4&i=9"

        # Request the page and parse it
        pageX = requests.get(URL)
        soup = BeautifulSoup(pageX.content, "html.parser")

        # Scrape links to listings and add to jobLinks
        for post in soup.find_all("div", {"class": "col-sm-9 col-lg-8 margin-b-2"}):
            for a in post.findAll('a', href=True):
                jobLinks.append("https://www.gamesjobsdirect.com/" + a['href'])

    # For each link in jobLinks, request page and parse.
    for link in jobLinks:
        jobPage = requests.get(link)
        jobsoup = BeautifulSoup(jobPage.content, "html.parser")
        # Collect name from parsed data
        name = jobsoup.find("h3", {"class": "margin-b-4"}).get_text().strip()

        # Create array to collect all information multiple bits of information from one area
        infoArray = []

        # Collect all information from aforementioned area
        for post in jobsoup.findAll("div", {"class": "well job-info-container"}):
            for item in post:
                infoArray.append(str(item).split("\n"))
            clean = re.compile('<.*?>')

            # Isolate and add information to variables
            location = infoArray[3][4]
            location = re.sub(clean, '', location)
            postdate = infoArray[5][10]
            postdate = re.sub(clean, '', postdate)

        info = jobsoup.findAll("div", {"class": "well job-info-container"})
        # Print to console all information collected
        print(name, location, postdate, link.strip())

        # Add information collected to SQL database
        cur.execute('INSERT INTO Jobs (jobTitle , location , postdate , link ) VALUES ( ?,  ?, ?,?)',(name, location, postdate, link.strip()))
        conn.commit()

# Scraper for aSwift
def aSwiftScraper():
    # Connect to SQL database
    conn = sqlite3.connect('JobData.db')
    cur = conn.cursor()

    # Create arrays to be used later
    jobLinks = []
    pages = []

    # Request URL and parse the data with BeautifulSoup
    URL = "https://aswift.com/job-search/?page_job=1&industry=&job_title=&cs_=Search&parent=bh-999833&industry=&job_title=&parent=bh-999833&industry=&job_title=&parent=bh-999833&industry=&job_title=&parent=bh-999833&industry=&job_title=&parent=bh-999833&industry=&job_title=&parent=bh-999833&industry=&job_title="
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Number of total listing being scraped to identify the number of pages.
    # This is used later to go through each available page.
    totalListings = int(soup.find('span', class_ = 'result-count').get_text())
    numberOfPages = math.ceil(totalListings / 10) + 1

    for i in range(1,numberOfPages):

        # This section determines which page to go to
        page = i
        URL = "https://aswift.com/job-search/?page_job=" + str(page) + "&industry=&job_title=&cs_=Search&parent=bh-999833&industry=&job_title="

        # Request the page and parse it
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # Scrape links to listings and add to jobLinks
        for post in soup.find_all("div", {"class": "cs-post-title"}):
            for a in post.findAll('a',href=True):
                jobLinks.append(a['href'])

    # For each link in jobLinks, request page and parse.
    for link in jobLinks:
        jobPage = requests.get(link)
        jobsoup = BeautifulSoup(jobPage.content, "html.parser")

        # Collect information from parsed data and add to variables
        name = jobsoup.find("div", {"class": "cs-page-title"}).get_text().strip()
        location = jobsoup.find("ul", {"class": "post-options"}).get_text().split('\n')[1].strip()
        postdate = jobsoup.find("ul", {"class": "post-options"}).get_text().split('\n')[2].strip()
        # Print collected data to console
        print(name, location, postdate, link)

        cur.execute('INSERT INTO Jobs (jobTitle , location , postdate , link ) VALUES ( ?,  ?, ?,?)',
                    (name, location, postdate, link.strip()))

        conn.commit()

# https://jobs.gamesindustry.biz/jobs/united-kingdom
def gamesIndustryScraper():
    conn = sqlite3.connect('JobData.db')
    cur = conn.cursor()

    # Create arrays to be used later
    jobLinks = []
    pages = []

    # Request URL and parse the data with BeautifulSoup
    URL = "https://jobs.gamesindustry.biz/jobs/united-kingdom?page=0"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    totalListings = (soup.find('h1', class_='search-result-header').get_text().split()[1])
    numberOfPages = math.ceil(int(totalListings) / 20) + 1

    for i in range(1, numberOfPages-1):

        # This section determines which page to go to
        page = i
        URL = "https://jobs.gamesindustry.biz/jobs/united-kingdom?page=" + str(page)

        # Request the page and parse it
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        #Scrape links to listings and add to jobLinks
        data = soup.find_all("a", {"class": "recruiter-job-link"})
        for x in data:
            if x.get("href") not in jobLinks:
                jobLinks.append(x.get("href"))

    # For each link in jobLinks, request page and parse.
    for link in jobLinks:
        jobPage = requests.get(link)
        jobsoup = BeautifulSoup(jobPage.content, "html.parser")

        # Collect information from parsed data and add to variables
        name = jobsoup.find("div", {"class": "pane-node-title"}).get_text().strip()
        location = jobsoup.find("div", {"class": "field--name-field-job-region"}).get_text()
        postdate = jobsoup.find("div", {"class": "job-published-date"}).get_text().split()[2]
        # Print collected data to console
        print("Job title: ",name, "Location: ", location, "Post date: ", postdate,"Link: ", link)

        # Section to scrape description.
        desc = jobsoup.findAll("div", {"class": "terms"})
        for word in desc:
            word = word.get_text().split()
            descWords.append(word)

        # Add collected data to SQL database
        cur.execute('INSERT INTO Jobs (jobTitle , location , postdate , link ) VALUES ( ?,  ?, ?, ?)', (name, location, postdate, link))
        conn.commit()

def amiqus():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    job_title = []
    job_location = []
    job_link = []

    url = "https://www.amiqus.com/jobs?options=,20993,20877,20876&page=1"
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    for title in soup.select(".attrax-vacancy-tile__title"):
        job_title.append(title.get_text(strip=True))

    #for salary in soup.select(".attrax-vacancy-tile__salary-value"):
    #    salary_amount.append(salary.get_text(strip=True))

    for location in soup.select(".attrax-vacancy-tile__option-location-valueset"):
        job_location.append(location.get_text(strip=True))

    for link in soup.select(".attrax-vacancy-tile__title"):
        job_link.append(link.get('href', href=True))

        # Section to scrape description.
        desc = soup.findAll("div", {"aria-label": "Job description"})
        for word in desc:
            word = word.get_text().split()
            descWords.append(word)
    print(job_title)
    print(job_location)
    print(job_link)


# https://hitmarker.net/
def hitMarkerScraper():
    conn = sqlite3.connect('JobData.db')
    cur = conn.cursor()

    # Create arrays to be used later
    jobLinks = []
    pages = []

    # Request URL and parse the data with BeautifulSoup
    URL = "https://hitmarker.net/jobs?location=uk"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
   # totalListings = soup.find('div', class_='justify-between mb-3').get_texft().split(' ')[0]

    for i in range(0, 19):

        # This section determines which page to go to
        page = i
        URL = "https://hitmarker.net/jobs?location=uk"

        # Request the page and parse it
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        links = []
        for i in soup.findAll("div", class_="flex items-start"):
            for link in i.findAll("a"):
                links.append(link.get("href"))

        # Section to scrape description.
        desc = soup.findAll("div", {"class": "content my-6"})
        for word in desc:
            word = word.get_text().split()
            descWords.append(word)
        #Scrape links to listings and add to jobLinks
        data = soup.find("div", class_="items-start")


# Create array to collect all instances of words in descriptions
descWords = []
keyWords =[]

#The function generateGraphs uses an if statement to determine if the 'locationGraph.png' exists
def generateGraphs():
    if not os.path.exists("static/locationGraph.png"):
        locationGraph()
        os.execl(sys.executable, sys.executable, *sys.argv)

    if not os.path.exists("static/jobtitleGraph.png"):
        jobtypeGraph()
        os.execl(sys.executable, sys.executable, *sys.argv)

    if not os.path.exists("static/midlandsGraph.png"):
        midlandsGraph()
        os.execl(sys.executable, sys.executable, *sys.argv)


generateGraphs()
#When the user runs the program it will presen them with 2 options, the first option is to regenerate job postings
#The second option will allow the user to view the job postings within a web format once all listings are loaded
print("Welcome to the jobscraper.\nWould you like to Regenerate postings (1)\nView the postings in web format (2)\n")
userChoice = input("Please enter your choice: ")

#User options
if userChoice == "1":
    print("Please allow time for  the scraper to load and run.")
    print("Loading gamesjobdirect.com scraper")
    gamesjobdirect()
    print("\n gamesjobdirect.com Complete")

    print("Loading aSwiftScraper.com scraper")
    aSwiftScraper()
    print("\n aSwiftScraper.com Complete")

    print("Loading gamesindustry.biz scraper")
    gamesIndustryScraper()
    print("\n gamesindustry.biz Complete")

    print("Loading hitMarkerScraper.biz scraper")
    hitMarkerScraper()
    print("\n hitmarker.net Complete")

if userChoice == "2":
    app.run(debug=False)

else:
    print("You must only select either 1 or 2")
    print("Please try again")



