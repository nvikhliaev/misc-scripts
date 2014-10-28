from lxml import html
import requests

index_url = "http://investing.businessweek.com/research/common/symbollookup/symbollookup.asp?letterIn=A&firstrow=180"


page = requests.get(index_url)
tree = html.fromstring(page.text)

names = tree.xpath('//*[@id="columnLeft"]/table/tbody/tr[1]/td[1]/a')

# graph is in adjacent list representation

graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

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


class graphs:
    def __init__(self):
        pass
    def add(self,obj):
        adict={}
        adict[str(obj.ID)]= [str(obj.ID)+'friends', str(obj.ID)+'concepts']
        return adict

class Graph(object):

    def __init__(self, graph_dict={}):
        """ initializes a graph object """
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res



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

adict={}
visited=[]
def build_graph(charID):
    visited.append(charID)
    for ID in Character(charID).friendIDs():
        adict[ID]=Character(ID).friendIDs()

    for ID in adict.keys():
        if ID not in visited:
            build_graph(ID)
    return None
