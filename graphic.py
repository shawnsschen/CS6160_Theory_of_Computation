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

class Graph():

    """
    Converts an input solution to a colored graph represented by a matrix.
    """

    def __init__(self, rows, cols, solution):
        """
        Takes an input solution and parse it.
        """
        self.gMat = [[0] * cols for i in range(rows)]
        for blk in solution:
            newblk = deepcopy(blk)
            blkname = int(newblk[0].replace('B', ''))
            newblk.remove(newblk[0])
            for point in newblk:
                point = point.replace('N', '')
                coord = [int(i) for i in point.split('_')]
                self.gMat[coord[0]][coord[1]] = blkname

    def gen(self):
        """
        Generates a graph using the gMat matrix.
        """
        return self.gMat
