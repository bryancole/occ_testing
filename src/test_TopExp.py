from OCC import TopExp, BRepPrimAPI, TopAbs, TopoDS

box = BRepPrimAPI.BRepPrimAPI_MakeBox(10., 20., 30.)
ex = TopExp.TopExp_Explorer(box.Shape(), TopAbs.TopAbs_EDGE)

results = []

while ex.More():
    shape = TopoDS.TopoDS().Edge(ex.Current())
    print "is null?", bool(shape.IsNull())
    results.append(shape)
    ex.Next()
ex.ReInit()
    
    
for edge in results:
    print "null now?", bool(edge.IsNull())
    