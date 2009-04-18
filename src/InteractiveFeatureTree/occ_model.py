from enthought.traits.api import (HasTraits, Property, Bool, 
                        on_trait_change, cached_property, Instance,
                        Float as _Float, List, Str, Enum
                                  )

from enthought.traits.ui.api import View, Item

from utils import Tuple, EditorTraits

from OCC import TDF, TopoDS, BRepPrimAPI, BRepAlgoAPI, gp

    
Input = Instance(klass="ProcessObject", process_input=True)


class Float(EditorTraits, _Float):
    pass

class ProcessObject(HasTraits):
    name = Str
    
    modified = Bool
    
    label = Instance(TDF.TDF_Label)
    
    shape = Property(Instance(TopoDS.TopoDS_Shape), depends_on="modified")

    _inputs = List
      
    @on_trait_change("+process_input")
    def on_input_change(self, obj, name, vold, vnew):
        print "ch", vold, vnew
        if vold is not None:
            vold.on_trait_change(self.on_modify, 'modified', remove=True)
            if vold in self._input_set:
                del self._inputs[self._inputs.index(vold)]
        
        vnew.on_trait_change(self.on_modify, 'modified')
        self._inputs.append(vnew)
        
    def on_modify(self, vnew):
        if vnew:
            self.modified = True
        
    @cached_property
    def _get_shape(self):
        shape = self.execute()
        self.modified = False
        return shape
        
    def execute(self):
        """return a TopoDS_Shape object"""
        raise NotImplementedError
        

      
class BlockSource(ProcessObject):
    name = "Block"
    dims = Tuple(10.0,20.0,30.0)
    position = Tuple(0.,0.,0.)
    x_axis = Tuple(1.,0.,0.)
    z_axis = Tuple(0.,0.,1.)
    
    traits_view = View('name',
                       'dims')
    
    @on_trait_change("dims, position, x_axis, z_axis")
    def on_edit(self):
        self.modified = True

    def execute(self):
        ax = gp.gp_Ax2(gp.gp_Pnt(*self.position),
                        gp.gp_Dir(*self.z_axis),
                        gp.gp_Dir(*self.x_axis))
        m_box = BRepPrimAPI.BRepPrimAPI_MakeBox(ax, *self.dims)
        return m_box.Shape()
        
        
class SphereSource(ProcessObject):
    name="Sphere"
    radius = Float(5.0)
    position = Tuple(0.,0.,0.)
    
    traits_view = View('name',
                       'radius',
                       'position')
    
    @on_trait_change("radius, position")
    def on_edit(self):
        self.modified = True
        
    def execute(self):
        pt = gp.gp_Pnt(*self.position)
        R = self.radius
        sph = BRepPrimAPI.BRepPrimAPI_MakeSphere(pt, R)
        return sph.Shape()
        
class BooleanOpFilter(ProcessObject):
    name = "Boolean Operation"
    input = Input
    tool = Input
    
    operation = Enum("cut", "fuse", "common")
    
    map = {'cut': BRepAlgoAPI.BRepAlgoAPI_Cut,
           'fuse': BRepAlgoAPI.BRepAlgoAPI_Fuse,
           'common': BRepAlgoAPI.BRepAlgoAPI_Common}
    
    traits_view = View('operation')
    
    def _operation_changed(self, vnew):
        self.name = "Boolean Op: %s"%vnew
        self.modified = True
        
    def execute(self):
        builder = self.map[self.operation]
        s1 = self.input.shape
        s2 = self.tool.shape
        return builder(s1, s2).Shape()
        
if __name__=="__main__":
    
    c1 = CutFilter()
    c2 = CutFilter()
    c3 = CutFilter(input=c1, tool=c2)
    
    print c3.shape
    
