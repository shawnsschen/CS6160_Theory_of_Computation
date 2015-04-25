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

class Puzzle():

    """
    A puzzle class
    """

    def __init__(self):
        self.name = ''
