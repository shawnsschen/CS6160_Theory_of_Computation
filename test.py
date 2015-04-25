import puzzle

if __name__ == '__main__':
    newtile = [[0,0],[1,0],[2,0],[3,0]]
    board = [[0,0],[0,1],[0,2],
             [1,0],[1,1],[1,2],
             [2,0],[2,1],[2,2]]
    tile = puzzle.Tile(newtile)
    print tile.fit(board)
