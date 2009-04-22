from OCC import BRepPrimAPI, BRepFilletAPI, TNaming,\
    TDocStd, AppStd, TCollection, TDF, BRepAlgoAPI, gp, TopTools

from OCC.Utils.Topology import Topo

import os
os.environ['CSF_GraphicShr'] = r"/usr/local/lib/libTKOpenGl.so"
from OCC.Display.wxSamplesGui import display, start_display

def print_children(label):
    tool = TDF.TDF_Tool()
    itr = TDF.TDF_ChildIterator(label, True)
    while itr.More():
        val = itr.Value()
        output = TCollection.TCollection_AsciiString()
        tool.Entry(val, output)
        entry = output.ToCString()
        print "entry", entry
        itr.Next()
    print "end iteration"

app = AppStd.AppStd_Application()

h_doc = TDocStd.Handle_TDocStd_Document()
schema = TCollection.TCollection_ExtendedString("MyFormat")
app.NewDocument(schema, h_doc)

doc = h_doc.GetObject()

root = doc.Main()

ts = TDF.TDF_TagSource()


box = BRepPrimAPI.BRepPrimAPI_MakeBox(10.0,10.0,10.0).Shape()

box_label = ts.NewChild(root)
ns_builder = TNaming.TNaming_Builder(box_label)
ns_builder.Generated(box)

topo = Topo(box)

##
##Name all the subshape we *might* want to refer to later
##
#for edge in topo.edges():
#    sub_label = ts.NewChild(box_label)
#    ns_builder = TNaming.TNaming_Builder(sub_label)
#    ns_builder.Generated(edge)

#
#Find and Name an edge
#
an_edge = topo.edges().next()

sub_label = ts.NewChild(box_label)
ns_builder = TNaming.TNaming_Builder(sub_label)
ns_builder.Generated(an_edge)

s_label = ts.NewChild(root)
selector = TNaming.TNaming_Selector(s_label)
ret = selector.Select(an_edge, box)
print "selected", ret

#
#now modify the box
#

cut_tool = BRepPrimAPI.BRepPrimAPI_MakeBox(gp.gp_Pnt(6,6,6),
                                           5.,5.,5.).Shape()
                                           
#tool_label = ts.NewChild(root)
#ns_builder = TNaming.TNaming_Builder(tool_label)
#ns_builder.Generated(cut_tool)
#
#topo = Topo(cut_tool)
#for edge in topo.edges():
#    sub_label = ts.NewChild(tool_label)
#    ns_builder = TNaming.TNaming_Builder(sub_label)
#    ns_builder.Generated(edge)


                                           
bop = BRepAlgoAPI.BRepAlgoAPI_Cut(box, cut_tool)
cut_shape = bop.Shape()

cut_label = ts.NewChild(root)
ns_builder = TNaming.TNaming_Builder(cut_label)
ns_builder.Modify(box, cut_shape)

#if bop.HasModified():
#    mod_label = ts.NewChild(cut_label)
#    ns_builder = TNaming.TNaming_Builder(mod_label)
#    for edge in Topo(cut_shape).edges():
#        modified = bop.Modified(edge)
#        itr = TopTools.TopTools_ListIteratorOfListOfShape(modified)
#        while itr.More():
#            this = itr.Value()
#            ns_builder.Modify(edge, modified)
#            print "modify", edge, modified
#            itr.Next()
#            
#if bop.HasGenerated():
#    mod_label = ts.NewChild(cut_label)
#    ns_builder = TNaming.TNaming_Builder(mod_label)
#    for edge in Topo(cut_shape).edges():
#        modified = bop.Generated(edge)
#        itr = TopTools.TopTools_ListIteratorOfListOfShape(modified)
#        while itr.More():
#            this = itr.Value()
#            ns_builder.Modify(edge, modified)
#            print "generated", edge, modified
#            itr.Next()


#
#Chamfer selected edge
#

aMap = TDF.TDF_LabelMap()
ok = selector.Solve(aMap)
print "solve OK", ok

#display.DisplayShape(bop)
#start_display()
