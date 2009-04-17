from enthought.traits.api import HasTraits, Instance, Event, List, Str, Button

from enthought.traits.ui.api import CustomEditor, View, Item, TreeEditor, TreeNode,\
            VSplit, HSplit

from OCC.Display.wxDisplay import wxViewer3d

from OCC import AIS

from occ_model import Input, ProcessObject

import wx

import os
os.environ['CSF_GraphicShr'] = r"/usr/local/lib/libTKOpenGL.so"

def MakeCanvas(parent, editor):
    canvas = wxViewer3d(parent)
    shapes = editor.object.shape_list.shapes
    
    def display_gen():
        canvas.Show()
        print "is shown", canvas.IsShown()
        wx.SafeYield()
        canvas.InitDriver()
        viewer = canvas._3dDisplay
        context = viewer.Context
        for shape in shapes:
            ais_shape = shape.ais_shape
            context.Display(ais_shape.GetHandle())
        yield
        while True:
            context.Redisplay(AIS.AIS_KOI_Shape)
            yield

    gen = display_gen()

    def on_render(obj, name, vnew):
        print "render"
        gen.next()

    for shape in shapes:
        shape.on_trait_change(on_render, "render")
    return canvas


class DisplayShape(HasTraits):
    """A displayable shape"""
    name = Str("an AIS shape")
    input = Input

    _input = List

    ais_shape = Instance(AIS.AIS_Shape)

    render = Event

    def _input_changed(self, name, vold, vnew):
        if vold is not None:
            vold.on_trait_change(self.on_modified, "modified", remove=True)
        vnew.on_trait_change(self.on_modified, "modified")
        self._input_list = [vnew]

    def on_modified(self):
        if vnew is True:
            shape = self.input.shape
            self.ais_shape.Set(shape)
            self.render = True


class ShapeList(HasTraits):
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
    
    render_btn = Button("render")

    traits_view=View(HSplit(
                    Item('shape_list', editor=occ_tree, show_label=False),
                    Item('shape_list', editor=CustomEditor(MakeCanvas),
                            show_label=False)
                        ),
                    Item("render_btn", show_label=False),
                    resizable=True,
                    width=1000,
                    height=800
                    )
                    
    def _shapes_changed(self, vnew):
        self.shape_list = ShapeList(shapes=vnew)
        
    def _render_btn_changed(self):
        self.shape_list.shapes[0].render = True
                    


