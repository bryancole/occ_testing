from occ_model import BlockSource, SphereSource, BooleanOpFilter

from occ_display import OCCModel, DisplayShape

block = BlockSource()

sphere = SphereSource()

bop = BooleanOpFilter(input=block, tool=sphere)

shape = DisplayShape(input=bop)

model = OCCModel(shapes=[shape])

print shape._input

model.configure_traits()

