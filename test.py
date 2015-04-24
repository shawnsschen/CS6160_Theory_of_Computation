import unittest
from dancinglinks import DancingLinks

class TestAlgorithmX(unittest.TestCase):

    def check(self, mat, expected):
        solver = DancingLinks(mat)
        solution = solver.solve()
        sets = [n.row for n in solution]
        sets.sort()
        self.assertEquals(expected, sets)

    def testSimpleIdentity(self):
        self.check([[1, 0], [0, 1]], [0, 1])

    def testUnfeasible(self):
        mat = [[0, 1, 1], [1, 1, 0]]
        self.check(mat, [])

    def testDemoCase(self):
        mat = [[0, 0, 1, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 1],
               [0, 1, 1, 0, 0, 1, 0],
               [1, 0, 0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 1],
               [0, 0, 0, 1, 1, 0, 1]]
        self.check(mat, [0, 3, 4])

    def testMultiSol(self):
        mat = [[1, 0, 1, 0, 0, 0],
               [1, 1, 0, 0, 0, 0],
               [0, 1, 0, 1, 0, 0],
               [0, 0, 1, 1, 0, 0],
               [0, 0, 0, 0, 1, 1]]
        self.check(mat, [0, 2, 4])

if __name__ == '__main__':
    unittest.main()
