#!/usr/bin/python

# FEMM Helper by Jeff Martin

import numpy as np
import math
from optparse import OptionParser
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d


parser = OptionParser()

parser.add_option("-s", "--selfshielded",
                  action="store_true", dest="ss", default=False,
                  help="included self-shielding coil")

parser.add_option("-c", "--cylindrical",
                  action="store_true", dest="cyl", default=False,
                  help="cylindrical geometry")

parser.add_option("-r", "--read-file", action="store_true",
                  dest="yesread", default=False, help="read geometry from files")

parser.add_option("-i", "--inner", dest="innerfile",
                  default="Cylinder_inner_0.2mA.txt", help="read inner coils from FILE", metavar="FILE")

parser.add_option("-o", "--outer", dest="outerfile",
                  default="Cylinder_outer_0.2mA.txt", help="read outer coils from FILE", metavar="FILE")

parser.add_option("-f", "--file", dest="filename", default="femm_helper.fem",
                  help="write to FILE", metavar="FILE")

(options, args) = parser.parse_args()


with open(options.innerfile) as innerstream:
    d=np.loadtxt(innerstream,comments="%",unpack=True)

unique=np.unique(d[3])

print (unique)

for value in unique:
    iso=d[:,(d[3]==value)]
    points=np.transpose(iso[:3])
    sorted_points=np.transpose(iso[:3])
    nnindex=0
    for i in range(len(sorted_points)-1):
        point=points[nnindex]
        sorted_points[i]=point
        x,y,z=point
        points=np.delete(points,nnindex,0)
        xs,ys,zs=np.transpose(points)
        distance2=(x-xs)**2+(y-ys)**2+(z-zs)**2
        nnindex=np.where(distance2==distance2.min())[0][0]
    sorted_points[len(sorted_points)-1]=points
    f=open('sortedPoints.dat','ab')
    np.savetxt(f, sorted_points)
    f.close 

d=np.loadtxt('sortedPoints.dat')
p=np.transpose(d)

X=p[0]
Y=p[1]
Z=p[2]

fig=plt.figure
ax=plt.axes(projection='3d')

ax.scatter(X,Y,Z)
plt.suptitle('Extracted Traces')
ax.set_xlabel('x(m)')
ax.set_ylabel('y(m)')
ax.set_zlabel('z(m)')
plt.show()
fig.savegif('extracted_traces.jpg')





    
