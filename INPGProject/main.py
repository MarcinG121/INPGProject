from grid import *
import sys
import math
from random import randint


class PathFinder():
    class Node():
        def __init__(self, obs, pos):
            self.obstacle = obs
            self.visited = False
            self.connections = []
            self.pos = pos
            self.dist = math.inf
            self.prev = None

    def __init__(self, argv):
        if len(argv) < 2:
            print('Usage: {} file'.format(argv[0]))
            exit(1)
        self.display = GridDisplay(0, 0, True, 'PathFinder')
        self.grid = self.display.createGrid(10, 10, self.display.getWindowSize()[0] - 20,
                                            self.display.getWindowSize()[1] - 20, (GridDisplay.BLUE, GridDisplay.BLACK))
        self.data = []
        self.grid.outline = 3
        self.source = (0, 0)
        self.target = (0, 0)
        self.readFile(argv[1])
        self.fillBoard()
        self.grid.setFontFace('./Hack-Bold.ttf')
        self.grid.setFontSize(14)
        self.graphify()

    def readFile(self, file):
        with open(file, 'r') as f:
            try:
                lines = [line for line in f.read().split('\n') if len(line.strip()) > 0]
                count = -1
                for line in lines:
                    if 't' in line:
                        self.target = (line.index('t'), len(self.data))
                        line = line.replace('t', '0')
                    if 's' in line:
                        self.source = (line.index('s'), len(self.data))
                        line = line.replace('s', '0')
                    self.data.append([int(c) for c in line])
                    if count != -1 and len(self.data[-1]) != count:
                        print("Lines are not of equal length")
                        exit(-2)
                    count = len(self.data[-1])
            except Exception as e:
                print("File format error: {}".format(e))
                exit(-1)
        self.source = (self.source[0], len(self.data) - 1 - self.source[1])
        self.target = (self.target[0], len(self.data) - 1 - self.target[1])

    def graphify(self):
        xlen = self.grid.getBoardSize()[0]
        ylen = self.grid.getBoardSize()[1]
        for y in range(ylen):
            for x in range(xlen):
                tile = self.grid.getTile(x, y)
                if tile.data.obstacle:
                    continue
                if y > 0 and not self.grid.getTile(x, y - 1).data.obstacle:
                    tile.data.connections.append((x, y - 1))
                if y < ylen - 1 and not self.grid.getTile(x, y + 1).data.obstacle:
                    tile.data.connections.append((x, y + 1))
                if x > 0 and not self.grid.getTile(x - 1, y).data.obstacle:
                    tile.data.connections.append((x - 1, y))
                if x < xlen - 1 and not self.grid.getTile(x + 1, y).data.obstacle:
                    tile.data.connections.append((x + 1, y))

    def fillBoard(self):
        len_x = len(self.data[0])
        len_y = len(self.data)
        self.grid.populate(len_x, len_y)
        for y in range(len_y):
            for x in range(len_x):
                self.grid.getTile(x, y).data = PathFinder.Node(self.data[len_y - 1 - y][x] == 1, (x, y))
                if self.grid.getTile(x, y).data.obstacle:
                    self.grid.getTile(x, y).color = GridDisplay.RED
        self.grid.getTile(*self.source).color = GridDisplay.MAGENTA
        self.grid.getTile(*self.target).color = GridDisplay.GREEN

    def run(self):
        a_star_alg = AStarAlgorithm(self.grid.getTile(*self.source).data, self.grid.getTile(*self.target).data, self.grid)
        while not self.display.closeRequest:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.display.closeRequest = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.display.closeRequest = True

            for i in range(3):
                a_star_alg.AStarAlgorithmIter()
            self.display.render()
            self.display.tick(60)

class AStarAlgorithm():

    def __init__(self, source, target, grid):
        self.source = source
        self.target = target
        self.grid = grid
        self.hasEnd = False
        self.openset = set()
        self.closedset = set()
        self.g_score = {}
        self.h_score = {}
        self.f_score = {}
        for node in grid:
            self.g_score[node.data] = math.inf
            self.h_score[node.data] = math.inf
            self.f_score[node.data] = math.inf
        self.g_score[source] = 0
        self.openset.add(self.source)

    def heuristic(self, vertex):
        return  abs(vertex.pos[0] - self.target.pos[0]) + abs(vertex.pos[1] - self.target.pos[1])

    def reconstruct_path(self):
        point = self.target
        while point is not self.source:
            self.grid.getTile(*point.pos).color = (0xFE, 0x7F, 0x00)
            point = self.grid.getTile(*point.prev).data

    def AStarAlgorithmIter(self):
        if len(self.openset) == 0 or self.hasEnd:
            return
        minVertex = min(self.openset, key=lambda ver: self.f_score[ver])
        if minVertex is self.target:
            self.reconstruct_path()
            self.hasEnd = True
            return
        self.openset.remove(minVertex)
        self.closedset.add(minVertex)
        for conn in [self.grid.getTile(*c).data for c in minVertex.connections]:
            if conn in self.closedset:
                continue
            tentative_g_score = self.g_score[minVertex] + 1
            tentative_is_better = False
            if conn not in self.openset:
                self.openset.add(conn)
                self.h_score[conn] = self.heuristic(conn)
                tentative_is_better = True
            elif tentative_g_score < self.g_score[conn]:
                tentative_is_better = True
            if tentative_is_better:
                conn.prev = minVertex.pos
                self.g_score[conn] = tentative_g_score
                self.f_score[conn] = self.g_score[conn] + self.h_score[conn]
                self.grid.getTile(*conn.pos).setText(str(self.g_score[conn]))
                self.grid.getTile(*conn.pos).color = (0x00, 0x80, 0x00)

if __name__ == '__main__':
    PathFinder(sys.argv).run()
