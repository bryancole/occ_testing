from viewer import view
from OCC import BRepPrimAPI, STEPControl

def get_shape():
    box = BRepPrimAPI.BRepPrimAPI_MakeBox(10,20,30)    
    shape = box.Shape()
    return shape

shape = get_shape()

view(shape)

writer = STEPControl.STEPControl_Writer()
writer.Transfer(shape, STEPControl.STEPControl_AsIs)
writer.Write("test.step")

