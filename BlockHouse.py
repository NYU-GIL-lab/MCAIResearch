import time  # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import utilityFunctions as utilityFunctions

# inputs are taken from the user. Here I've just showing labels, as well as letting the user define
# what the main creation material for the structures is
inputs = (
    ("Blocky house example", "label"),
    ("Wall Material", alphaMaterials.Cobblestone),  # the material we want to use to build the mass of the structures
    ("Roof Material", alphaMaterials.Wood),
    ("Creator: Marco Scirea", "label"),
)


# MAIN SECTION #
# Every agent must have a "perform" function, which has three parameters
# 1: the level (aka the minecraft world). 2: the selected box from mcedit. 3: User defined inputs from mcedit
def perform(level, box, options):
    # clear selection in case there is already something there
    clearTerrain(level,box)
    makeFloor(level,box,options)
    height = makeWall(level, box, options)
    makeRoof(level, box, options, height)

def makeFloor(level, box, options):
    # make floor
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(level, (options["Roof Material"].ID, 0), x, box.miny, z)

def makeWall(level,box, options):
    # make walls
    boxSize = utilityFunctions.getBoxSize(box)
    minimumWidth = min(boxSize[0], boxSize[2])
    minimumWidth = max(minimumWidth, 6);
    height = random.randint(5, minimumWidth)
    for x in range(box.minx, box.maxx):
        utilityFunctions.setBlockToGround(level, (options["Wall Material"].ID, 0), x, box.miny + height, box.minz, box.miny)
        utilityFunctions.setBlockToGround(level, (options["Wall Material"].ID, 0), x, box.miny + height, box.maxz-1, box.miny)
    for z in range(box.minz, box.maxz):
        utilityFunctions.setBlockToGround(level, (options["Wall Material"].ID, 0), box.maxx-1, box.miny + height, z, box.miny)
        utilityFunctions.setBlockToGround(level, (options["Wall Material"].ID, 0), box.minx, box.miny + height, z, box.miny)
    return height

def makeRoof(level,box,options,height):
    # make sloped roof
    smallx = box.minx
    bigx = box.maxx-1
    addedHeight = 1
    while smallx <= bigx:
        for z in range(box.minz, box.maxz):
            if z == box.minz or z == box.maxz -1:
                utilityFunctions.setBlockToGround(level, (options["Roof Material"].ID, 0), smallx, box.miny + height + addedHeight, z,
                                              box.miny)
                utilityFunctions.setBlockToGround(level, (options["Roof Material"].ID, 0), bigx, box.miny + height + addedHeight,
                                              z, box.miny)
            else:
                utilityFunctions.setBlock(level, (options["Roof Material"].ID, 0), smallx,
                                                  box.miny + height + addedHeight-1, z)
                utilityFunctions.setBlock(level, (options["Roof Material"].ID, 0), bigx,
                                                  box.miny + height + addedHeight-1,
                                                  z)
        smallx+=1
        bigx-=1
        addedHeight+=1


def clearTerrain(level, box):
    for x in range(box.minx, box.maxx):
        # let's assume we won't build things taller than 50 blocks
        for y in range(box.miny, box.miny + 50):
            for z in range(box.minz, box.maxz):
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, z)
