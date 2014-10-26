"""
Uses the giantbomb api to produce a Jaccord simalarity index between two characters.
To test it out, simply call simalarity_index(charID1,charID2), where charID1 and charID2 are
character IDs, as recorded by the giantbomb database.

Example:
simalarity_index(177,370)
"""
import json
import requests

url= "http://www.giantbomb.com/api/character/3005-"
url2 = "/?api_key=ce6972cdd7d9f713817345a0256f6bd645629481&format=json"


class Character:
    def __init__(self, ID):
        self.ID = ID
    
    def name(self):
        data = requests.get(url+str(self.ID)+url2).text
        data = json.loads(data)
        if not data['results']:
            return "[Character not found]"
        else:
            return data['results']['name']
    
    def concepts(self):
        concepts_list=[]
        data = requests.get(url+str(self.ID)+url2).text
        data = json.loads(data)
        if not data['results']:
            return concepts_list
        else:
            y= data['results']['concepts']
            for concept in y:
                concepts_list.append(concept['name'])
            return concepts_list
            
def intersect(a, b):
     return list(set(a) & set(b))
     
def union(a, b):
    return list(set(a) | set(b))
    
def jaccard(a,b):
    if len(union(a,b)) == 0:
        return 0
    else:
        return float(len(intersect(a,b)))/float(len(union(a,b)))
     
def simalarity_index(charID1,charID2):
    char1 = Character(charID1)
    char2 = Character(charID2)
    print "The simalarity index between "+char1.name()+" and " +char2.name()+" is "+str(jaccard(char1.concepts(), char2.concepts()))
