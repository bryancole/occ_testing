from enthought.traits.api import (HasTraits, Property, Bool, TraitType,
                                  TraitHandler, Tuple, on_trait_change,
                                  Proprty, cached_property
                                  )


from OCC import TDF, TopoDS

class ProcessObject(HasTraits):
    modified = Bool
    
    shape = Property(TopoDS.TopoDS_Shape, depends_on="modified")
      
    def on_input_change(self, vold, vnew):
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
        

Input = Trait(ProcessObject)

      
class BlockSource(ProcessObject):
    dims = Tuple(10.0,20.0,30.0)
    
    label = Instance(TDF.TDF_Label)
    
    def _dims_changed(self):
        self.modified = True