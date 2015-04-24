#!/usr/bin/env python
# Initially created by: David Goodger <goodger@python.org>
# Modified by: Shawn Chen <schen@virginia.edu>
#
# LICENSE
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or(at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details at http://www.gnu.org/copyleft/gpl.html
#
# Brief
# This is an implementation of Donald E. Knuth's 'Algorithm X' for exact cover
# problem using the 'Dancing Links' approach.

# optional acceleration with Psyco (up to 3x!):
try:
    import psyco
    psyco.full()
except ImportError:
    pass


class ExactCover(object):

    """
    Given a sparse matrix of 0s and 1s, find every set of rows containing
    exactly one 1 in each primary column (and at most one 1 in each secondary
    column).  See `load_matrix` for a description of the data structure.
    Uses the Dancing Links approach in Knuth's Algorithm X.
    """

    __slots__ = ('root', 'solution', 'num_solutions', 'num_searches')

    def __init__(self, matrix=None, secondary=0, state=None):
        """
        Parameters:
        * `matrix` & `secondary`: see `self.load_matrix`.
        * `state`: a `puzzler.SessionState` object which stores the runtime
          state of this puzzle (resuming a previously interrupted
          puzzle), or None (no state, starting from the beginning).
        """
        self.root = None
        """A `Root` object, set in `self.load_matrix()`."""

        self.solution = []
        self.num_solutions = 0
        self.num_searches = 0

        if state:
            self.solution = state.solution
            self.num_solutions = state.num_solutions
            self.num_searches = state.num_searches
        if matrix:
            self.load_matrix(matrix, secondary)

    def load_matrix(self, matrix, secondary=0):
        """
        Convert and store (into `self.root`) the input `matrix` as a four-way
        linked list to represent a sparse matrix.

        The input `matrix` is a two-dimensional list of tuples:
        * Each row is a tuple of equal length.

        * The first row contains the column names: first the puzzle piece
          names, then the solution space coordinates.  For example::
              ('A', 'B', 'C', '0,0', '1,0', '0,1', '1,1')

        * The subsequent rows consist of 1 & 0 (True & False) values.  Each
          row contains a 1/True value in the column identifying the piece, and
          1/True values in each column identifying the position.  There must
          be one row for each possible position of each puzzle piece.

        The `secondary` parameter is the number of secondary (rightmost)
        columns: columns which may, but need not, participate in the solution.

        The converted data structure consists of a sparse matrix
        representation starting at `self.root`, a `Root` node, the leftmost
        node in a circular doubly-linked list of `Column` header nodes.  The
        rightmost column node links (to the right) to the root, and the root
        links (to the left) to the rightmost column node.  Each column node is
        the topmost node in a circular doubly-linked list of `Node` nodes;
        the last node node links (downwards) to the column node, and the
        column node links (upwards) to the last node node.  Each node node
        links to the left and right to the nodes in the same row (again, the
        rightmost node links to the leftmost and vice-versa, in a circular
        doubly-linked list).

        The secondary columns are not part of the circular doubly-linked list
        of column nodes.  The last primary column links (to the right) to the
        root, and vice-versa (to the left).

        Except for the root node, each node contains five pointers: left,
        right, up, and down, and another pointer pointing to its column header.
        Each column header contains the column name and a count of the number
        of active nodes in that column.
        """

        self.root = root = Root()
        root.left = root.right = root
        columns = []
        prev = root

        for name in matrix[0]:
            column = Column(name=name, left=prev, right=root)
            prev.right = column
            root.left = column
            column.up = column.down = column
            columns.append(column)
            prev = column

        # usually not used
        for i in range(secondary):
            column = root.left
            root.left = column.left
            root.left.right = root
            column.left = column.right = column

        for row in matrix[1:]:
            first = None
            last = None
            for i, item in enumerate(row):
                # pruning, detect all 0 rows and skip
                if item:
                    column = columns[i]
                    node = Node(column=column, up=column.up, down=column)
                    if first is None:
                        first = node
                        last = node
                    column.up.down = node
                    column.up = node
                    node.left = last
                    node.right = first
                    last.right = node
                    first.left = node
                    column.size += 1
                    last = node

    def solve(self, level=0):
        """A generator that produces all solutions"""
        if self.root.right is self.root:
            yield list(self.solution)
            return
        self.num_searches += 1
        c = self.root.choose_column()
        c.cover()
        for r in c.down_siblings():
            # TODO: get a row index
            row = sorted(d.column.name for d in r.row_data())
            if len(self.solution) > level:
                if self.solution[level] != row:
                    # skip rows already fully explored
                    continue
            else:
                self.solution.append(row)
            for j in r.right_siblings():
                j.column.cover()
            for solution in self.solve(level+1):
                yield solution
            self.solution.pop()
            for j in r.left_siblings():
                j.column.uncover()
        c.uncover()


class Node(object):

    """
    A four-way linked data node in the exact cover sparse matrix.
    """

    __slots__ = ('up', 'down', 'left', 'right', 'column')

    def __init__(self, up=None, down=None, left=None, right=None, column=None):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.column = column

    # The following methods return lists for better performance:

    def row_data(self):
        """Return a list of all nodes on this row, including this node."""
        return [self] + self.right_siblings()

    def right_siblings(self):
        """Return a list of all rightward siblings of this node."""
        next = self.right
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.right
        return sibs

    def left_siblings(self):
        """Return a list of all leftward siblings of this node."""
        next = self.left
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.left
        return sibs

    def down_siblings(self):
        """Return a list of all downward siblings of this node."""
        next = self.down
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.down
        return sibs

    def up_siblings(self):
        """Return a list of all upward siblings of this node."""
        next = self.up
        sibs = []
        while next != self:
            sibs.append(next)
            next = next.up
        return sibs


class Column(Node):

    """
    A column header node in the exact cover sparse matrix.
    """

    __slots__ = ('name', 'size')

    def __init__(self, up=None, down=None, left=None, right=None, column=None,
                 name=None, size=0):
        Node.__init__(self, up, down, left, right, column)
        self.name = name
        self.size = size

    def cover(self):
        self.right.left = self.left
        self.left.right = self.right
        for i in self.down_siblings():
            for j in i.right_siblings():
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1

    def uncover(self):
        for i in self.up_siblings():
            for j in i.left_siblings():
                j.column.size += 1
                j.down.up = j
                j.up.down = j
        self.right.left = self
        self.left.right = self


class Root(Node):

    """
    The root node in the exact cover sparse matrix, doubly-linked to the
    column header nodes.
    """

    __slots__ = ('name',)

    name = 'root'
    up = None
    down = None
    column = None

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self):
        seen = set()
        header = []
        columns = {}
        width = 0
        for i, column in enumerate(self.right_siblings()):
            node = '%s/%s' % (column.name, column.size)
            header.append(node)
            width = max(width, len(node))
            columns[column] = i
        lines = [' '.join('%-*s' % (width, h) for h in header)]
        for i, column in enumerate(self.right_siblings()):
            for row in column.down_siblings():
                if row in seen:
                    continue
                line = []
                lastcol = -1
                for item in row.row_data():
                    seen.add(item)
                    colnum = columns[item.column]
                    line.extend([' '] * (colnum - lastcol - 1))
                    line.append(item.column.name)
                    lastcol = colnum
                lines.append(' '.join('%-*s' % (width, item)
                                      for item in line))
        return '\n'.join(lines)

    def choose_column(self):
        size, column = min((column.size, column)
                           for column in self.right_siblings())
        return column


# main function
if __name__ == '__main__':
    matrix = [
        'A  B  C  D  E  F'.split(),
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1]]
    mat = ExactCover(matrix)
    print 'Matrix =\n', mat.root, '\n'
    for solution in mat.solve():
        print 'Solutions:\n', sorted(solution), '\n'
    print mat.num_searches, 'searches'
