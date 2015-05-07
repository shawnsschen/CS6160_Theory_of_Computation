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

    def __init__(self, coordinates, pattern, FLIP=False, ROTATE=False):
        """
        Initialize the coordinates of current tile and auxiliary variables.
        """
        # contain the original tile
        self.origCoords = coordinates
        self.origPattern = pattern
        # contain the original tile and flipped and rotated variation.
        self.fliprotCoords = []
        self.fliprotCoords.append(self.origCoords)
        # contain the rotated and flipped patterns.
        self.fliprotPatterns = []
        self.fliprotPatterns.append(self.origPattern)
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
        patternMatrix = [[' '] * cols for i in range(rows)]
        for row in self.origCoords:
            metaMatrix[row[0]][row[1]] = 1
            print 'origPattern:', (row[0], row[1])
            patternMatrix[row[0]][row[1]] = self.origPattern[(row[0], row[1])]
        print 'orignial meta matrix', metaMatrix
        print 'orignial pattern matrix', patternMatrix

        if self.FLIP:
            metaflipset = []
            patternflipset = []
            print 'FLIP enabled'
            metaflip = deepcopy(metaMatrix)
            patternflipMat = deepcopy(patternMatrix)
            metaflipset.append(metaflip)
            patternflipset.append(patternflipMat)
            # horizontal flip
            newmeta = [row[::-1] for row in metaflip]
            newpattMat = [row[::-1] for row in patternflipMat]
            metaflipset.append(newmeta)
            patternflipset.append(newpattMat)
            print 'horizontal flipped meta matrix', newmeta
            print 'horizontal flipped pattern matrix', newpattMat
            rows = len(metaflip)
            cols = len(metaflip[0])
            newcoord = []
            newpattern = {}
            for r in range(rows):
                for c in range(cols):
                    if newmeta[r][c]:
                        newcoord.append([r, c])
                    if newpattMat[r][c] != ' ':
                        newpattern[(r, c)] = newpattMat[r][c]
            print 'horizontal flipped coords', newcoord
            print 'horizontal flipped patterns', newpattern
            # detect equivalence with existing coordinates
            if (sorted(newcoord) not in sorted(self.fliprotCoords) and
                newpattern not in self.fliprotPatterns):
                print 'new coordinates not in fliprotCoords, append'
                print 'new pattern not in fliprotPatterns, append'
                self.fliprotCoords.append(newcoord)
                self.fliprotPatterns.append(newpattern)
            else:
                print 'new coordinates already in fliprotCoords, omit'
                print 'new pattern already in fliprotPatterns, omit'
            # vertical flip
            # rotate 90 degrees clockwise
            newmeta = [list(r) for r in zip(*metaflip[::-1])]
            newpattMat = [list(r) for r in zip(*patternflipMat[::-1])]
            # horizontal flip
            newmeta = [row[::-1] for row in newmeta]
            newpattMat = [row[::-1] for row in newpattMat]
            # rotate 90 degrees counter-clockwise
            newmeta = [list(r) for r in zip(*newmeta)[::-1]]
            newpattMat = [list(r) for r in zip(*newpattMat)[::-1]]
            metaflipset.append(newmeta)
            patternflipset.append(newpattMat)
            print 'vertical flipped meta matrix', newmeta
            print 'vertical flipped pattern matrix', newpattMat
            rows = len(metaflip)
            cols = len(metaflip[0])
            newcoord = []
            newpattern = {}
            for r in range(rows):
                for c in range(cols):
                    if newmeta[r][c]:
                        newcoord.append([r, c])
                    if newpattMat[r][c] != ' ':
                        newpattern[(r, c)] = newpattMat[r][c]
            print 'vertical flipped coords', newcoord
            print 'vertical flipped patterns', newpattern
            # detect equivalence with existing coordinates
            if (sorted(newcoord) not in sorted(self.fliprotCoords) and
                newpattern not in self.fliprotPatterns):
                print 'new coordinates not in fliprotCoords, append'
                print 'new pattern not in fliprotPatterns, append'
                self.fliprotCoords.append(newcoord)
                self.fliprotPatterns.append(newpattern)
            else:
                print 'new coordinates already in fliprotCoords, omit'
                print 'new pattern already in fliprotPatterns, omit'

        if self.ROTATE:
            print 'ROTATE enabled'
            for metarot, pattrot in zip(metaflipset, patternflipset):
                for _ in range(3):
                    # rotate 90 degrees clockwise
                    metarot = [list(r) for r in zip(*metarot[::-1])]
                    pattrot = [list(r) for r in zip(*pattrot[::-1])]
                    print 'rotated 90 meta matrix', metarot
                    print 'rotated 90 pattern matrix', pattrot
                    rows = len(metarot)
                    cols = len(metarot[0])
                    # construct new rotated coordinates
                    newcoord = []
                    newpattern = {}
                    for r in range(rows):
                        for c in range(cols):
                            if metarot[r][c]:
                                newcoord.append([r, c])
                            if pattrot[r][c] != ' ':
                                newpattern[(r, c)] = pattrot[r][c]
                    print 'rotated coords', newcoord
                    print 'rotated pattern', newpattern
                    # detect equivalence with existing coordinates
                    if (sorted(newcoord) not in sorted(self.fliprotCoords) and
                        newpattern not in self.fliprotPatterns):
                        print 'new coordinates not in fliprotCoords, append'
                        print 'new pattern not in fliprotPatterns, append'
                        self.fliprotCoords.append(newcoord)
                        self.fliprotPatterns.append(newpattern)
                    else:
                        print 'new coordinates already in fliprotCoords, omit'
                        print 'new pattern already in fliprotPatterns, omit'

    def fit(self, tilecoor, bdcoor):
        """
        Check if the tile fits into the board.
        """
        for idx in range( len(tilecoor) ):
            if tilecoor[idx] not in bdcoor:
                return False
        return True

    def place(self, bdcoor):
        """
        Enumerate all the available placements.
        """
        # calculate rows and columns of the board
        rows = max([row[0] for row in bdcoor]) + 1
        cols = max([col[1] for col in bdcoor]) + 1
        # achieve all the flip and rotate combinations
        self.fliprotate()
        # iterate over all combinations and achieve all placements
        for tilecoor in self.fliprotCoords:
            print 'tile coords: ', tilecoor
            for vertical in range(rows):
                for horizon in range(cols):
                    newcoord = deepcopy(tilecoor)
                    tmpcoord = []
                    for r in newcoord:
                        r[0] += vertical
                        r[1] += horizon
                        tmpcoord.append(r)
                    # append if current placement fits the board
                    if self.fit(tmpcoord, bdcoor):
                        self.availCoords.append(tmpcoord)
                        print 'Avail placement', tmpcoord
