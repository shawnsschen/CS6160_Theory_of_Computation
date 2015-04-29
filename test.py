import solve
import easygui
import os
import threading
import multiprocessing
import time

if __name__ == '__main__':
    FLIP = True
    ROTATE = True
    choice = easygui.ccbox(msg='Start solving puzzle?\nChoose a puzzle first.', title='Puzzle Solver v1.0', choices=('Continue', 'Cancel'), image=None)
    if choice:
        inputpath = easygui.fileopenbox(title='Choose a puzzle', default=None, filetypes=['*.txt'])
    puzzlename = inputpath.split('/')[-1].split('.')[0]
    outputpath = os.getcwd() + '/results/' + puzzlename

    start = time.time()
    solve.solve(inputpath, FLIP, ROTATE)
    end = time.time()
    print 'Total time: ', end - start
    """
    #proc = multiprocessing.Process(target=solve.solve, args=(inputpath, FLIP, ROTATE))
    proc = threading.Thread(target=solve.solve, args=(inputpath, FLIP, ROTATE))
    proc.start()
    time.sleep(3)
    if os.path.exists(outputpath) and os.listdir(outputpath):
        easygui.msgbox("pic generated")
    else:
        easygui.msgbox("nothing found")
    #proc.terminate()
    """
