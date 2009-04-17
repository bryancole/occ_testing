from OCC import BRepPrimAPI, BRep, STEPControl, TopoDS, gp, \
        BRepBuilderAPI, BRepAlgoAPI, BRepOffsetAPI
from itertools import izip, tee
import itertools
import numpy

from viewer import view


def pairs(itr):
    a,b = tee(itr)
    b.next()
    return izip(a,b)

def MakeVertex(pt): 
    bd = BRepBuilderAPI.BRepBuilderAPI_MakeVertex(gp.gp_Pnt(*pt))
    return bd
    
def MakeEdge(v1, v2):
    bd = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(v1.Vertex(), v2.Vertex())
    return bd

def MakeWire(edgeList):
    bd = BRepBuilderAPI.BRepBuilderAPI_MakeWire()
    for e in edgeList:
        bd.Add(e.Edge())
    return bd

points1 = [(-1,-1,0),
          (1,-1,0),
          (1,1,0),
          (-1,1,0)]

verts1 = [MakeVertex(pt) for pt in points1]

edges1 = [MakeEdge(v1,v2) for v1,v2 in pairs(verts1)]
edges1.append(MakeEdge(verts1[-1], verts1[0]))

wire1 = MakeWire(edges1)

points2 = [(-1,-1,4),
          (1,-1,4),
          #(1.3,0,4),
          (1,1,4),
          (-1,1,4)]

verts2 = [MakeVertex(pt) for pt in points2]

edges2 = [MakeEdge(v1,v2) for v1,v2 in pairs(verts2)]
edges2.append(MakeEdge(verts2[-1], verts2[0]))

wire2 = MakeWire(edges2)

section = BRepOffsetAPI.BRepOffsetAPI_ThruSections(True)
section.AddVertex(MakeVertex((0,0,-1)).Vertex())
section.AddWire(wire1.Wire())
section.AddWire(wire2.Wire())
section.AddVertex(MakeVertex((0,0,5)).Vertex())

view(section.Shape())
