import sqlite3
import matplotlib.pyplot as plt

def jobtypeGraph():
    con = sqlite3.connect("jobData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where jobTitle LIKE '%Design%'")
    rows = cur.fetchall()
    totalDesigner = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where jobTitle LIKE '%Artist%'")
    rows = cur.fetchall()
    totalArtist = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where jobTitle LIKE '%Program%'")
    rows = cur.fetchall()
    totalDeveloper = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where jobTitle LIKE '%UI%'")
    rows = cur.fetchall()
    totalUI = len(rows)


    totalJobTitles = [totalDeveloper, totalDesigner, totalArtist, totalUI]
    jobTitles = ["Development", "Design", "Artist", "UI"]
    plt.bar(jobTitles,totalJobTitles)
    for i in range(0, len(jobTitles)):
        plt.text(i, totalJobTitles[i], totalJobTitles[i], ha='center')
    plt.ylabel("Total Postings")
    plt.xlabel("Job Titles")
    # add chart title
    plt.title("Most Common keywords in job postings")
    # save the plot as a PNG image
    plt.savefig("static/jobtitleGraph.png")

