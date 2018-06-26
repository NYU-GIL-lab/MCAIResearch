# Build Road
# 1.create a simple road between two points
# problem: how to see two points location in the map.
import untilityFunctions

inputs = (
    ("Road Build Example", "label")
    ("Road Material", alphaMaterials.Cobblestone),  # the material we want to use to build the mass of the structures
    ("Bridge Material", alphaMaterials.Wood),
    # ("Start Point - X", ()),
    # ("Start Point - Y", ()),
    # ("Start Point - Z", ()),
    # ("End Point - X", ()),
    # ("End Point - Y", ()),
    # ("End Point - Z", ()),
    ("Creator: Changxing Cao", "label"),
)



def perform(level, box, options):
    buildRoad(level, box options)

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

    for dx in xrange(width):
        for dy in xrange(height):
            for dz in xrange(depth):
                x = box.minx + dx
                y = box.miny + dy
                z = box.minz + dz

def detectMap(level, box, options):
    ground = box.miny
    width = box.maxx - box.minx
    height = box.maxy - box.miny
    depth = box.maxz - box.minz
    treeMap = untilityFunctions.treeMap(level, box)
    map = zeros((width, height, depth))
    for dx in xrang(width):
        for dz in xrange(depth):






    # A Star Algorithm
#     A星算法伪码：
# a、将开始点记录为当前点P
# b、将当前点P放入封闭列表
# c、搜寻点P所有邻近点，假如某邻近点既没有在开放列表或封闭列表里面，则计算出该邻近点的F值，并设父节点为P，然后将其放入开放列表
# d、判断开放列表是否已经空了，如果没有说明在达到结束点前已经找完了所有可能的路径点，寻路失败，算法结束；否则继续。
# e、从开放列表拿出一个F值最小的点，作为寻路路径的下一步。
# f、判断该点是否为结束点，如果是，则寻路成功，算法结束；否则继续。
# g、将该点设为当前点P，跳回步骤c。
