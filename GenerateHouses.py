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
    ("Max Height", 50)
)

matrix = [[(0,0),(0,0),(0,0)]]
matrix.append([(0,0)])
print matrix

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
    box = BoundingBox((box.minx,minY,box.minz),(box.width, options["Max Height"], box.length))   
    utilityFunctions.fillBox(level, box, (0,0))
    
    utilityFunctions.fillLayer(level, box, 0, (alphaMaterials.Grass.ID,0))
    (houses, roads) = idonknowPartition(box)
    for house in houses:
        chooseHouse(level, CutBar(house,2,2,2,2).middle, options)
        #utilityFunctions.fillBox(level, CutBar(house,2,2,2,2).middle, (random.randint(40,80),0))
        #buildSimpleFarmHouse(level, CutBar(house,2,2,2,2).middle, options)
        #buildFence(level, house, options)
    for road in roads:
    
        utilityFunctions.fillBox(level, road,(208,0))
        utilityFunctions.fillBox(level,CutBar(road,0,0,0,0,options["Max Height"],2).middle,(0,0))
    #buildSimpleFarmHouse(level, box, options)

#require box at least 10*10
def buildSimpleFarmHouse(level, box, options):
    #fencesBox = CutBar(box,1,1,1,1,boxSize[1]).middle
    #baseBox = CutBar(fencesBox, 2,2,2,2, boxSize[1]).middle
    #build fences and base
    #fenceLeft, fenceRight,fenceFront, fenceBack = buildFence(level, fencesBox, options,1) 
    centerX = (box.minx+box.maxx)//2
    centerZ = (box.minz + box.minz)//2
    for y in range(0, 250):
        if level.blockAt(centerX, y, centerZ) != 0 and level.blockAt(centerX, y+1, centerZ)==0:
            minY = y
            break
    
    box = BoundingBox((box.minx, minY+1, box.minz),(box.width, box.height, box.length))
    utilityFunctions.fillBox(level, CutBar(box,0,0,0,0,options["Max Height"],2).middle,(0,0))

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
    for i in range(0, height):
        layer = BoundingBox((box.minx,box.miny+i,box.minz),(boxSize[0],1,boxSize[2]))
        utilityFunctions.fillBoxEmpty(level,CutBar(layer,i,i,i,i).middle,(block,data))
        #makeFloor(level, CutBar(layer,i,i,i,i).middle, options)
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
        buildSimpleFarmHouse(level, box, options)

    else:
        buildFarm()

def makeFloor(level, box, options):
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(level,(options["Base"].ID, 0),x,box.miny, z)

def buildFarm():
    pass       

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

'''
#build the house stair and return the bottom box
def afterBuildHouseBase(level,box,(block,data),height):
    boxSize = utilityFunctions.getBoxSize(box)
    for i in range(0, height):
        layer = BoundingBox((box.minx,box.miny+i,box.minz),(boxSize[0],1,boxSize[2]))
        utilityFunctions.fillBox(level,CutBar(layer,i,i,i,i).middle,(block,data))
        #makeFloor(level, CutBar(layer,i,i,i,i).middle, options)
    layer = BoundingBox((box.minx,box.miny+height,box.minz),(boxSize[0],1,boxSize[2]))
    return CutBar(layer,height,height,height,height,boxSize[1]-height).middle
'''