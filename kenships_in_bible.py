from graphviz import Digraph, Graph
import webbrowser
import os
import urllib.parse
dot = Graph(format='svg')
dot.attr(ranksep="1.6", pad="1")# ranksep="20"  pad="24.5"  nodesep="10"
dot.attr(splines='polyline')
names_of_characters = open(os.path.join(os.path.dirname(__file__),"names_of_characters.txt"), 'r', encoding="utf-8")
kinship_of_characters = os.path.join(os.path.dirname(__file__),'kinship_of_characters.txt')
list_of_names = names_of_characters.read().split("\n")

def add_person(graph, number):
    name, tooltip = get_tooltip(number)
    wikipedia = "https://he.wikipedia.org/w/index.php?search="
    name_url = urllib.parse.quote(name.replace("w", "").replace("k", ""))
    href = wikipedia + name_url + "(דמות מקראית)"
    # "https://he.wikipedia.org/wiki/%D7%90%D7%91%D7%A8%D7%94%D7%9D"
    if 'עתליהו' in name:
        graph.node(str(number) , name.replace("k" , "") , tooltip=tooltip , fillcolor="pink" , style="filled" , shape="rectangle" , href=href ,color="gold")
    if 'w' in name:
        graph.node(str(number) , name.replace("w", "") , tooltip=tooltip , fillcolor="pink" , style="filled" , shape="rectangle" , href=href)
    elif 'k' in name:
        graph.node(str(number) , name.replace("k" , "") , tooltip=tooltip , fillcolor="powderblue" , style="filled" , shape="rectangle" , href=href, color="gold")
    else:
        graph.node(str(number), name, tooltip=tooltip, fillcolor="powderblue", style="filled", shape="rectangle", href=href)

def chrome_hebrew(name):
    if "(" in name:
        return name + u'\u200F' # Right to left character
    return name

def get_tooltip(number):
    name = list_of_names[number]
    open_, close_ = name.find("["), name.find("]")
    if open_==-1 or close_==-1:
        return chrome_hebrew(name), str(number)
    return chrome_hebrew(name[:open_]), name[open_+1:close_]

def get_diagram_husband_and_wife(husband, wife, source):
    with dot.subgraph() as s:
        s.attr(rank='same')
        add_person(s , husband)
        add_person(s , wife)
    with dot.subgraph() as s:
        point_name = str(husband) + "+" + str(wife)
        s.node(point_name, shape = 'point')
        s.edge(str(husband), point_name, tooltip=source, fontname="Arial", fontcolor="blue", fontsize="10" , penwidth="2" , color = "green")
        s.edge(point_name, str(wife), tooltip=source , fontname="Arial" , fontcolor="blue" , fontsize="10"  , penwidth="2" ,color="green")

def get_diagram_father_and_son(parentes, son, source):
    # parentes is string (E.g. "3" or "3+4")
    # son is always int
    # source is str (of course...)
    d = dot
    d.rankdir = "TB"
    if "+" in parentes:
        t = parentes.split("+")
        father = int(t[0])
        mother = int(t[1])
        add_person(d, father)
        add_person(d, mother)
        d.node(parentes , shape='point')
    else:
        father = int(parentes)
        add_person(d, father)
        parentes = str(father)
    add_person(d, son)
    d.edge(parentes , str(son) , tooltip=source , fontname="Arial" , fontcolor="blue" , fontsize="10" , penwidth="2" , color="red")
    #dot.subgraph(d)

def get_diagram_kings(king1, king2, source):
    with dot.subgraph() as k:
        add_person(k , king1)
        add_person(k , king2)
        k.edge(str(king1) , str(king2) , tooltip=source , fontname="Arial" , fontcolor="blue" , fontsize="10" , penwidth="2" , color="gold")

list_of_hasbends_and_wifes = []
list_of_fathers_and_sons = []
list_of_kings = []
def main():
    with open(kinship_of_characters, 'r', encoding="utf-8") as fid:
        lines =  fid.readlines()
    for num, source in zip(lines[::2], lines[1::2]):
        kinship_number = num.replace("\n", "")
        if '#' in kinship_number:
            continue
        source = source.replace("\n", "")
        if ',' in kinship_number:
            kinship_number = kinship_number.split(',')
            list_of_fathers_and_sons.append((kinship_number[0], int(kinship_number[1]), source))
            get_diagram_father_and_son(kinship_number[0] , int(kinship_number[1]) , source)
        elif '+' in kinship_number:
            husband_and_wife = list(map(int ,kinship_number.split('+')))
            list_of_hasbends_and_wifes.append((husband_and_wife[0], husband_and_wife[1], source))
            get_diagram_husband_and_wife(husband_and_wife[0], husband_and_wife[1], source)
        elif 'k' in kinship_number:
            kings = list(map(int ,kinship_number.split('k')))
            list_of_kings.append((kings[0], kings[1], source))
            get_diagram_kings(kings[0], kings[1], source)

main()
# print(dot.source)
dorot_ = os.path.join(os.path.dirname(__file__),"dorot_")

dot.render(filename=dorot_)
chrome_path =  r"C:/Program Files/Google/Chrome/Application/chrome.exe %s"
# chrome_path = 'C:/Users/burstain/AppData/Local/Google/Chrome/Application/chrome.exe --profile-directory="Profile 1" %s'
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
webbrowser.get(chrome_path).open(dorot_+".svg")
