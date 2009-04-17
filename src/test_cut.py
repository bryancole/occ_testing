from viewer import view
from OCC import BRepPrimAPI, BRepBuilderAPI, gp, Geom, STEPControl,\
        BRepAlgoAPI

R = 20.

sphere = BRepPrimAPI.BRepPrimAPI_MakeSphere(R)


class GTransform(gp.gp_GTrsf):
    def ScaleX(self, val):
        v = self.Value(1,1)
        self.SetValue(1,1,val*v)
        
    def ScaleY(self, val):
        v = self.Value(2,2)
        self.SetValue(2,2,val*v)
        
    def ScaleZ(self, val):
        v = self.Value(3,3)
        self.SetValue(3,3,val*v)
        
    def Translate(self, dx, dy, dz):
        self.SetTranslationPart(gp.gp_XYZ(dx,dy,dz))

t = GTransform()
t.ScaleZ(2.0)

trans = BRepBuilderAPI.BRepBuilderAPI_GTransform(sphere.Shape(),
                                                 t)

box = BRepPrimAPI.BRepPrimAPI_MakeBox(100,100,100)

cut = BRepAlgoAPI.BRepAlgoAPI_Cut(box.Shape(), trans.Shape())

view(cut.Shape())

#step_export = STEPControl.STEPControl_Writer()
#step_export.Transfer(trans.Shape(), STEPControl.STEPControl_AsIs)
#step_export.Write("/home/bryan/test_ellipse.stp")

#el = gp.gp_Elips(gp.gp_Ax2(gp.gp_Pnt(0,0,0), gp.gp_Dir(1,0,0)), 10, 5)
#EL = Geom.Geom_Ellipse(el)
#handle = Geom.Handle_Geom_Ellipse(EL)
#revolve = BRepPrimAPI.BRepPrimAPI_MakeRevolution(handle, 180)
#nurbs = 
#view(revolve.Shape())