from OCC import XCAFApp, STEPCAFControl, TDocStd, TCollection,\
        XCAFDoc, BRepPrimAPI, Quantity, STEPControl,\
        TopLoc, gp, TDF, TPrsStd
        
from viewer import viewXDE

reader = STEPCAFControl.STEPCAFControl_Reader()
print "1"
reader.ReadFile('XDE_test.step')
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
print "4"
h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())
shape_tool = h_shape_tool.GetObject()
# get the top level shapes

l_LabelShapes = TDF.TDF_LabelSequence()
shape_tool.GetShapes(l_LabelShapes)

count = l_LabelShapes.Length()

root_label = l_LabelShapes.Value(1)

shape = shape_tool.GetShape(root_label)
viewXDE(doc, root_label, shape)

