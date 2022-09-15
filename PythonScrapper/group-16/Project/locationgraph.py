import sqlite3
import matplotlib.pyplot as plt

def locationGraph():
    con = sqlite3.connect("jobData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%London%'")
    rows = cur.fetchall()
    totalLondon = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Manchester%'")
    rows = cur.fetchall()
    totalManchester = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Nottingham%'")
    rows = cur.fetchall()
    totalNottingham = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Farnborough%'")
    rows = cur.fetchall()
    totalFarnborough = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Sheffield%'")
    rows = cur.fetchall()
    totalSheffield = len(rows)

    totalLocations = [totalLondon, totalFarnborough, totalManchester, totalNottingham, totalSheffield]
    titles = ["London", "Farnborough", "Manchester", "Nottingham", "Sheffield"]
    plt.bar(titles,totalLocations)
    for i in range(0, len(titles)):
        plt.text(i, totalLocations[i], totalLocations[i], ha='center')
    plt.ylabel("Total Postings")
    plt.xlabel("Recent Locations")
    # add chart title
    plt.title("Most Common Locations of Postings")
    # save the plot as a PNG image
    plt.savefig("static/locationGraph.png")

