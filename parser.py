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
# Parses the input ASCII file containing tiles and board. After recognizing
# those tiles, convert them into coordinates and save in a list.

import string

class Parser():

    """
    A parser class to parse the input ASCII file and find all the tiles.
    """

    def __init__(self, filename):
        """
        Reads the given file and scan it into a matrix.
        """
        self.inputMat = []
        f = open(filename, 'r')
        self.matcols = len(max(f, key=len))
        f.seek(0)
        for line in f:
            newline = string.replace(line, '\n', ' ')
            linelist = list(newline) + [' '] * (self.matcols - len(newline))
            self.inputMat.append(linelist)
        self.matrows = len(self.inputMat)
        f.close()

    def lookaround(self, coord):
        """
        Look around current point, up down left and right. Return the
        coordinates in a list if found non-empty elements.
        """
        neighbors = []
        if coord[0] > 0:
            # look up
            if self.inputMat[coord[0] - 1][coord[1]] != ' ':
                neighbors.append([coord[0] - 1, coord[1]])
        if coord[1] < (self.matcols - 1):
            # look right
            if self.inputMat[coord[0]][coord[1] + 1] != ' ':
                neighbors.append([coord[0], coord[1] + 1])
        if coord[0] < (self.matrows - 1):
            # look down
            if self.inputMat[coord[0] + 1][coord[1]] != ' ':
                neighbors.append([coord[0] + 1, coord[1]])
        if coord[1] > 0:
            # look left
            if self.inputMat[coord[0]][coord[1] - 1] != ' ':
                neighbors.append([coord[0], coord[1] - 1])
        return neighbors

    def align(self, coords):
        """
        Reset the top-left most coordinates to 0.
        """
        minrow = min([row[0] for row in coords])
        mincol = min([row[1] for row in coords])
        for r in coords:
            r[0] -= minrow
            r[1] -= mincol
        return coords

    def search(self):
        """
        Search the input matrix and find all the tiles.
        """
        self.tileset = []
        for row, rowidx in zip(self.inputMat, range(len(self.inputMat))):
            for col, colidx in zip(row, range(len(row))):
                if self.inputMat[rowidx][colidx] == ' ':
                    continue
                discover = []
                unsearch = []
                current = [rowidx, colidx]
                firstpass = True
                while firstpass or unsearch:
                    firstpass = False
                    if [current[0], current[1]] not in discover:
                        discover.append([current[0], current[1]])
                    if [current[0], current[1]] in unsearch:
                        unsearch.remove([current[0], current[1]])
                    self.inputMat[current[0]][current[1]] = ' '
                    # search around
                    surround = self.lookaround([current[0], current[1]])
                    # if surround has no elements
                    if surround:
                        for i in surround:
                            if i not in discover:
                                discover.append(i)
                            if i not in unsearch:
                                unsearch.append(i)
                    if unsearch:
                        # fetch the first element in unsearch
                        current = [unsearch[0][0], unsearch[0][1]]
                    else:
                        discover = self.align(discover)
                        self.tileset.append(sorted(discover))
        # the largest tile is board
        self.board = max(self.tileset, key=len)
        self.tileset.remove(self.board)
        return self.tileset
