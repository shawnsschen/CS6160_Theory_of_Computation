import dlx

# main function
if __name__ == '__main__':
    matrix = [
        'A  B  C  D  E  F'.split(),
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1]]
    mat = dlx.ExactCover(matrix)
    print 'Matrix =\n', mat.root, '\n'
    for solution in mat.solve():
        print 'Solutions:\n', sorted(solution), '\n'
    print mat.num_searches, 'searches'
