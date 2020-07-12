from bs4 import BeautifulSoup  as bs4
import urllib3
import re
import csv

url_domain = "https://en.wikipedia.org"
# source: wikepidia directors list
url = "https://en.wikipedia.org/wiki/List_of_film_and_television_directors"

http = urllib3.PoolManager()

# parse link
#===================================================================================
i = 0
names = []
links = []
req = http.request("GET", url)
soup = bs4(req.data, features="html.parser")
for div in soup.find_all("div", class_="div-col columns column-width"):
    for link in div.find_all("a"):
        names.append(link.get_text().strip()) # trim space
        links.append(link.get("href").strip()) # trim space
        i += 1

print("total found: " + str(i) + " directors\n")

# parse directors infomation
#====================================================================================
heads = ["Director", "Education", "Year Active", "Birth Day", "Birth Place", "Roles", "Died", "Link"]
bodys = []

i = 0
j = 0
for name, link in zip(names, links):
    # build link
    url = url_domain + link

    req = http.request("GET", url)
    soup = bs4(req.data, features="html.parser")

    education = ""
    year_active = ""
    birth_day = ""
    birth_place = ""
    roles = ""
    died = 0  # 0: alive, 1 died, by dedfaut alive
    
    table = soup.find("table", {'class': re.compile(r'.*infobox.*vcard.*')})

    if table == None :
        j += 1
        print("****************************************************************** Unrecognized ! ************ { " + str(j) + " }")

    # parse informaton box
    if (table != None):
        # find diead
        if len(re.findall(r'Died', table.get_text())) > 0:
            died = 1
        
        # find birth_day
        bday=table.find("span", class_="bday")
        if ((bday != None) and len(bday.get_text().strip()) > 0):
            birth_day = re.sub(r'[\n|\t|\s]+', ' ', bday.get_text()).strip()

        # find birth_day2, in case that sometimes wikipedia don't fowllow the normal format
        if (birth_day == ""):
            for tr in table.find_all("tr"):
                res = re.findall(r'.*(Born|born).*', tr.get_text())
                if ((res != None) and len(res) > 0):
                    birth_day = re.sub(r'[\n|\t|\s]+', ' ', tr.get_text()).strip()
            
        # find birth_place
        div = table.find("div", class_="birthplace", style="display:inline")
        if ((div != None) and len(div.get_text()) > 0):
            birth_place = re.sub(r'[\n|\t|\s]+', ' ', div.get_text()).strip()
            pass
            
        # find roles
        td = table.find("td", class_="role")
        if ((td != None) and len(td.get_text()) > 0):
            roles = re.sub(r'[\n|\t|\s]+', ' ', td.get_text()).strip()

        # find year_active
        for tr in table.find_all("tr"):
            res = re.findall(r'.*Years.*active.*(\d{4}.*[\d{4}|present]).*', tr.get_text())
            if ((res != None) and len(res) > 0):
                year_active = re.sub(r'[\n|\t|\s]+', ' ', res[0]).strip()

        # find education
        for tr in table.find_all("tr"):
            res = re.findall(r'.*(Education|education).*', tr.get_text())
            if ((res != None) and len(res) > 0):
                education = re.sub(r'[\n|\t|\s]+', ' ', tr.get_text()).strip()

        # build row data
        body = [name, education, year_active, birth_day, birth_place, roles, died, url]
        bodys.append(body)
        i += 1
        print("=========================================================================== Succeed ! =========>{ " + str(i) + " }")
        

# write to csv
#=================================================================================================
k = 0
m = 0
with open("movie_directors_information.csv", "w", newline = "") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(heads)
    #print(heads)
    for body in bodys:
        #print(body)
        try:
            writer.writerow(body)
            k += 1
        except:
            # encode problems !
            print("\n----------------------------------- ignored ! -----------------------------------------------\n")
            m += 1
#================================================================================================
print("finished ! =============== { failed: " + str(j) + ", succeed: " + str(i) + ", ignored: " + str(m) + ", parsed: " + str(k) +" }\n")