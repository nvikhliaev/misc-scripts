# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 15:59:41 2014
"""

import requests
import bs4
import pandas

rowlist = []

index_url = "http://investing.businessweek.com/research/common/symbollookup/symbollookup.asp?letterIn=A&firstrow="

i=0
while i<20:
    url_to_check = index_url+str(i)
    response = requests.get(url_to_check)
    soup = bs4.BeautifulSoup(response.text)
    row = soup.findAll('table')[1].findAll('tr')[1].find_all('td')
    
    if 'No matches found' in row[0].text:
        break
    else:
        rowlist.append({'Name':row[0].text, 'Country':row[1].text, 'Industry':row[2].text})
        i+=1

df = pandas.DataFrame(rowlist)
df.to_csv('out.csv')
