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
# Generates the tiling puzzle matrix, converting a general form puzzle into an
# exact cover problem. A placement detector traverses all the possible places
# on the board and an equivalence detector detects the equivalent blocks after
# flipping and rotation.

from copy import deepcopy

class Tile():

    """
    A tile class for each tile of various shapes.
    """

    def __init__(self, coordinates, FLIP=False, ROTATE=False):
        """
        Initialize the coordinates of current tile and auxiliary variables.
        """
        # contain the original tile
        self.origCoords = coordinates
        # contain the original tile and flipped and rotated variation.
        self.fliprotCoords = []
        self.fliprotCoords.append(self.origCoords)
        # contain all the possible positions of the tile
        self.availCoords = []
        self.horizon = 0
        self.vertical = 0
        self.FLIP = FLIP
        self.ROTATE = ROTATE

    def fliprotate(self):
        """
        Generate all the flipped and rotated variation of this tile.
        """
        # generate a meta matrix from the original tile
        rows = max([row[0] for row in self.origCoords]) + 1
        cols = max([col[1] for col in self.origCoords]) + 1
        metaMatrix = [[0] * cols for i in range(rows)]
        for row in self.origCoords:
            metaMatrix[row[0]][row[1]] = 1
        print 'orignial meta matrix', metaMatrix

        if self.FLIP:
            print 'flip enabled'
            metaflip = deepcopy(metaMatrix)
            # horizontal flip
            newmeta = [row[::-1] for row in metaflip]
            print 'horizontal flipped meta matrix', newmeta
            newcoord = []
            for r in range(rows):
                for c in range(cols):
                    if newmeta[r][c]:
                        newcoord.append([r, c])
            print 'horizontal flipped coords', newcoord
            # detect equivalence with existing coordinates
            if sorted(newcoord) not in sorted(self.fliprotCoords):
                print 'new coordinates not in fliprotCoords, append'
                self.fliprotCoords.append(newcoord)
            else:
                print 'new coordinates already in fliprotCoords, omit'
            # vertical flip
            # rotate 90 degrees clockwise
            newmeta = [list(r) for r in zip(*metaflip[::-1])]
            # horizontal flip
            newmeta = [row[::-1] for row in newmeta]
            # rotate 90 degrees counter-clockwise
            newmeta = [list(r) for r in zip(*newmeta)[::-1]]
            print 'vertical flipped meta matrix', newmeta
            newcoord = []
            for r in range(rows):
                for c in range(cols):
                    if newmeta[r][c]:
                        newcoord.append([r, c])
            print 'vertical flipped coords', newcoord
            # detect equivalence with existing coordinates
            if sorted(newcoord) not in sorted(self.fliprotCoords):
                print 'new coordinates not in fliprotCoords, append'
                self.fliprotCoords.append(newcoord)
            else:
                print 'new coordinates already in fliprotCoords, omit'

        if self.ROTATE:
            print 'rotate enabled'
            metarot = deepcopy(metaMatrix)
            for _ in range(3):
                # rotate 90 degrees clockwise
                metarot = [list(r) for r in zip(*metarot[::-1])]
                print 'rotated 90 matrix', metarot
                # construct new rotated coordinates
                newcoord = []
                for r in range(rows):
                    for c in range(cols):
                        if metarot[r][c]:
                            newcoord.append([r, c])
                print 'rotated coords', newcoord
                # detect equivalence with existing coordinates
                if sorted(newcoord) not in sorted(self.fliprotCoords):
                    print 'new coordinates not in fliprotCoords, append'
                    self.fliprotCoords.append(newcoord)
                else:
                    print 'new coordinates already in fliprotCoords, omit'

    def fit(self, tilecoor, bdcoor):
        """
        Check if the tile fits into the board.
        """
        for idx in range( len(tilecoor) ):
            if self.tilecoor[idx] not in bdcoor:
                return False
        return True

    def place(self, bdcoor):
        """
        Enumerate all the available placements.
        """
