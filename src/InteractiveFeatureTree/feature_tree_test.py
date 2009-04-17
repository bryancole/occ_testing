from occ_model import BlockSource

from occ_display import OCCModel, DisplayShape

block = BlockSource()

shape = DisplayShape(input=block)

model = OCCModel(shapes=[shape])

model.configure_traits()

