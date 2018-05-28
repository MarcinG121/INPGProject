"""
Funkcje do generowania grafu w formacie networkx
WIP
Uzycie:
python osm_parser sciezka_pliku_osm
"""

import networkx as nx
import xml.etree.ElementTree as et
import math


class Node:

    def __init__(self, id: str, longitude: float, latitude: float):
        self.id = id
        self.longitude = longitude
        self.latitude = latitude
        self.used = 0

    def __str__(self):
        return "Wierzchołek numer {} dlugosc {} szerokosc {}\n".format(self.id, self.longitude, self.latitude)


class Way:

    def __init__(self, id: str):
        self.id = id
        self.nodes = []
        self.tags = []

    def __str__(self):
        return "Droga numer {} z tagami\n".format(self.id) + str(self.tags) + "\n"


def length(n1: Node, n2: Node):
    return math.sqrt(pow(n1.latitude - n2.latitude, 2) + pow(n1.longitude - n2.longitude, 2))


def parse_osm(osm_path: str):
    g = nx.Graph()
    ways = []
    nodes = {}
    tree = et.parse(osm_path)
    root = tree.getroot()
    for node in root.iter("node"):  # each node from map is stored in nodes dictionary
        n = Node(node.get("id"), float(node.get("lon")), float(node.get("lat")))
        nodes[node.get("id")] = n
    for way in root.iter("way"):  # each road from map is stored in ways list
        w = Way(way.get("id"))
        w.tags = {x.get("k"): x.get("v") for x in way.iter("tag")}
        if "highway" not in w.tags.keys():  # every road is highway type
            continue
        if w.tags["highway"] in ["pedestrian", "footway", "cycleway", "bridleway", "path"]:  # those are not roads
            continue
        w.nodes = [x.get("ref") for x in way.iter("nd")]  # list of nodes ids
        for n in w.nodes:
            nodes[n].used += 1
        ways.append(w)
    for way in ways:
        junctions = []
        n1 = way.nodes[0]
        g.add_node(nodes[n1].id, node=nodes[n1])
        junctions = [nodes[n] for n in way.nodes if nodes[n].used > 1]
        for (i, j) in enumerate(junctions):
            g.add_node(j.id, node=j)
            if i > 0:
                g.add_edge(junctions[i - 1].id, junctions[i].id, weight=length(junctions[i - 1], junctions[i]))
    return g

# TODO: funkcja znajdująca wierzchołek blisko podanych koordynatów
def find_closest(latitude_length: str) -> str:
    """
    zwraca id wierzchołka bliskiego podanym koordynatom
    latitude_length w formacie str oddzielone przecinkiem np. "50.21,20.38"
    """
    pass


def get_route(g, node1_id="240977613", node2_id="2468665585"):
    d_path = nx.dijkstra_path(g, node1_id, node2_id)
    coordinates = ""
    for n in d_path:
        coordinates += "[{},{}],".format(g.nodes[n]['node'].latitude, g.nodes[n]['node'].longitude)
    coordinates = coordinates[:-1]
    return coordinates

# if __name__ == "__main__":
#     try:
#         path = sys.argv[1]
#     except IndexError:
#         path = "data\msagh.osm"
#     nodes, g = parse_osm(path)
# with open("data\output.txt", "w", encoding="utf-8") as f:
#     for way in ways:
#         f.write(str(way))
#     for node in nodes:
#         f.write(str(node))
# d_path = nx.dijkstra_path(g, "1450438909", "1055518868")
