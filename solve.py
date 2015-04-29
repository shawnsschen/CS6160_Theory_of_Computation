import dlx
import graphic
import puzzle
import parser

import matplotlib.pylab as plt
import os


def savepic(mat, maxscale, picname):
    fig = plt.matshow(mat, vmin=0, vmax=maxscale)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(picname, bbox_inches='tight', pad_inches = 0, dpi=100)
    plt.close()

def fliprot(sol):
    # horizontal flip
    horisol = [row[::-1] for row in sol]
    # vertical flip
    # rotate 90 degrees clockwise
    vertsol = [list(r) for r in zip(*sol[::-1])]
    # horizontal flip
    vertsol = [row[::-1] for row in vertsol]
    # rotate 90 degrees counter-clockwise
    vertsol = [list(r) for r in zip(*vertsol)[::-1]]
    return [sol, horisol, vertsol]

def solve(inputpath, FLIP, ROTATE):
    outputpath = 'results/' + inputpath.split('/')[-1].split('.')[0]
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    origPuzzle = parser.Parser(inputpath)
    bset = origPuzzle.search()
    board = origPuzzle.board
    bdrows = max([row[0] for row in board]) + 1
    bdcols = max([col[1] for col in board]) + 1
    tiles = [puzzle.Tile(b, FLIP, ROTATE) for b in bset]
    rows = 0
    cols = 0
    for tile in tiles:
        # find out all the possible tile placements
        tile.place(board)
        rows += len(tile.availCoords)
        print '\n'
        print '\n'
    cols = len(tiles) + len(board)
    coverMatrix = [[0] * cols for i in range(rows)]
    for n, tile in zip(range(len(tiles)), tiles):
        rowbase = 0
        for i in range(n):
            rowbase += len(tiles[i].availCoords)
        tilerange = range(len(tile.availCoords))
        for offset, coords in zip(tilerange, tile.availCoords):
            rowidx = rowbase + offset
            coverMatrix[rowidx][n] = 1
            for pair in coords:
                colidx = board.index(pair) + len(tiles)
                coverMatrix[rowidx][colidx] = 1
    # create a name row
    namerow = ['B'+`n` for n in range(len(tiles))]
    namerow += ['N'+`pair[0]`+'_'+`pair[1]` for pair in board]
    coverMatrix = [namerow] + coverMatrix

    indepSol = []
    mat = dlx.ExactCover(coverMatrix)
    solutions = mat.solve()
    if not next(solutions, False):
        print '---- No available solution ----'
    solcnt = 0
    for solution in solutions:
        graph = graphic.Graph(bdrows, bdcols, solution)
        newsol = graph.gen()
        newsolFR = fliprot(newsol)
        isIndep = True
        for nsol in newsolFR:
            for _ in range(4):
                if nsol in indepSol:
                    isIndep = False
                    break
                # rotate solution matrix 90 degrees clockwise
                nsol = [list(r) for r in zip(*nsol[::-1])]
        if isIndep:
            indepSol.append(newsol)
            solcnt += 1
            maxscale = max([max(m) for m in newsol])
            print 'Solution:', newsol
            print '\n'
            picname = outputpath + '/' + str(solcnt) + '.png'
            savepic(newsol, maxscale, picname)
    print 'found', solcnt, 'independent solutions'
    print mat.num_searches, 'searches'
