from enthought.traits.api import (HasTraits, Property, Bool, 
                        on_trait_change, cached_property, Instance,
                        Float as _Float, List, Str, Enum
                                  )

from enthought.traits.ui.api import View, Item

from utils import Tuple, EditorTraits

from OCC import TDF, TopoDS, BRepPrimAPI, BRepAlgoAPI, gp, BRepFilletAPI

from OCC.Utils import Topology

    
Input = Instance(klass="ProcessObject", process_input=True)


class Float(EditorTraits, _Float):
    pass

class ProcessObject(HasTraits):
    name = Str
    
    modified = Bool(True)
    
    label = Instance(TDF.TDF_Label)
    
    _shape = Instance(TopoDS.TopoDS_Shape)
    
    shape = Property(Instance(TopoDS.TopoDS_Shape))

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
        
    def _get_shape(self):
        if self.modified:
            shape = self.execute()
            self._shape = shape
            self.modified = False
            return shape
        else:
            return self._shape
        
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
        
        
class ChamferFilter(ProcessObject):
    name = "Chamfer"
    input = Input
    
    distance1 = Float(1.0)
    
    distance2 = Float(1.0)
    
    edges = List([1])
    
    faces = List([0])
    
    traits_view = View(Item('distance1'),
                            Item('distance2'),
                            Item('edges'),
                            Item('faces'))
    
    @on_trait_change("distance1, distance2, edges, faces")
    def on_edit(self):
        self.modified = True
    
    def execute(self):
        print self.input.shape
        topo = Topology.Topo(self.input.shape)
        all_edges = list(topo.edges())
        all_faces = list(topo.faces())
        print all_edges
        edges = [all_edges[i] for i in self.edges]
        faces = [all_faces[i] for i in self.faces]
        print edges
        print "faces", faces
        #~ for e in edges:
            #~ print topo.number_of_faces_from_edge(e)
        #~ for e in edges:
            #~ for face in topo.faces_from_edge(e):
                #~ print face
        #~ faces = [list(topo.faces_from_edge(e)) for e in edges]
        #~ print faces
        chamf = BRepFilletAPI.BRepFilletAPI_MakeChamfer(self.input.shape)
        for e,f in zip(edges, faces):
            chamf.Add(self.distance1,
                            self.distance2,
                            e,
                            f)
        chamf.Build()
        print "done", chamf.IsDone()
        return chamf.Shape()
    
        
if __name__=="__main__":
    
    c1 = CutFilter()
    c2 = CutFilter()
    c3 = CutFilter(input=c1, tool=c2)
    
    print c3.shape
    
