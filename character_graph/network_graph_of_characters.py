import requests
import sys
from py2neo import neo4j,node, rel
import time
import json

url= "http://www.giantbomb.com/api/character/3005-"
url2 = "/?api_key=ce6972cdd7d9f713817345a0256f6bd645629481&format=json"
url3 = "http://www.giantbomb.com/api/concept/3015-"

class Character:
    def __init__(self, ID):
        self.ID = ID
        self.data = requests.get(url+str(self.ID)+url2).json()['results']
    
    def name(self):
        if not self.data:
            return "[Character not found]"
        else:
            return self.data['name']
    
    def concepts(self):
        concepts_list=[]
        if not self.data:
            return concepts_list
        else:
            for concept in self.data['concepts']:
                concepts_list.append(concept['name'])
            return concepts_list
    
    def conceptIDs(self):
        conceptIDs_list=[]
        if not self.data:
            return conceptIDs_list
        else:
            for concept in self.data['concepts']:
                conceptIDs_list.append(concept['id'])
            return conceptIDs_list
    
    def friends(self):
        friends_list=[]
        if not self.data:
            return friends_list
        else:
            for friend in self.data['friends']:
                friends_list.append(friend['name'])
            return friends_list
    
    def friendIDs(self):
        friends_list=[]
        if not self.data:
            return friends_list
        else:
            for friend in self.data['friends']:
                friends_list.append(friend['id'])
            return friends_list

class Concept:
    def __init__(self, ID):
        self.ID = ID
        self.data = requests.get(url3+str(self.ID)+url2).json()['results']
    
    def name(self):
        if not self.data:
            return "[Concept not found]"
        else:
            return self.data['name']
    
    def characters(self):
        characters_list=[]
        if not self.data:
            return characters_list
        else:
            for character in self.data['characters']:
                characters_list.append(character['name'])
            return characters_list
            
    def characterIDs(self):
        characterIDs_list=[]
        if not self.data:
            return characterIDs_list
        else:
            for character in self.data['characters']:
                characterIDs_list.append(character['id'])
            return characterIDs_list

def build_graph_names(charID, adict, visited):
    charac = Character(charID)
    visited.append(charID)
    adict[charac.name()] = charac.friends()
    for friendID in charac.friendIDs():
        if friendID not in visited:
            build_graph_names(friendID, adict, visited)
    return adict
    
def build_graph_IDs(charID, adict, visited):
    charac = Character(charID)
    visited.append(charID)
    adict[charID] = charac.friendIDs()
    for friendID in charac.friendIDs():
        if friendID not in visited:
            build_graph_IDs(friendID, adict, visited)
    return adict

def connected(graph, A, B):
    if not graph:
        return False
    for edge in graph:
        if ((edge['source']==A) and (edge['target']==B)) or ((edge['source']==B) and (edge['target']==A)):
            return True
    return False

def build_json_nodes(graph):
    nodes_list=[]
    edges_list=[]
    i=0
    keys = graph.keys()
    for key in keys:
        nodes_list.append({'size':1, 'id':str(key), 'label':str(key)})
    for key in keys:
        for friend in graph[key]:
            if not connected(edges_list,str(key),str(friend)):
                edges_list.append({'id':str(i), 'source':str(key), 'target':str(friend)})
                i+=1
    with open("data.json",  mode="w") as outfile:
        json.dump({'nodes':nodes_list, 'edges':edges_list}, outfile, indent=4)
 


#The code below is experimental and pertains only to when a local instance of neo4j is running.
#neo4j is an open source database for storing graph-based data. The variable graph_db references the local
#neo4j instance. The function build_graph_neo will take a character ID and load their network of friends
#into the local neo4j database.
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
  
def build_graph_neo(charID, adict, visited):
    charac = Character(charID)
    visited.append(charID)
    this_node = graph_db.get_or_create_indexed_node("Characters",'ID',charID,{'name':charac.name()})
    for friendID in charac.friendIDs():
        friend_node = graph_db.get_or_create_indexed_node("Characters",'ID',friendID)
        if not list(graph_db.match(start_node=this_node, end_node=friend_node,bidirectional=True)):   
            link = neo4j.Path(this_node,"friends",friend_node)
            link.get_or_create(graph_db)
    for friendID in charac.friendIDs():
        if friendID not in visited:
            build_graph_neo(friendID, adict, visited)
    return adict
    
#build_neo will load the first 50 characters into the local neo4j instance as nodes.
def build_neo(i):
    while i<50:
        charac = Character(i)
        if not charac.data:
            pass
        else:
            graph_db.get_or_create_indexed_node("Characters",'ID',i,{'name':charac.name()})
        if i%300 ==0:
            time.sleep(900)
        i+=1

