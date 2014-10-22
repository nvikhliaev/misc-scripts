import json
import requests

url = "http://www.giantbomb.com/api/characters/?api_key=ce6972cdd7d9f713817345a0256f6bd645629481&format=json&field_list=name&filter=id:"

for i in range(1,100):
    data = requests.get(url+str(i)).text
    data = json.loads(data)
    if not data['results']:
        pass
    else:
        print i
        print data['results'][0]['name']