import wx
from wxDisplay import GraphicsCanva3D
from math import pi
from OCC import BRepPrimAPI
from OCC.gp import gp_Pnt, gp_Ax2, gp_Vec, gp_Trsf, gp_Ax3, gp_Dir
from OCC import TopoDS, BRep, STEPControl, BRepBuilderAPI

app = wx.App()

frame = wx.Frame(None, -1, "OCC frame", size=(600,700))
canvas = GraphicsCanva3D(frame)
frame.Show()
wx.SafeYield()

canvas.Init3dViewer()
viewer = canvas._3dDisplay
print viewer

box = BRepPrimAPI.BRepPrimAPI_MakeBox(20,30,40)

ax = gp_Ax2()
ax.Translate(gp_Vec(50,50,50))

cyl_len = 40
radius = 10
angle = pi*1.5

cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(radius, cyl_len)

ax = gp_Ax3()
ax.SetLocation(gp_Pnt(50,60,70))
ax.SetDirection(gp_Dir(gp_Vec(1,1,1)))
trans = gp_Trsf()
trans.SetTransformation(ax)

t_cyl = BRepBuilderAPI.BRepBuilderAPI_Transform(cyl.Shape(), trans)

viewer.DisplayShape(box.Shape())
viewer.DisplayShape(t_cyl.Shape())

app.MainLoop()

##Building the resulting compund
#aRes = TopoDS.TopoDS_Compound()
#aBuilder = BRep.BRep_Builder()
#aBuilder.MakeCompound(aRes)
#aBuilder.Add(aRes, box.Shape())
#aBuilder.Add(aRes, cyl.Shape())

# Export to STEP
step_export = STEPControl.STEPControl_Writer()
step_export.Transfer(box.Shape(),STEPControl.STEPControl_AsIs)
step_export.Transfer(t_cyl.Shape(),STEPControl.STEPControl_AsIs)
step_export.Write('/home/bryan/test_STEP_gen.stp')


