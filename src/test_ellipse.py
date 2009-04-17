from viewer import view
from OCC import BRepPrimAPI, BRepBuilderAPI, gp, Geom, STEPControl

R = 50.

sphere = BRepPrimAPI.BRepPrimAPI_MakeSphere(R)

def scale(sx, sy, sz):
    t = gp.gp_GTrsf()
    t.SetValue(1,1,sx)
    t.SetValue(2,2,sy)
    t.SetValue(3,3,sz)
    return t

trans = BRepBuilderAPI.BRepBuilderAPI_GTransform(sphere.Shape(),
                                                 scale(1,1,2))

step_export = STEPControl.STEPControl_Writer()
step_export.Transfer(trans.Shape(), STEPControl.STEPControl_AsIs)
step_export.Write("/home/bryan/test_ellipse.stp")

#el = gp.gp_Elips(gp.gp_Ax2(gp.gp_Pnt(0,0,0), gp.gp_Dir(1,0,0)), 10, 5)
#EL = Geom.Geom_Ellipse(el)
#handle = Geom.Handle_Geom_Ellipse(EL)
#revolve = BRepPrimAPI.BRepPrimAPI_MakeRevolution(handle, 180)
#nurbs = 
#view(revolve.Shape())