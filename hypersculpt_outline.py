import cadquery as cq
cq.freecad_impl.console_logging.enable()
import math
import numpy as np
import logging
log = logging.getLogger(__name__)

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def my_rotate(axis, theta, vec):
    return tuple(np.dot(rotation_matrix(axis,theta),np.array(vec)))

# Points we will use to create spline and polyline paths to sweep over
pts = []
for theta in np.linspace(0,math.pi/2,50):
    r = 4*math.cos(theta)
    x = r*math.cos(theta)
    y = r*math.sin(theta)
    pts.append((x,y))
for theta in np.linspace(0,math.pi/2,50):
    r = 4*math.cos(theta)
    x = -r*math.cos(theta)
    y = r*math.sin(theta)
    pts.append((x,y))
    

# Sweep a circle with a diameter of 1.0 units along the spline path we just created
defaultSweep = cq.Workplane("XY").circle(0.5).sweep(cq.Workplane("XZ").spline(pts).close())

# Translate the resulting solids so that they do not overlap and display them left to right
slices=20
inc = math.pi/slices

axes = [(0,1,0),(1,0,0),(0,0,1)]

loc = (0,0,0)
vec = (0,1,0)
records = []
records.append({'x':loc[0],'y':loc[1],'z':loc[2]})
show_object(defaultSweep)
for i in range(2*slices):
    loc = tuple(np.array(loc)+np.array(vec))
    vec = my_rotate(axes[2],inc,vec)
    records.append({'x':loc[0],'y':loc[1],'z':loc[2]})

    defaultSweep = defaultSweep.rotate((0,0,0),(1,0,0),inc*180/math.pi).rotate((0,0,0),(0,1,0),inc*180/math.pi).rotate((0,0,0),(0,0,1),inc*180/math.pi)
    show_object(defaultSweep.translate(loc))

defaultSweep = cq.Workplane("YZ").circle(0.5).sweep(cq.Workplane("XY").spline(pts).close())

axes = [(0,1,0),(1,0,0),(0,0,1)]

loc = (0,0,0)
vec = (0,0,1)
records = []
records.append({'x':loc[0],'y':loc[1],'z':loc[2]})
show_object(defaultSweep)
for i in range(2*slices):
    loc = tuple(np.array(loc)+np.array(vec))
    vec = my_rotate(axes[0],inc,vec)
    records.append({'x':loc[0],'y':loc[1],'z':loc[2]})

    defaultSweep = defaultSweep.rotate((0,0,0),(1,0,0),inc*180/math.pi).rotate((0,0,0),(0,1,0),inc*180/math.pi).rotate((0,0,0),(0,0,1),inc*180/math.pi)
    show_object(defaultSweep.translate(loc))


defaultSweep = cq.Workplane("XZ").circle(0.5).sweep(cq.Workplane("YZ").spline(pts).close())

axes = [(0,1,0),(1,0,0),(0,0,1)]

loc = (0,0,0)
vec = (1,0,0)
records = []
records.append({'x':loc[0],'y':loc[1],'z':loc[2]})
show_object(defaultSweep)
for i in range(2*slices):
    loc = tuple(np.array(loc)+np.array(vec))
    vec = my_rotate(axes[1],inc,vec)
    records.append({'x':loc[0],'y':loc[1],'z':loc[2]})

    defaultSweep = defaultSweep.rotate((0,0,0),(1,0,0),inc*180/math.pi).rotate((0,0,0),(0,1,0),inc*180/math.pi).rotate((0,0,0),(0,0,1),inc*180/math.pi)
    show_object(defaultSweep.translate(loc))
