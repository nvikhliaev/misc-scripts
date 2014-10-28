import json
import requests

url= "http://www.giantbomb.com/api/character/3005-"
url2 = "/?api_key=ce6972cdd7d9f713817345a0256f6bd645629481&format=json"

class Character:
    def __init__(self, ID):
        self.ID = ID
        self.data = json.loads(requests.get(url+str(self.ID)+url2).text)['results']
    
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

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

def build_graph(charID, adict, visited):
    visited.append(charID)
    adict[charID] = Character(charID).friendIDs()
    for friendID in adict[charID]:
        if friendID not in visited:
            build_graph(friendID, adict, visited)
    return adict
