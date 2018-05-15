"""
Funkcje do generowania grafu w formacie networkx
WIP
Uzycie:
python osm_parser sciezka_pliku_osm
"""

import networkx as nx
import xml.etree.ElementTree as et
import sys


class Node:
    def __init__(self, id, longitude, latitude):
        self.id = id
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return "Wierzchołek numer {} dlugosc {} szerokosc {}\n".format(self.id, self.longitude, self.latitude)


class Way:
    def __init__(self, id):
        self.id = id
        self.nodes = []
        self.tags = []

    def __str__(self):
        return "Droga numer {} z tagami\n".format(self.id) + str(self.tags) + "\n"


def parse_osm(osm_path):
    ways = []
    nodes = []
    tree = et.parse(osm_path)
    root = tree.getroot()
    for way in root.iter("way"):
        w = Way(way.get("id"))
        w.tags = dict([(x.get("k"), x.get("v")) for x in way.iter("tag")])
        if "highway" not in w.tags.keys():
            continue
        w.nodes = [x.get("ref") for x in way.iter("nd")]
        ways.append(w)

    for node in root.iter("node"):
        n = Node(node.get("id"), node.get("lon"), node.get("lat"))
        nodes.append(n)

    return ways, nodes


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        path = "data\map.osm"
    ways, nodes = parse_osm(path)
    with open("data\output.txt", "w", encoding="utf-8") as f:
        for way in ways:
            f.write(str(way))
        for node in nodes:
            f.write(str(node))




