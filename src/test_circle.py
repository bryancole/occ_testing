from OCC import Geom, BRepBuilderAPI, gp
from viewer import view
import numpy

curvature = 50.0

ax = gp.gp_Ax2(gp.gp_Pnt(0,0,0),
                    gp.gp_Dir(0,1,0),
                    gp.gp_Dir(1,0,0))
circ = Geom.Geom_Circle(ax, curvature)
h_circ = Geom.Handle_Geom_Circle(circ)

angle=1.3
p1 = gp.gp_Pnt(0,0,curvature)
p2 = gp.gp_Pnt(curvature,0,0)

edge =BRepBuilderAPI.BRepBuilderAPI_MakeEdge(h_circ,p1,p2)

view(edge.Shape())
