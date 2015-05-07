import dlx
import graphic
import itertools
import puzzle
import parser

from copy import deepcopy
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

def patternmatch(sol, tiles, board, bpattern):
    tmpsol = deepcopy(sol)
    bdrows = max([row[0] for row in board]) + 1
    bdcols = max([col[1] for col in board]) + 1
    solMatrix = [[' '] * bdcols for i in range(bdrows)]
    boardMatrix = deepcopy(solMatrix)
    for s in tmpsol:
        tileid = int(s[0].replace('B', ''))
        s.remove(s[0])
        tile = tiles[tileid]
        tilecoord = []
        for point in s:
            point = point.replace('N', '')
            coord = [int(i) for i in point.split('_')]
            tilecoord.append(coord)
        tilermin = min([row[0] for row in tilecoord])
        tilecmin = min([col[1] for col in tilecoord])
        rawtilecoor = deepcopy(tilecoord)
        for r in tilecoord:
            r[0] -= tilermin
            r[1] -= tilecmin
        if sorted(tilecoord) in tile.fliprotCoords:
            idx = tile.fliprotCoords.index(sorted(tilecoord))
            pattern = tile.fliprotPatterns[idx]
            for pair in rawtilecoor:
                val = pattern[(pair[0] - tilermin, pair[1] - tilecmin)]
                solMatrix[pair[0]][pair[1]] = val
    for r in range(bdrows):
        for c in range(bdcols):
            if (r, c) in bpattern:
                boardMatrix[r][c] = bpattern[(r, c)]
    if solMatrix == boardMatrix:
        return True
    else:
        return False

def solve(inputpath, FLIP, ROTATE):
    filename = inputpath.split('/')[-1].split('.')[0]
    outputpath = 'results/' + filename
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    origPuzzle = parser.Parser(inputpath)
    bset, bpatterns = origPuzzle.search()
    board = origPuzzle.board
    bdrows = max([row[0] for row in board]) + 1
    bdcols = max([col[1] for col in board]) + 1
    if filename == 'partial_cross':
        partcnt = 0
        tsets = []
        psets = []
        for comb in itertools.combinations(bset, 9):
            tsets.append(list(comb))
            ptmp = []
            for item in comb:
                idx = bset.index(item)
                ptmp.append(bpatterns[idx])
            psets.append(ptmp)
    else:
        tsets = [bset]
        psets = [bpatterns]

    for tset, pset in zip(tsets, psets):
        tiles = [puzzle.Tile(b, p, FLIP, ROTATE) for b, p in zip(tset, pset)]
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
        for tile in tiles:
            n = tiles.index(tile)
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
        namerow = ['B'+`name` for name in range(len(tiles))]
        namerow += ['N'+`pair[0]`+'_'+`pair[1]` for pair in board]
        coverMatrix = [namerow] + coverMatrix

        indepSol = []
        mat = dlx.ExactCover(coverMatrix)
        solutions = mat.solve()
        if not next(solutions, False):
            print '---- No available solution ----'
        solcnt = 0
        for solution in solutions:
            match = patternmatch(solution, tiles, board, origPuzzle.bdpattern)
            if not match:
                continue
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
        if filename == 'partial_cross':
            partcnt += solcnt
    if filename == 'partial_cross':
        print 'found', partcnt, 'independent solutions'
    else:
        print 'found', solcnt, 'independent solutions'
    #print mat.num_searches, 'searches'
