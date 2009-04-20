from occ_model import BlockSource, SphereSource, BooleanOpFilter, ChamferFilter

from occ_display import OCCModel, DisplayShape

block = BlockSource()

sphere = SphereSource()

chamfer = ChamferFilter(input=block)

bop = BooleanOpFilter(input=chamfer, tool=sphere)

shape = DisplayShape(input=bop)

model = OCCModel(shapes=[shape])

print chamfer.shape

model.configure_traits()

