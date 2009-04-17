from enthought.traits.api import (HasTraits, Property, Bool, Tuple, 
                        on_trait_change, cached_property, Instance,
                        Float
                                  )


from OCC import TDF, TopoDS

    
Input = Instance(klass="ProcessObject", process_input=True)


class ProcessObject(HasTraits):
    modified = Bool
    
    label = Instance(TDF.TDF_Label)
    
    shape = Property(Instance(TopoDS.TopoDS_Shape), depends_on="modified")
      
    @on_trait_change("+process_input")
    def on_input_change(self, obj, name, vold, vnew):
        print "ch", vold, vnew
        if vold is not None:
            vold.on_trait_change(self.on_modify, 'modified', remove=True)
        
        vnew.on_trait_change(self.on_modify, 'modified')
        
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
    dims = Tuple(10.0,20.0,30.0)
    
    def _dims_changed(self):
        self.modified = True
        
class SphereSource(ProcessObject):
    radius = Float(5.0)
        
class CutFilter(ProcessObject):
    input = Input
    tool = Input
        
if __name__=="__main__":
    
    c1 = CutFilter()
    c2 = CutFilter()
    c3 = CutFilter(input=c1, tool=c2)
    
    print c3.shape
    