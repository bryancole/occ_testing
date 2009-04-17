from examples_gui import display, loop, canvas

from OCC import XCAFApp, TDocStd, TCollection,\
        XCAFDoc, BRepPrimAPI, Quantity, TopLoc, gp,\
        TPrsStd, XCAFPrs, STEPCAFControl, TDF
        
import wx
filename = wx.FileSelector()
        
reader = STEPCAFControl.STEPCAFControl_Reader()
print "1"
reader.ReadFile(str(filename))
print "2"
#
# Create the TDocStd document
#
h_doc = TDocStd.Handle_TDocStd_Document()
print h_doc.IsNull()
#
# Create the application: really *awfull* way to do that
#
#app = Handle_XCAFApp_Application().GetObject()
app = XCAFApp.GetApplication().GetObject()
app.NewDocument(TCollection.TCollection_ExtendedString("MDTV-CAF"),h_doc)
print "3"
#
# Transfer
#
print h_doc.IsNull()
if not reader.Transfer(h_doc):
    print "Error"
print "4 bis"

#
# Get root assembly
#
doc = h_doc.GetObject()
h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())

shape_tool = h_shape_tool.GetObject()

l_LabelShapes = TDF.TDF_LabelSequence()
shape_tool.GetShapes(l_LabelShapes)

count = l_LabelShapes.Length()
print "shape count", count
top_label = l_LabelShapes.Value(1)

context = display.Context

#
# Set up AIS Presentation stuff (I don't understand this, but it kinda works)
#
aisView = TPrsStd.TPrsStd_AISViewer().New(top_label, context.GetHandle())

aisPres = TPrsStd.TPrsStd_AISPresentation().Set(top_label, XCAFPrs.XCAFPrs_Driver().GetID())
aisPres.GetObject().Display(True)

#context.UpdateCurrentViewer()
#canvas.ZoomAll(None)
display.FitAll()

loop()
