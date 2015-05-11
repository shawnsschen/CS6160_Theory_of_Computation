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
# Interactive GUI to get user-input puzzle file and FLIP/ROTATE flags.


import solve
import easygui
import os
import time

if __name__ == '__main__':
    choice = easygui.ccbox(msg='Start solving puzzle?\nChoose a puzzle first.', title='Puzzle Solver v1.0', choices=('Continue', 'Cancel'), image=None)
    if choice:
        inputpath = easygui.fileopenbox(title='Choose a puzzle', default=None, filetypes=['*.txt'])
    puzzlename = inputpath.split('/')[-1].split('.')[0]
    outputpath = os.getcwd() + '/results/' + puzzlename

    msg = "Enable flipping and rotation?"
    title = 'Puzzle Solver v1.0'
    fieldName = ["Flipping", "Rotation"]
    fieldValue = []
    fieldValue = easygui.multenterbox(msg, title, fieldName)
    FLIP = fieldValue[0]
    ROTATE = fieldValue[1]

    start = time.time()
    solve.solve(inputpath, FLIP, ROTATE)
    end = time.time()

    printstr = 'Total time: ' + str(end - start) + ' seconds'
    msg = "Solutions generated. Please choose one."
    fieldName = ["Solution number"]
    fieldValue = []
    fieldValue = easygui.multenterbox(msg, title, fieldName)
    imgpath = outputpath + '/' + str(fieldValue[0]) + '.png'
    if os.path.exists(outputpath) and os.listdir(outputpath):
        easygui.msgbox(printstr, title, image=imgpath)
    else:
        easygui.msgbox("nothing found")
