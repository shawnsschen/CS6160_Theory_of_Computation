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
