import sqlite3
import matplotlib.pyplot as plt


def midlandsGraph():

    con = sqlite3.connect("jobData.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Leicester%' or jobTitle LIKE '%Leicester%'")
    rows = cur.fetchall()
    totalLeicester = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Birmingham%' or jobTitle LIKE '%Birmingham%'")
    rows = cur.fetchall()
    totalBirmingham = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Nottingham%' or jobTitle LIKE '%Nottingham%'")
    rows = cur.fetchall()
    totalNottingham = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Warwick%' or jobTitle LIKE '%Warwick%'")
    rows = cur.fetchall()
    totalWarwick = len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Leamington%' or jobTitle LIKE '%Leamington%'")
    rows = cur.fetchall()
    totalLeamington= len(rows)

    cur = con.cursor()
    cur.execute("SELECT * FROM 'Jobs' where location LIKE '%Derby%'")
    rows = cur.fetchall()
    totalDerby = len(rows)

    # allMidlands = ("Leamington","Alfreton", "Ashbourne"," Belper", "Bakewell", "Warwick")#, "Buxton", "Chesterfield", "Derby", "Glossop", "Ilkeston", "Long Eaton","Swadlincote", "Matlock", "Bromyard", "Hereford", "Kington", "Leominster", "Ledbury","Ross", "Weobley", "Ashby", "Coalville", "Hinckley", "Leicester", "Loughborough","Market Bosworth", "Market Harborough", "Melton" , "Lutterworth", "Corby", "Daventry", "Fotheringhay","Higham" , "Kettering", "Nassington", "Northampton", "Oundle", "Rockingham","Towcester","Wansford", "Wellingborough", "Yarwell", "Bingham", "Mansfield", "Newark", "Nottingham", "Retford","Ruddington", "Southwell", "Sutton-in-Ashfield", "Worksop", "Ashwell", "Hambleton", "Lyddington", "Oakham","Uppingham", "Bridgnorth",  "Ludlow", "Market Drayton", "Oswestry", "Shrewsbury", "Telford", "Whitchurch", "Burton" , "Cannock", "Leek", "Lichfield", "Stafford", "Stoke", "Tamworth", 'Uttoxeter', "Walsall", "Wolverhampton", "Atherstone", "Bedworth", "Coleshill", "Leamington", "Nuneaton", "Rugby","Stratford-upon-Avon", "Warwick", "Coventry", "Birmingham", "Dudley", "Evesham", "Halesowen", "Kidderminster","Stourbridge", "Malvern", "Worcester"]
    # cur = con.cursor()
    #
    # cities= cur.execute("SELECT cities FROM Midlands")
    # cur.execute("SELECT * FROM Jobs WHERE location LIKE (SELECT cities FROM Midlands)")
    # rows = cur.fetchall()
    # totalMidlands = len(rows)
    # # count=0
    # # while count != len(allMidlands):
    # #     n=allMidlands[count]
    # #     cur.execute("SELECT * FROM 'Jobs' where location LIKE (?)", (n))# or jobTitle LIKE '%"+allMidlands[count]+"%'")
    # #     count += 1


    midlandsLocations = [totalLeamington, totalNottingham, totalBirmingham, totalWarwick, totalDerby, totalLeicester,]
    midlandsTitles = ["Leamington", "Nottingham", "Birmingham", "Warwick", "Derby", "Leicester"]
    ax = plt.subplot()
    plt.bar(midlandsTitles, midlandsLocations, align='center')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    plt.xticks(fontsize=8)
    for i in range(0, len(midlandsTitles)):
        plt.text(i, midlandsLocations[i], midlandsLocations[i], ha='center')

    plt.ylabel("Total Postings")
    plt.xlabel("Midlands Locations")
    # add chart title
    plt.title("Postings in the Midlands")
    # save the plot as a PNG image
    plt.savefig("static/midlandsGraph.png")

