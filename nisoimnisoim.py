from graphviz import Digraph, Graph
import webbrowser
import os
import urllib.parse

wikipedia = "https://he.wikipedia.org/w/index.php?search="
# init
dot = Graph(format='svg')
dot.attr(ranksep="1.6", pad="1", splines='polyline')# ranksep="20"  pad="24.5"  nodesep="10"
names_of_characters = open(os.path.join(os.path.dirname(__file__),"names_1.txt"), 'r', encoding="utf-8").read().split("\n") # "names_of_characters.txt"
kinship_of_characters = open(os.path.join(os.path.dirname(__file__),'kinship_1.txt'), 'r', encoding="utf-8").read().split("\n") # 'kinship_of_characters.txt'
print (names_of_characters)
dict_of_characters = {}
for num, (person, rank) in enumerate(zip(names_of_characters[::2], names_of_characters[1::2])):
    name  = person.replace("w", "").replace("k", "")
    women = (True if 'w' in person else False)
    king  = (True if 'k' in person else False)
    url   = wikipedia + urllib.parse.quote(name) + "(דמות מקראית)"
    rank  = int(rank) 
    dict_of_characters[num] = name, women, king, url, rank

ranks = {}
for k,v in dict_of_characters.items():
    rank = v[4]
    ranks.setdefault(rank, []) 
    ranks[rank].append(k)

for k, v in ranks.items():
    with dot.subgraph() as r:
        r.attr(rank='same')
        for num_person in v:
            r.node(str(num_person), dict_of_characters[num_person][0] , tooltip=str(num_person) , fillcolor=("pink" if dict_of_characters[num_person][1] == True else "powderblue") , style="filled" , shape="rectangle" , href=dict_of_characters[num_person][3], color=("gold" if dict_of_characters[num_person][2]==True else "black"))

# for num in range(len(dict_of_characters)):
#     dot.node(str(num), dict_of_characters[num][0] , tooltip=str(num) , fillcolor=("pink" if dict_of_characters[num][1] == True else "powderblue") , style="filled" , shape="rectangle" , href=dict_of_characters[num][3], color=("gold" if dict_of_characters[num][2]==True else "black"))
dot.edge('0', '1', tooltip="source", fontname="Arial", fontsize="10", penwidth="2", color="gold", rankdir='LR')
print(dot.source)

