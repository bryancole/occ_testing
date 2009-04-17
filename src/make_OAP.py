from OCC import Geom, gp, GeomAPI, BRepBuilderAPI, BRepPrimAPI, BRepAlgoAPI,\
        STEPControl

from viewer import view

EFL = 50.8

ax = gp.gp_Ax2(gp.gp_Pnt(0.,0.,0.), #origin
               gp.gp_Dir(1.,0.,0.), #main direction is Z
               gp.gp_Dir(0.,0.,1.)) #X Direction is X
FL = EFL/2. #focal length

para = Geom.Geom_Parabola(ax, FL)

h_para = Geom.Handle_Geom_Parabola(para)


radius = 25.4

outside = EFL + radius
length = (outside**2)/(4.*FL)

ax2 = gp.gp_Ax2(gp.gp_Pnt(0,0,0), #origin
               gp.gp_Dir(0.,0.,1.), #main direction is X
               gp.gp_Dir(1.,0.,0.)) #X Direction is Z

pbl_shape = BRepPrimAPI.BRepPrimAPI_MakeRevolution(ax2, h_para,
                                                   1.0, outside)



ax3 = gp.gp_Ax2(gp.gp_Pnt(EFL,0,0), #origin
               gp.gp_Dir(0.,0.,1.), #main direction is X
               gp.gp_Dir(0.,1.,0.)) #X Direction is Y
cyl_solid = BRepPrimAPI.BRepPrimAPI_MakeCylinder(ax3, radius, length)


nurb = BRepBuilderAPI.BRepBuilderAPI_NurbsConvert(pbl_shape.Shape())

cut = BRepAlgoAPI.BRepAlgoAPI_Cut(cyl_solid.Shape(), 
                                  nurb.Shape())
    
#view(wire.Shape(), cyl_solid.Shape(), pbl_shape.Shape())
#view(cyl_solid.Shape(), pbl_shape.Shape())



view(cut.Shape())

exportList = [nurb.Shape()]

step_export = STEPControl.STEPControl_Writer()
for shape in exportList:
    step_export.Transfer(shape,STEPControl.STEPControl_AsIs)
#step_export.Write("/home/bryan/ParabolicMirror.step")
