from raytrace.step_export import make_ellipsoid, make_ellipsoid_mirror
from viewer import view

def ellipsoid():
    #ellipse = make_ellipsoid((0,0,0),(5,6,7), 14)
    mirror = make_ellipsoid_mirror((0.0, -60.1066, 39.9808),
                                   (0.0, 0.0, 74.9808),
                                   50,
                                   (-45.0, 0.0),
                                   (-22.5, 22.5),
                                   (22.139800000000001, 62.139800000000001),
                                   (0.0, 0.0, 0.0),
                                   (0.0, 0.0, 1.0))
                                   
    return mirror

view(ellipsoid())
