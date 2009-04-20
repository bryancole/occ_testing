import os
os.environ['CSF_GraphicShr'] = r"/usr/local/lib/libTKOpenGl.so"

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.BRepFilletAPI import BRepFilletAPI_MakeChamfer

from OCC.Utils import Topology

from OCC import TopExp, TopAbs, TopoDS, BRepBuilderAPI

import itertools

box = BRepPrimAPI_MakeBox(10.0,20.0,30.0).Shape()

topo = Topology.Topo(box)

edge_ids = [1,2,3,5]

chamf = BRepFilletAPI_MakeChamfer(box)

def iedges():
    ex = TopExp.TopExp_Explorer(box, TopAbs.TopAbs_EDGE)
    while ex.More():
        shape = ex.Current()
        shape._builder = ex
        yield shape
        #e = TopoDS.TopoDS().Edge( shape )
        #e._shape = shape
        #yield e
        ex.Next()

edges = lambda : list(itertools.islice(iedges(),0,10))
#edges = iedges

for i, s in enumerate(edges()):
    if i in edge_ids:
        edge = TopoDS.TopoDS().Edge(s)
        face = topo.faces_from_edge(edge).next()
        print i, face
        chamf.Add(2.,2., edge, face)

print "build"
chamf.Build()

print "success", chamf.IsDone()


from OCC.Display.wxSamplesGui import display, start_display
display.DisplayShape(chamf.Shape())
start_display()


