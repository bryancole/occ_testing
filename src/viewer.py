import wx
import os

os.environ['CSF_GraphicShr'] = "/usr/local/lib/libTKOpenGl.so"

from wxDisplay import GraphicsCanva3D
from OCC import TPrsStd, XCAFPrs

app = wx.App()

def view(*shapeList):
    frame = wx.Frame(None, -1, "OCC frame", size=(600,700))
    canvas = GraphicsCanva3D(frame)
    frame.Show()
    wx.SafeYield()
    
    canvas.Init3dViewer()
    viewer = canvas._3dDisplay
    
    for shape in shapeList:
        viewer.DisplayShape(shape)
        
    app.MainLoop()
    
    
def viewXDE(doc, aLabel, shape):
    frame = wx.Frame(None, -1, "OCC frame", size=(600,700))
    canvas = GraphicsCanva3D(frame)
    frame.Show()
    wx.SafeYield()
    
    canvas.Init3dViewer()
    viewer = canvas._3dDisplay
    context = viewer.Context
    aisView = TPrsStd.TPrsStd_AISViewer().New(aLabel, viewer.Viewer.GetHandle())
    print aisView
#    aisView.SetInteractiveContext(context.GetHandle())
#    #viewer.DisplayShape(shape)
    aisPres = TPrsStd.TPrsStd_AISPresentation().Set(aLabel, XCAFPrs.XCAFPrs_Driver().GetID())
    aisPres.GetObject().Display(True)
    #context.SetDisplayMode(1)
    #aisView.GetObject().Update(doc.GetData().GetObject().Root())
    context.UpdateCurrentViewer()
    
    app.MainLoop()