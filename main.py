from time import sleep
import requests, sqlite3
from requests.auth import HTTPBasicAuth

def pagecount():
    if 'rel="last"' in str(header):
        try:
            pagecounter = header['link'].split('?page=')
            pagecounter = pagecounter[len(pagecounter)-1][0:2]
            return int(pagecounter)
        except:
            pagecounter = header['link'].split('?page=')
            pagecounter = pagecounter[len(pagecounter)-1][0:1]
            return int(pagecounter)
    else:
        return 1

def ratelimit():
    if int(header['X-RateLimit-Remaining']) <= 1:
        print("Waiting Rate Limit")
        sleep(3600)
    else:
        print("Avaliable Rate Limit:" + header['X-RateLimit-Remaining'])

def readreposlist():
    try:
        txtlines = open("repository-urls-list.txt","r").readlines()
        for line in txtlines:
            urlslist.append(line.strip())
        print("Text File Read Successful")
        for i in range(0,len(urlslist)):
            urlslist[i] = "https://api.github.com/repos" + urlslist[i][18:len(urlslist[i])] + "/contributors"
    except:
        print("Text File Error!")
        exit()

def createdb():
    sqlconnection = sqlite3.connect("data.db")
    sqldb = sqlconnection.cursor()
    sqldb.execute("CREATE TABLE IF NOT EXISTS contributionstable(mainrepourl TEXT, url TEXT, htmlurl TEXT, followersurl TEXT, followingurl TEXT, reposurl TEXT, contributions TEXT)")
    return sqlconnection, sqldb

username = input("Github Username :")
token = input("Github Personal Access Token")

urlslist = []
readreposlist()
sqlconnection, sqldb = createdb()
for z in range(0,len(urlslist)):
    response = requests.get(urlslist[z], auth=HTTPBasicAuth(username,token))
    header = response.headers
    response = response.json()
    ratelimit()
    for i in range(pagecount()):
        if i > 0: response = requests.get(urlslist[z] + "?page=" + str(i), auth=HTTPBasicAuth(username,token)).json()
        ratelimit()
        for x in range(len(response)):
            sqldb.execute("INSERT INTO contributionstable VALUES ('"+urlslist[z]+"','"+response[x]['url']+"','"+response[x]['html_url']+"','"+response[x]['followers_url']+"','"+response[x]['following_url']+"','"+response[x]['repos_url']+"','"+str(response[x]['contributions'])+"')")
            sqlconnection.commit()
    print("Working...")

sqlconnection.close()
print("Succesful")
exit()
             

