# Build Road
# 1.create a simple road between two points
# problem: how to see two points location in the map.
import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import*
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

from mcplatform import *

import utilityFunctions as utilityFunctions

inputs = (
    ("Road Build Example", "label"),
    ("Road Material", alphaMaterials.Cobblestone),  # the material we want to use to build the mass of the structures
    ("Bridge Material", alphaMaterials.Wood),
    ("Creator: Changxing Cao", "label"),
)

# -*- coding: utf-8 -*-
import math

test_map = []
tm = []


#########################################################
class Node_Elem:
    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist

class A_Star:
    def __init__(self, s_x, s_y, e_x, e_y, box):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y

        self.width = box.maxx - box.minx
        self.height = box.maxz - box.minz

        self.open = []
        self.close = []
        self.path = []

    def find_path(self):
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            self.extend_round(p)
            if not self.open:
                return
            idx, p = self.get_best()
            if self.is_target(p):
                self.make_path(p)
                return
            self.close.append(p)
            del self.open[idx]
 
    def make_path(self,p):
        while p:
            self.path.append((p.x, p.y))
            p = p.parent

    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y

    def get_best(self):
        best = None
        bv = 1000000 
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)
            if value < bv:
                best = i
                bv = value
                bi = idx
        return bi, best

    def get_dist(self, i):
        return i.dist + math.sqrt(
            (self.e_x-i.x)*(self.e_x-i.x)
            + (self.e_y-i.y)*(self.e_y-i.y))*1.2

    def extend_round(self, p):
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1,-1,-1,  0, 0,  1, 1, 1)
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            if not self.is_valid_coord(new_x, new_y):
                continue
            node = Node_Elem(p, new_x, new_y, p.dist+self.get_cost(
                        p.x, p.y, new_x, new_y))
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            if i != -1:
                if self.open[i].dist > node.dist:
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                continue
            self.open.append(node)

    def get_cost(self, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.4

    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'

    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.close:
            l.append((i.x, i.y))
        return l

#########################################################

def print_test_map():
    for line in test_map:
        print ''.join(line)

def get_start_XY():
    return get_symbol_XY('S')

def get_end_XY():
    return get_symbol_XY('E')

def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x, y

#########################################################
def mark_path(l):
    mark_symbol(l, '*')

def mark_searched(l):
    mark_symbol(l, ' ')

def mark_symbol(l, s):
    for x, y in l:
        test_map[y][x] = s

def mark_start_end(s_x, s_y, e_x, e_y):
    test_map[s_y][s_x] = 'S'
    test_map[e_y][e_x] = 'E'

def tm_to_test_map():
    for line in tm:
        test_map.append(list(line))

def find_path(box):
    s_x, s_y = get_start_XY()
    e_x, e_y = get_end_XY()
    a_star = A_Star(s_x, s_y, e_x, e_y, box)
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    mark_searched(searched)
    mark_path(path)
    print "path length is %d"%(len(path))
    print "searched squares count is %d"%(len(searched))
    mark_start_end(s_x, s_y, e_x, e_y)

 


#########################################
# Perform

# def perform(level, box, options):
#     global tm
#     tm = detectMap(level, box, options)
#     global width
#     width = box.maxx - box.minx
#     global height
#     height = box.maxz - box.minz
#     tm_to_test_map()
#     find_path(box)
#     print_test_map()
#     #clearTerrain(level,box)
#     for i in range(len(test_map)):
#         for j in range(len(test_map[0])):
#             if(test_map[i][j] == '*'):
#                 print i,j
#                 #utilityFunctions.setBlock(level, (options["Road Material"].ID, 0), box.minx + j, box.miny, box.minz + i)
#                 utilityFunctions.setBlockToGround(level, (options["Road Material"].ID, 0), box.minx + j, box.maxy, box.minz + i, box.miny)

def clearTerrain(level, box):
    for x in range(box.minx, box.maxx):
        # let's assume we won't build things taller tidentityhan 50 blocks
        for y in range(box.miny, box.miny + 50):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, z)
                
     

def buildRoad(level, box, options):
    # start_point = options["Start Point"]
    # end_point = options["End Point"]
    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz

    blocks = zeros((width, height, depth))
    dmgs = zeros((width, height, depth))

    cache = {}

    # Use two points in one level to create Road.
    start_x = box.minx
    start_y = box.miny
    end_x = box.maxx
    end_y = box.maxy


def detectMap(level, box, options, house_matrix):
    ground = box.miny
    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz
    # treeMap = utilityFunctions.treeMap(level, box)
    houseMap = house_matrix
    matrix = [['.' for temp_x in range(width)] for temp_y in range(depth)]
    # for i in range(len(houseMap)):
    #     for j in range(len(houseMap[0])):
    #         if(houseMap[i][j] > 1):
    #             matrix[i][j] = '#'
    matrix[0][0] = 'S'
    matrix[len(houseMap) - 1][len(houseMap[0]) - 1] = 'E'
    return matrix




