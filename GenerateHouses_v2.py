import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import*
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

from mcplatform import *

import utilityFunctions as utilityFunctions

#input   
inputs = (
    ("House example", "label"),
    ("Base", alphaMaterials.Cobblestone),
    ("Wall", alphaMaterials.Cobblestone),
    ("Roof", alphaMaterials.Wood),
    ("Max Height", 50),
    ("Road Build Example", "label"),
    ("Road Material", alphaMaterials.Purpur),  # the material we want to use to build the mass of the structures
    ("Bridge Material", alphaMaterials.Wood),
)

# matrix = [[(0,0),(0,0),(0,0)]]
# matrix.append([(0,0)])
# print matrix

# Build Road
# 1.create a simple road between two points
# problem: how to see two points location in the map.


# -*- coding: utf-8 -*-

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
    matrix = house_matrix
    # matrix = [['.' for temp_x in range(width)] for temp_y in range(depth)]
    # for i in range(len(houseMap)):
    #     for j in range(len(houseMap[0])):
    #         if(houseMap[i][j] > 1):
    #             matrix[i][j] = '#'
    for i in range(len(matrix[0])):
        if matrix[0][i] == '.':
            matrix[0][i] = 'S'
            break
    for j in range(len(matrix[0])):
        if matrix[len(matrix) - 1][len(matrix[0]) - 1 - j] == '.':
            matrix[len(matrix) - 1][len(matrix[0]) - 1 - j] = 'E'
            break
            # matrix[len(matrix) - 1][len(matrix[0]) - 1] = 'E'
    return matrix







class CutBar(object):
    def __init__(self, box, recessLeft,recessRight,recessFront,recessBack,height = 1,offSetY = 0):
        boxSize = utilityFunctions.getBoxSize(box)
        middle = BoundingBox((box.minx+recessLeft,box.miny+offSetY,box.minz+recessFront),(boxSize[0]-recessLeft-recessRight,height,boxSize[2]-recessFront-recessBack))
        leftBar = BoundingBox((box.minx, box.miny+offSetY, box.minz+recessFront),(recessLeft, height, boxSize[2]-recessFront))
        rightBar = BoundingBox((box.maxx-recessRight, box.miny+offSetY, box.minz),(recessRight,height,boxSize[2]-recessBack))
        backBar = BoundingBox((box.minx+recessLeft,box.miny+offSetY,box.maxz-recessBack),(boxSize[0]-recessLeft,height,recessBack))
        frontBar = BoundingBox((box.minx,box.miny+offSetY,box.minz),(boxSize[0]-recessRight,height,recessFront))
        
        cornorLF = BoundingBox((box.minx,box.miny+offSetY,box.minz),(recessLeft,height,recessFront))
        cornorLB = BoundingBox((box.minx,box.miny+offSetY,box.maxz-recessBack),(recessLeft,height,recessBack))
        cornorRF = BoundingBox((box.maxx-recessRight,box.miny+offSetY,box.minz),(recessRight,height,recessFront))
        cornorRB = BoundingBox((middle.maxx,box.miny+offSetY,middle.maxz),(recessRight,height,recessBack))

        self.left = leftBar
        self.right = rightBar
        self.front = frontBar
        self.back = backBar
        self.cornorLF = cornorLF
        self.cornorLB = cornorLB
        self.cornorRF = cornorRF
        self.cornorRB = cornorRB
        self.middle = middle
       
class AddBar(object):
    def __init__(self, box, addLeft,addRight,addFront,addBack,height = 1, offSetY=0):
        boxSize = utilityFunctions.getBoxSize(box)
        fullBox = BoundingBox((box.minx-addLeft,box.miny+offSetY,box.minz-addBack),(boxSize[0]+addLeft+addRight,height,boxSize[2]+addFront+addBack))
        leftBar = BoundingBox((fullBox.minx, box.miny+offSetY, fullBox.minz),(addLeft, height, boxSize[2]+addFront))
        rightBar = BoundingBox((box.maxx, box.miny+offSetY, box.minz),(addRight,height,boxSize[2]+addBack))
        backBar = BoundingBox((fullBox.minx,box.miny+offSetY,box.maxz+addFront),(boxSize[0]+addLeft,height,addBack))
        frontBar = BoundingBox((box.minx,box.miny+offSetY,fullBox.minz),(boxSize[0]+addRight,height,addFront))
        
        cornorLF = BoundingBox((fullBox.minx,box.miny+offSetY,fullBox.minz),(addLeft,height,addFront))
        cornorLB = BoundingBox((fullBox.minx,box.miny+offSetY,box.maxz),(addLeft,height,addBack))
        cornorRF = BoundingBox((box.maxx, box.miny+offSetY, fullBox.minz),(addRight,height,addFront))
        cornorRB = BoundingBox((box.maxx,box.miny+offSetY,box.maxz),(addRight,height,addBack))
        
        self.left = leftBar
        self.right = rightBar
        self.front = frontBar
        self.back = backBar
        self.full = fullBox

        self.cornorLF = cornorLF
        self.cornorLB = cornorLB
        self.cornorRF = cornorRF
        self.cornorRB = cornorRB

def getPlanMatrix(level,box, houses):
    matrix = [['.' for j in range(box.width)] for i in range(box.length)]
    for house in houses:
        for x in range(house.minx, house.maxx):
            for z in range(house.minz, house.maxz):
                matrix[z-box.minz][x-box.minx] = '#'
    for line in matrix:
        print ''.join(line)
    return box, matrix

def findBottom(level, box):
    centerX = (box.minx+box.maxx)//2
    centerZ = (box.minz + box.minz)//2
    for y in range(250, 0, -1):
        if level.blockAt(centerX, y, centerZ) != 0 and level.blockAt(centerX, y+1, centerZ)==0:
            minY = y
            break
    return minY

#perform function
#each sunbBox = (BounddingBox, houseType)
def perform(level, box, options):
    minY = findBottom(level, box)
    fillBox = BoundingBox((box.minx,box.miny,box.minz),(box.width, max(minY-box.miny,1), box.length)) 
    box = BoundingBox((box.minx,minY,box.minz),(box.width, options["Max Height"], box.length))   
    utilityFunctions.fillBox(level, box, (0,0))   
    utilityFunctions.fillBoxEmpty(level, fillBox, (alphaMaterials.Grass.ID,0))

    (houses, roads) = idonknowPartition(box)
    test, house_matrix =getPlanMatrix(level, box, houses)
    for house in houses:
        chooseHouse(level, house , options)
    for road in roads:
        utilityFunctions.fillBox(level, road,(208,0))
        utilityFunctions.fillBox(level,CutBar(road,0,0,0,0,options["Max Height"],1).middle,(0,0))


    ##########################
    # build road
    # house_matrix = getPlanMatrix(level, box, houses)
    global tm
    tm = detectMap(level, box, options, house_matrix)
    global width
    width = box.maxx - box.minx
    global height
    height = box.maxz - box.minz
    tm_to_test_map()
    find_path(box)
    print_test_map()
    #clearTerrain(level,box)
    for i in range(len(test_map)):
        for j in range(len(test_map[0])):
            if(test_map[i][j] == '*'):
                print i,j
                utilityFunctions.setBlock(level, (options["Road Material"].ID, 0), box.minx + j, box.miny, box.minz + i)
                if box.minx + j + 1 < box.maxx:
                    utilityFunctions.setBlock(level, (options["Road Material"].ID, 0), box.minx + j + 1, box.miny, box.minz + i)
                if box.minz + i + 1 < box.maxz:
                    utilityFunctions.setBlock(level, (options["Road Material"].ID, 0), box.minx + j, box.miny, box.minz + i + 1)
                ##
                # utilityFunctions.setBlockToGround(level, (options["Road Material"].ID, 0), box.minx + j, box.maxy, box.minz + i, box.miny)
                # why set to ground will up to the high location???



#require box at least 10*10
def buildSimpleFarmHouse(level, box, options):
    wallPartBox = buildBase(level,box,(options["Base"].ID, 0), 1)
    floorBoxes = buildWall(level, wallPartBox,(options["Base"].ID, 0), random.randint(5,25))
    
    for i in range(size(floorBoxes)-1):
        fillFrame(level, floorBoxes[i], (45,0), floorBoxes[i].height)
    #build the wall of the house
    if size(floorBoxes)>=2:
        buildRoof(level,AddBar(floorBoxes[-1],2,2,3,3).full, (options["Roof"].ID, 0),1, 10) 
    else:
        buildRoof(level,AddBar(floorBoxes[-1],2,2,3,3).full, (options["Roof"].ID, 0),1, 1)

def buildFence(level, box, options, buildFenceHightRange=1):
    boxSize = utilityFunctions.getBoxSize(box)
    if min(boxSize[0],boxSize[1]) < 2:
        return box,box,box,box
    fenceLeft  =  CutBar(box, 1,1,0,0,buildFenceHightRange).left
    fenceRight =  CutBar(box, 1,1,0,0,buildFenceHightRange).right
    fenceFront =  CutBar(box, 0,0,1,1,buildFenceHightRange).front
    fenceBack  =  CutBar(box, 0,0,1,1,buildFenceHightRange).back

    utilityFunctions.fillLayerEmpty(level,fenceLeft,0,(85,0))
    utilityFunctions.fillLayerEmpty(level,fenceRight,0,(85,0))
    utilityFunctions.fillLayerEmpty(level,fenceFront,0,(85,0))
    utilityFunctions.fillLayerEmpty(level,fenceBack,0,(85,0))
    return fenceLeft, fenceRight,fenceFront, fenceBack

def buildBase(level, box, (block,data),height):
    boxSize = utilityFunctions.getBoxSize(box)
    for i in range(height):
        layer = BoundingBox((box.minx,box.miny+i+1,box.minz),(boxSize[0],1,boxSize[2]))
        utilityFunctions.fillBoxEmpty(level,CutBar(layer,i,i,i,i).middle,(block,data))

    layer = BoundingBox((box.minx,box.miny+height,box.minz),(boxSize[0],1,boxSize[2]))
    
    return CutBar(layer,height,height,height,height,boxSize[1]-height).middle

def buildWall(level, box, (block,data), height, floorInterVal=5):
    floorBoxes = []
    curBottom = 0
    floorHeight = random.randint(floorInterVal, floorInterVal+3)
    floorBoxes.append(BoundingBox((box.minx, box.miny+curBottom, box.minz),(box.width, floorHeight, box.length)))
    while height - curBottom > floorInterVal:       
        #utilityFunctions.fillLayer(level,AddBar(box,1,1,1,1).full, curBottom, (block,data))
        floorBoxes.append(BoundingBox((box.minx, box.miny+curBottom, box.minz),(box.width, floorHeight, box.length)))
        curBottom += floorHeight
        floorHeight = random.randint(floorInterVal, floorInterVal+3)
    
    floorBoxes.append(BoundingBox((box.minx, box.miny+curBottom, box.minz),(box.width, max(height-curBottom,1), box.length)))
    return floorBoxes

def fillFrame(level, box, (block,data), height):
    wallBoxSize = utilityFunctions.getBoxSize(box)
    leftWall  =  CutBar(box, 1,1,0,0, height-1).left
    rightWall =  CutBar(box, 1,1,0,0, height-1).right
    frontWall =  CutBar(box, 0,0,1,1, height-1).front
    backWall  =  CutBar(box, 0,0,1,1, height-1).back
    topFloor = AddBar(box,2,2,2,2,1,height-1).full

    for j in range(leftWall.length):
        colL = BoundingBox((leftWall.minx, leftWall.miny, leftWall.minz+j),(1, leftWall.height,1))
        colR = BoundingBox((rightWall.minx, rightWall.miny, rightWall.minz+j),(1, rightWall.height,1))
        if j%4 == 2:
            utilityFunctions.fillBox(level,colL,(5,5))
            utilityFunctions.fillBox(level,colR,(5,5))
        else:
            utilityFunctions.fillBox(level,colL,(45,0))
            utilityFunctions.fillBox(level,colR,(45,0))

    for i in range(frontWall.width):
        colF = BoundingBox((frontWall.minx+i, frontWall.miny, frontWall.minz),(1, frontWall.height,1))
        colB = BoundingBox((backWall.minx+i, backWall.miny, backWall.minz),(1, backWall.height,1))
        if i%4 == 0:
            utilityFunctions.fillBox(level,colF,(5,5))
            utilityFunctions.fillBox(level,colB,(5,5))
        else:
            utilityFunctions.fillBox(level,colF,(45,0))
            utilityFunctions.fillBox(level,colB,(45,0))

    for i in range(0,leftWall.height-1,3):  
        frameBar = CutBar(box,1,1,1,1,1,i)
        utilityFunctions.fillBox(level,frameBar.left,(5,5))
        utilityFunctions.fillBox(level,frameBar.right,(5,5))
        utilityFunctions.fillBox(level,frameBar.front,(5,5))
        utilityFunctions.fillBox(level,frameBar.back,(5,5))

    cornorBox = AddBar(box, 1,1,1,1,height-1)
    LF =  cornorBox.cornorLF
    LB =  cornorBox.cornorLB
    RF =  cornorBox.cornorRF
    RB =  cornorBox.cornorRB  

    utilityFunctions.fillBox(level,LF,(5,5))
    utilityFunctions.fillBox(level,LB,(5,5))
    utilityFunctions.fillBox(level,RF,(5,5))
    utilityFunctions.fillBox(level,RB,(5,5))

    utilityFunctions.fillBox(level,topFloor,(5,5))
    return leftWall, rightWall, frontWall, backWall, topFloor 

def buildRoof(level, box, (block,data), minHeight=1, maxHeight=5):
    roofHeight = random.randint(minHeight,maxHeight)
    for i in range(0, roofHeight):
        utilityFunctions.fillLayer(level, CutBar(box,0,0,i,i).middle, i, (block,data))

#only to front wall
def drillDoorCenter(level, box, doorWidth,doorHeight):
    halfWidth = doorWidth // 2
    centerBox = utilityFunctions.getCenterBoundingBox(box)
    centerBox = BoundingBox((centerBox.minx, box.miny, centerBox.minz),(centerBox.width, box.height, centerBox.length))
    doorSpace = AddBar(centerBox, halfWidth, halfWidth, 0, 0 ,doorHeight).full
    return doorSpace

def chooseHouse(level, box,options):
    area = box.width*box.length
    length = box.length
    width = box.width
    if min(length, width) >=8:
        hbox = CutBar(box,2,2,2,2)
        buildSimpleFarmHouse(level, hbox.middle, options)
        utilityFunctions.fillLayer(level,hbox.left,0,(options["Base"].ID, 0))
        utilityFunctions.fillLayer(level,hbox.right,0,(options["Base"].ID, 0))
        utilityFunctions.fillLayer(level,hbox.front,0,(options["Base"].ID, 0))
        utilityFunctions.fillLayer(level,hbox.back,0,(options["Base"].ID, 0))

    else:
        buildFarm(level, box,options)

def makeFloor(level, box, options):
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(level,(options["Base"].ID, 0),x,box.miny, z)

def buildFarm(level, box,options):
    buildFence(level, box, options)
    garden = CutBar(box,1,1,1,1,box.height).middle
    for x in range(garden.minx, garden.maxx):
        for z in range(garden.minz, garden.maxz):
            utilityFunctions.setBlock(level, (59,0), x, garden.miny, z)

def makePyramid(level, box, options, floors):
    [cx,cy,cz]=[(box.minx+box.maxx)/2, (box.miny+box.maxy)/2, (box.minz+box.maxz)/2]
    boxSize = utilityFunctions.getBoxSize(box)
    minWidth = min(boxSize[0], boxSize[2])
    step = 2
    count=0
    for floor in range(floors-1):
        subBox = BoundingBox((box.minx+floor,floor+box.miny,box.minz+floor),(boxSize[0]-step*floor, 1, boxSize[2]-step*floor))
        if subBox.width>1 and subBox.length>1:
            utilityFunctions.setSquareFrame(level,(options["Wall"].ID,0), subBox.minx, subBox.miny, subBox.minz, subBox.length,subBox.width)    
            count += 1
        else: 
            break
    subBox = BoundingBox((box.minx+count,count+box.miny,box.minz+count),(boxSize[0]-step*count, 1, boxSize[2]-step*count))
    print subBox
    makeFloor(level, subBox, options)
        
def makeWall(level, box, options):
    #1 find edges
        boxSize = utilityFunctions.getBoxSize(box)
        minimumWidth = min(boxSize[0],boxSize[2])
        minimumWidth = max( minimumWidth, 6)
        height = random.randint(5,minimumWidth)
        for x in range(box.minx+1, box.maxx-1):
            utilityFunctions.setBlockToGround(level, (options["Wall"].ID, 0),x,box.miny+height,box.minz, box.miny)
            utilityFunctions.setBlockToGround(level, (options["Wall"].ID, 0),x,box.miny+height,box.maxz-1, box.miny )
    
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlockToGround(level, (options["Wall"].ID,0), box.minx,   box.miny+height, z, box.miny)
            utilityFunctions.setBlockToGround(level, (options["Wall"].ID,0), box.maxx-1, box.miny+height, z, box.miny)
    #2 build wall

def cleanTerrain(level, box, options):
    #upperLayer #the flat part of the box
    #bottomLayer#the unflatten bottom of the box
    pass
def binaryPartition(box):
	partitions = []
	# create a queue which holds the next areas to be partitioned
	queue = []
	queue.append(box)
	# for as long as the queue still has boxes to partition...
	count = 0
	while len(queue) > 0:
		count += 1
		splitMe = queue.pop(0)
		(width, height, depth) = utilityFunctions.getBoxSize(splitMe)
		print "Current partition width,depth",width,depth 
		centre = 0
		# this bool lets me know which dimension I will be splitting on. It matters when we create the new outer bound size
		isWidth = False
		# find the larger dimension and divide in half
		# if the larger dimension is < 10, then block this from being partitioned
		minSize = 24
		#we choose the longer side to split
		if width > depth: 
			# roll a random die, 1% change we stop anyways
			chance = random.randint(100)

			if depth < minSize or chance == 1:
				partitions.append(splitMe)
				continue

			isWidth = True
			centre = width / 2
		else:
			chance = random.randint(10)
			if width < minSize or chance == 1:
				partitions.append(splitMe)
				continue				
			centre = depth / 2

		# a random modifier for binary splitting which is somewhere between 0 and 1/16 the total box side length
		randomPartition = random.randint(0, (centre / 8) + 1)

		# creating the new bound
		newBound = centre + randomPartition

		#creating the outer edge bounds
		outsideNewBounds = 0
		if isWidth:
			outsideNewBound = width - newBound - 1
		else:
			outsideNewBound = depth - newBound - 1

		# creating the bounding boxes
		# NOTE: BoundingBoxes are objects contained within pymclevel and can be instantiated as follows
		# BoundingBox((x,y,z), (sizex, sizey, sizez))
		# in this instance, you specifiy which corner to start, and then the size of the box dimensions
		# this is an if statement to separate out binary partitions by dimension (x and z)
		if isWidth:
			queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz), (newBound-1, 256, depth)))
			queue.append(BoundingBox((splitMe.minx + newBound + 1, splitMe.miny, splitMe.minz), (outsideNewBound - 1, 256, depth)))
		else:
			queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz), (width, 256, newBound - 1)))
			queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz + newBound + 1), (width, 256, outsideNewBound - 1)))
	return partitions

def idonknowPartition(box):
    HousePartitions = []
    RoadPartitions  = []
    queue = []
    queue.append(box)
    count = 0
    while len(queue)>0:
        curBox = queue.pop(0)
        length = curBox.length
        width = curBox.width

        roadw = min(ceil(0.1*width),10)
        roadl = min(ceil(0.1*length),10)
        remainLR = max(width - roadw,1)
        remainFB = max(length - roadl,1)

        if roadl<2 and roadw<2:
            HousePartitions.append(curBox)
            continue

        if random.randint(100)<=10:
            HousePartitions.append(curBox)
            continue
        else:       
            front = 0
            back = 0
            left = 0
            right = 0
            front = floor(random.uniform(0.3,0.7)*remainFB)
            back = max(remainFB  - front,0)
            left  = floor(random.uniform(0.3,0.7)*remainLR)
            right = max(remainLR - left,0)

            if front >5 and back>5 and left >5 and right >5:
                nextBox = CutBar(curBox,left,right,front,back,curBox.height)   
                cLF = nextBox.cornorLF 
                cLB = nextBox.cornorLB
                cRF = nextBox.cornorRF
                cRB = nextBox.cornorRB
                queue.append(nextBox.cornorLF)
                queue.append(nextBox.cornorLB)
                queue.append(nextBox.cornorRF)
                queue.append(nextBox.cornorRB)
                roadLRBox = CutBar(curBox, 0,0,front,back)
                RoadPartitions.append(roadLRBox.middle)
                roadFBBox = CutBar(curBox,left,right,0,0)
                RoadPartitions.append(roadFBBox.middle)
            
            elif front >5 and back>5 and min(left,right)<=5:
                nextBox = CutBar(curBox,0,0,front,back,curBox.height)   
                bF = nextBox.front 
                bB = nextBox.back
                queue.append(nextBox.front)
                queue.append(nextBox.back)
                roadLRBox = CutBar(curBox, 0,0,front,back)
                RoadPartitions.append(roadLRBox.middle)
            
            elif left >5 and right>5 and min(front,back)<=5:
                nextBox = CutBar(curBox,left,right,0,0,curBox.height)   
                bL = nextBox.left
                bR = nextBox.right
                queue.append(nextBox.left)
                queue.append(nextBox.right)
                roadLRBox = CutBar(curBox,left,right,0,0)
                RoadPartitions.append(roadLRBox.middle)

            else:
                HousePartitions.append(curBox)




    return HousePartitions, RoadPartitions
