from bs4 import BeautifulSoup  as bs4
import urllib3
import csv

# source: wikipedia
# content: countries (projected) GDP (1970-2024)
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projected_GDP_(nominal)'

http = urllib3.PoolManager()
req = http.request('GET', url)
soup = bs4(req.data, features='html.parser')

# parse table into csv
#==========================================================================
countries = []
heads = []
bodys = []
i = 0
for table in soup.find_all("table"):
    table_body = table.find_all("tbody", recursive=False)[0]
    for tr in table_body.find_all("tr"):
        if (tr.find_all("table") != None):
            for tr_table in tr.find_all("table"):
                tr_table_trs = tr_table.find_all("tr")
                if (len(tr_table_trs[0].find_all("th")) == 6 or len(tr_table_trs[0].find_all("th")) == 11):
                    # table head
                    head = []
                    body = []
                    for column in tr_table_trs[0].find_all("th"):
                        #print(column.get_text())
                        head.append(column.get_text().strip()) # trim space
                        pass
                    # table data
                    datas = tr_table_trs[1:]
                    for data in datas:
                        for idx, column in zip(range(len(data.find_all("td"))), data.find_all("td")):
                            if (idx == 0) and (column.get_text().strip() not in countries):
                                countries.append(column.get_text().strip()) # get country as index
                            #print(column.get_text())
                            body.append(column.get_text().strip())
                            pass
                    heads.append(head)
                    bodys.append(body)
                    print("======================================================>{" , str(i), " }")
                    i += 1

# write to csv
#=================================================================================================
with open("gdps_1970_2024.csv", "w", newline = "") as outfile:
    writer = csv.writer(outfile)
    head_columns = [heads[0][0]]
    for head in heads:
        head_columns += head[1:]
    writer.writerow(head_columns)
    
    for country in countries:
        row = [country]
        for body in bodys:
            if country in body:
                idx_start = body.index(country)
                if body == bodys[-1]:
                    row += body[idx_start+1:idx_start+1+5]
                else:
                    row += body[idx_start+1:idx_start+1+10]
                pass
            else:
                if body == bodys[-1]:
                    row += ['', '', '', '', '']
                else:
                    row += ['', '', '', '', '', '', '', '', '', '']
        writer.writerow(row)
