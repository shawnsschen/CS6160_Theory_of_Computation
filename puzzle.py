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


# flag enables flipping or not
flip   = False
# flag enables rotation or not
rotate = False

class Tile():

    """
    A tile class for each tile of various shapes.
    """

    # coordinates is a list of lists holding all coordinates of the given tile.
    def __init__(self, coordinates):
        """
        Initialize the coordinates of current tile and auxiliary variables.
        """
        self.coords = coordinates
        self.horizon = 0
        self.vertical = 0

    # bdcoor is the coordinates of the board.
    def fit(self, bdcoor):
        """
        Check if the tile fits into the board.
        """
        for idx in range( len(self.coords) ):
            if self.coords[idx] not in bdcoor:
                return False
        return True
