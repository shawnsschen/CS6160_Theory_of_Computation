import dlx
import puzzle
import parser

if __name__ == '__main__':
    origPuzzle = parser.Parser('puzzle_inputs/IQcreator.txt')
    """
    bset = []
    b0 = [[0,0],[1,0],[1,1]]
    bset.append(b0)
    b1 = [[0,0],[1,0]]
    bset.append(b1)
    b2 = [[0,0],[0,1],[0,2],[1,1]]
    bset.append(b2)
    board = [[0,0],[0,1],[0,2],
             [1,0],[1,1],[1,2],
             [2,0],[2,1],[2,2]]
    """
    bset = origPuzzle.search()
    board = origPuzzle.board
    bdcols = max([col[1] for col in board]) + 1
    #tiles = [puzzle.Tile(b, True, True) for b in bset]
    tiles = [puzzle.Tile(b) for b in bset]
    rows = 0
    cols = 0
    for tile in tiles:
        # find out all the possible tile placements
        tile.place(board)
        rows += len(tile.availCoords)
        print '\n'
        print '\n'
    cols = len(tiles) + len(board)
    print 'Cols', cols
    print 'Rows', rows
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
                colidx = pair[0] * bdcols + pair[1] + len(tiles)
                coverMatrix[rowidx][colidx] = 1
    # create a name row
    namerow = ['B'+`n` for n in range(len(tiles))]
    namerow += ['N'+`pair[0]`+`pair[1]` for pair in board]
    coverMatrix = [namerow] + coverMatrix

    mat = dlx.ExactCover(coverMatrix)
    for solution in mat.solve():
        print 'Solutions:\n', sorted(solution), '\n'
    print mat.num_searches, 'searches'
