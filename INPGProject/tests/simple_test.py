import unittest

from osm_parser import Node, Way, length

class TestNode(unittest.TestCase):

    def test_init(self):
        node = Node(first, 3, 4)

        self.assertEqual(3, node.longgitude)
        self.assertEqual(4, node.latitude)

     def test_str(self):
        node = Node(first, 3, 4)

        self.assertEqual('Wierzchołek numer first dlugosc 3 szerokosc 4', __str__(node))


class TestWay(unittest.TestCase):

    def test_init(self):
        way = Way(first)

        self.assertEqual(first, way.id)

     def test_str(self):
         way = Way(first)

         self.assertEqual('Droga numer first[]', str(way))


class TestOther(unittest.TestCase):

    def test_length(self):
        node1 = Node(first, 1, 1)
        node2 = Node(second, 2, 2)

        self.assertEqual(math.sqrt(2), length(node1, node2))
