import dlx
import graphic
import puzzle
import parser

if __name__ == '__main__':
    origPuzzle = parser.Parser('puzzle_inputs/pentominoes8x8_middle_missing.txt')
    bset = origPuzzle.search()
    board = origPuzzle.board
    bdrows = max([row[0] for row in board]) + 1
    bdcols = max([col[1] for col in board]) + 1
    tiles = [puzzle.Tile(b, True, True) for b in bset]
    #tiles = [puzzle.Tile(b) for b in bset]
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
        isIndep = True
        for _ in range(4):
            if newsol in indepSol:
                isIndep = False
                break
            # rotate solution matrix 90 degrees clockwise
            newsol = [list(r) for r in zip(*newsol[::-1])]
        if isIndep:
            indepSol.append(newsol)
            solcnt += 1
            print 'Solution:', newsol
            print '\n'
    print 'found', solcnt, 'independent solutions'
    print mat.num_searches, 'searches'
