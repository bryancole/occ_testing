"""
A simple example of a editable feature tree. We only have two source objects
(box and sphere) and a boolean-op filter.
"""

from occ_model import BlockSource, SphereSource, BooleanOpFilter
from occ_display import OCCModel, DisplayShape

block = BlockSource()

sphere = SphereSource()

bop = BooleanOpFilter(input=block, tool=sphere)

shape = DisplayShape(input=bop)

model = OCCModel(shapes=[shape])

model.configure_traits()

