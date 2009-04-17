from OCC import BRepBuilderAPI, gp, STEPControl, BRepOffsetAPI, GeomAbs
from itertools import izip, tee
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

#points = [(0,0,-1),
#          (0,0,0),
#          (0,1,1),
#          (1,1,2),
#          (1,0,3),
#          (0,0,3.1)]

points = [(0,0,0),
          (1,1,2)]

vertices = [MakeVertex(p) for p in points]

edges = [MakeEdge(v1,v2) for v1,v2 in pairs(vertices)]
         
spine = MakeWire(edges)
    
s = 0.2
pts = [(-s,s,0),
       (s,s,0),
       (s,-s,0),
       (-s,-s,0)]

vs = [MakeVertex(p) for p in pts]
vs.append(vs[0])

es = [MakeEdge(v1,v2) for v1,v2 in pairs(vs)]

ws = MakeWire(es)

face = BRepBuilderAPI.BRepBuilderAPI_MakeFace(ws.Wire())

#pipe = BRepOffsetAPI.BRepOffsetAPI_MakeEvolved(face.Face(), spine.Wire(),
#                                               3)
#pipe.SetMode(gp.gp_Dir(0,0,1))
#pipe.Add(ws.Shape(), False, True)

pipe = BRepOffsetAPI.BRepOffsetAPI_MakePipe(spine.Wire(), face.Shape())

view(pipe.Shape())
print "end"

#step_export = STEPControl.STEPControl_Writer()
#step_export.Transfer(pipe.Shape(), STEPControl.STEPControl_AsIs)
#step_export.Write("/home/bryan/test_pipe.stp")