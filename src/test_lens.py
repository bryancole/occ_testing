from viewer import view

from OCC import Geom, GeomAPI, gp, BRepBuilderAPI, BRep, TopoDS

radius = 25.0
sph = Geom.Geom_SphericalSurface(gp.gp_Ax3(), radius)
h_sph = Geom.Handle_Geom_SphericalSurface(sph)

c_rad = 12.0 #cylinder radius
cyl = Geom.Geom_CylindricalSurface(gp.gp_Ax3(), c_rad)
h_cyl = Geom.Handle_Geom_CylindricalSurface(cyl)

intersect = GeomAPI.GeomAPI_IntSS(h_sph, h_cyl, 1e-7)

edges = (BRepBuilderAPI.BRepBuilderAPI_MakeEdge(intersect.Line(i))
         for i in xrange(1,intersect.NbLines()+1))

wires = [BRepBuilderAPI.BRepBuilderAPI_MakeWire(e.Edge())
         for e in edges]

g_sph = gp.gp_Sphere(gp.gp_Ax3(), radius)
faces = [BRepBuilderAPI.BRepBuilderAPI_MakeFace(w.Wire())
         for w in wires]
cyl_face = BRepBuilderAPI.BRepBuilderAPI_MakeFace(h_cyl)
#cyl_face.Add(wires[0].Wire())
#cyl_face.Add(wires[1].Wire())

#shell = TopoDS.TopoDS_Shell()
shell_builder = BRep.BRep_Builder()
#shell_builder.MakeShell(shell)
#shell_builder.Add(shell, cyl_face.Shape())
#for f in faces:
#    shell_builder.Add(shell, f.Shape())
    
#sewing = BRepBuilderAPI.BRepBuilderAPI_Sewing()
#sewing.Add(shell)
#sewing.Perform()
    
#shell = BRepBuilderAPI.BRepBuilderAPI_MakeShell(h_cyl)
    
view(cyl_face.Shape())