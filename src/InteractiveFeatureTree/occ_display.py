from enthought.traits.api import HasTraits, Instance, Event, List, Str, Button

from enthought.traits.ui.api import CustomEditor, View, Item, TreeEditor, TreeNode,\
            VSplit, HSplit

from OCC.Display.wxDisplay import wxViewer3d

from OCC import AIS

from occ_model import Input, ProcessObject

#Jelle please don't shout at me!
import os
os.environ['CSF_GraphicShr'] = r"/usr/local/lib/libTKOpenGl.so"


class MyCanvas(wxViewer3d):
    def __init__(self, *args, **kwds):
        super(MyCanvas, self).__init__(*args, **kwds)
        self.SetSizeWH(800,-1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self._pending = []
        self.context = None
        
    def OnPaint(self, event):
        event.Skip()
        if self.context is None:
            self.FirstDisplay()
        
    def Display(self, shape):
        context = self.context
        if context is None:
            self._pending.append(shape)
        else:
            ais_shape = shape.ais_shape
            context.Display(ais_shape.GetHandle())
            
    def Render(self):
        context = self.context
        if context is not None:
            context.Redisplay(AIS.AIS_KOI_Shape)
            
    def FirstDisplay(self):
        self.InitDriver()
        viewer = self._display
        self.context = viewer.Context
        for shape in self._pending:
            self.Display(shape)
        self._pending = []
        self._display.FitAll()

def MakeCanvas(parent, editor):
    """
    A factory function to produce the wxViewer3d instance. This is
    called by the CustomEditor object.
    
    I still havn't found a nice way to do the InitDriver() stuff.
    """
    canvas = MyCanvas(parent)
    shapes = editor.object.shape_list.shapes

    def on_render(obj, name, vnew):
        canvas.Render()

    for shape in shapes:
        canvas.Display(shape)
        shape.on_trait_change(on_render, "render")
    
    return canvas


class DisplayShape(HasTraits):
    """
    A display-able shape. This class wraps AIS.AIS_Shape.
    
    Instances of this class are the root shape objects in the model
    and are the things we actually visualise.
    
    We could add visualisation traits to this object
    """
    name = Str("an AIS shape")
    input = Input

    _input = List

    ais_shape = Instance(AIS.AIS_Shape)

    render = Event

    def _input_changed(self, name, vold, vnew):
        if vold is not None:
            vold.on_trait_change(self.on_modified, "modified", remove=True)
        vnew.on_trait_change(self.on_modified, "modified")
        self._input = [vnew]

    def on_modified(self, vnew):
        if vnew is True:
            shape = self.input.shape
            self.ais_shape.Set(shape)
            self.render = True
            
    def _ais_shape_default(self):
        return AIS.AIS_Shape(self.input.shape)


class ShapeList(HasTraits):
    """
    Just a container for DisplayShapes. This exists mostly 
    because the TreeEditor expects child nodes on a single
    sub-object. A simple list doesn't work.
    """
    shapes = List(DisplayShape)
    

occ_tree = TreeEditor(nodes=[
            TreeNode(node_for=[ShapeList],
                    auto_open=True,
                    children='shapes',
                    label="=Shapes",
                    view=View()),
            TreeNode(node_for=[DisplayShape],
                     auto_open=True,
                     children='_input',
                     label='name',
                     view=View() ),
            TreeNode(node_for=[ProcessObject],
                    auto_open=True,
                    children='_inputs',
                    label='name')],
                orientation="vertical"
                )                    


class OCCModel(HasTraits):
    shapes = List
    
    shape_list = Instance(ShapeList)

    traits_view=View(HSplit(
                    Item('shape_list', editor=occ_tree, show_label=False,
                         width=-300),
                    Item('shape_list', editor=CustomEditor(MakeCanvas),
                            show_label=False, resizable=True),
                        id="occ.traits.test_feature_model_layout",
                        dock="fixed"
                        ),
                    resizable=True,
                    width=1000,
                    height=800,
                    id="occ.traits.test_feature_model"
                    )
                    
    def _shapes_changed(self, vnew):
        self.shape_list = ShapeList(shapes=vnew)
        
                    


