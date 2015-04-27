import parser

if __name__ == '__main__':
    origPuzzle = parser.Parser('puzzle_inputs/pentominoes5x12.txt')
    bset = origPuzzle.search()
    board = origPuzzle.board
    for tile in bset:
        print 'Tile: ', tile
    print 'Board', board
