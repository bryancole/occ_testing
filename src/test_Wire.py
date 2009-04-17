from OCC import BRepBuilderAPI, gp, STEPControl
from itertools import izip, tee

def pairs(itr):
    a,b = tee(itr)
    b.next()
    return izip(a,b)

points = [(0,0,0),
          (1,1,1),
          (0,0,-2),
          (0,2,0)]

vertices = [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(gp.gp_Pnt(*p))
            for p in points]
#print "verts", vertices
#edges = [BRepBuilderAPI.BRepBuilderAPI_MakeEdge(v1.Vertex(),v2.Vertex())
#         for v1,v2 in pairs(vertices)]
v=vertices
edges = [BRepBuilderAPI.BRepBuilderAPI_MakeEdge(v[i].Vertex(),v[j].Vertex())
         for i,j, in [(0,1),(0,2),(0,3)] ]
         

#print "edges", edges
wire = BRepBuilderAPI.BRepBuilderAPI_MakeWire()
for e in edges:
    wire.Add(e.Edge())
    
print wire

step_export = STEPControl.STEPControl_Writer()
step_export.Transfer(wire.Shape(), STEPControl.STEPControl_AsIs)
step_export.Write("/home/bryan/test_wire.stp")