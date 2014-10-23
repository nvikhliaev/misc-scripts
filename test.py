"""
Uses the giantbomb api to print out a list of character names
"""
import json
import requests

url= "http://www.giantbomb.com/api/character/3005-"
url2 = "/?api_key=ce6972cdd7d9f713817345a0256f6bd645629481&format=json"

print url + str(1) +url2

for i in range(1,30):
    data = requests.get(url+str(i)+url2).text
    data = json.loads(data)
    if not data['results']:
        pass
    else:
        print i
        print data['results']['name']
