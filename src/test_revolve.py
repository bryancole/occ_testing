from OCC import BRepPrimAPI, Geom, gp, BRepBuilderAPI
from viewer import view
from math import pi

el = gp.gp_Elips(gp.gp_Ax2(gp.gp_Pnt(0,0,0), gp.gp_Dir(1,0,0)), 
                          20.0, 10.0)
edge1 = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(el, 
                                              gp.gp_Pnt(0,0,20),
                                              gp.gp_Pnt(0,0,-20))
edge2 = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(gp.gp_Pnt(0,0,-20),
                                              gp.gp_Pnt(0,0,20))

wire = BRepBuilderAPI.BRepBuilderAPI_MakeWire()
wire.Add(edge1.Edge())
wire.Add(edge2.Edge())

face = BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire.Wire())

el = BRepPrimAPI.BRepPrimAPI_MakeRevol(face.Shape(), 
                                       gp.gp_Ax1(gp.gp_Pnt(0,0,0),
                                                 gp.gp_Dir(0,0,1)),
                                       pi*2)

#h_curve = Geom.Handle_Geom_Ellipse(curve)
#rev = BRepPrimAPI.BRepPrimAPI_MakeRevolution(h_curve, 120.1)
##nurbs = BRepBuilderAPI.BRepBuilderAPI_NurbsConvert(rev.Shape())
view(el.Shape())

