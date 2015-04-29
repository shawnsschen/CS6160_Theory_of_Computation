#!/usr/bin/env python
# Created by: Shawn Chen <schen@virginia.edu>
#
# LICENSE
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or(at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details at http://www.gnu.org/copyleft/gpl.html
#
# Brief
# Converts the output of solutions into a graphically equivalent matrix.

from copy import deepcopy
import numpy as np

class Graph():

    """
    Converts an input solution to a colored graph represented by a matrix.
    """

    def __init__(self, rows, cols, solution):
        """
        Takes an input solution and parse it and generates the puzzle matrix.
        """
        self.rows = rows
        self.cols = cols
        self.gMat = [[0] * cols for i in range(rows)]
        for blk in solution:
            newblk = deepcopy(blk)
            blkname = int(newblk[0].replace('B', '')) + 1
            newblk.remove(newblk[0])
            for point in newblk:
                point = point.replace('N', '')
                coord = [int(i) for i in point.split('_')]
                self.gMat[coord[0]][coord[1]] = blkname

    def gen(self):
        """
        Returns the puzzle matrix.
        """
        return self.gMat

    def gen3dmat(self):
        """
        Generates a normalized 3d colored graph in matrix representation.
        """
        self.rgb = [[ 0.        ,  0.        ,  0.        ],
                    [ 0.94117647,  0.63921569,  0.03921569],
                    [ 0.50980392,  0.35294118,  0.17254902],
                    [ 0.63529412,  0.        ,  0.14509804],
                    [ 0.        ,  0.31372549,  0.9372549 ],
                    [ 0.10588235,  0.63137255,  0.88627451],
                    [ 0.        ,  0.54117647,  0.        ],
                    [ 0.37647059,  0.6627451 ,  0.09019608],
                    [ 0.41568627,  0.        ,  1.        ],
                    [ 0.64313725,  0.76862745,  0.        ],
                    [ 0.84705882,  0.        ,  0.45098039],
                    [ 0.4627451 ,  0.37647059,  0.54117647],
                    [ 0.42745098,  0.52941176,  0.39215686],
                    [ 0.98039216,  0.40784314,  0.        ],
                    [ 0.95686275,  0.44705882,  0.81568627],
                    [ 0.89803922,  0.07843137,  0.        ],
                    [ 0.39215686,  0.4627451 ,  0.52941176],
                    [ 0.52941176,  0.4745098 ,  0.30588235],
                    [ 0.        ,  0.67058824,  0.6627451 ],
                    [ 0.66666667,  0.        ,  1.        ],
                    [ 0.89019608,  0.78431373,  0.        ]]
        a = np.empty((self.rows, self.cols, 3))
        for r, i in zip(self.gMat, range(len(self.gMat))):
            for c, j in zip(r, range(len(r))):
                a[i][j] = self.rgb[c]
        return a
