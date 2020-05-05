# No imports!


#############
# Problem 1 #
#############

def tree_parts(tree):
    for index in range(len(tree)):
        if tree[index] == None:
            yield (tree, index)
        else:
            yield tree_parts(tree)

def binary_trees(n):
    """As a generator, return all possible binary trees of size `k`,
    in any order, with no duplicates."""
    if n == 0:
        return [None]
    if n == 1:
        return [(None, None)]
    agenda = [[[None, None], 1]]
    while agenda:
        item = agenda.pop()
        tree = item[0]
        decision = item[1]
        num = item[2]
        if num == n:
            yield tuple(tree)
        # for each None in tree, replace with (None, None)
        for part, index in tree_parts(tree):
            tree_copy = tree.copy()
            part[index] == (None, None)
            agenda.append([tree, num+1])
            tree = tree_copy

#############
# Problem 2 #
#############

def locs(size):
    result = set()
    for i in range(size):
        for j in range(size):
            result.add((i, j))
    return result

def moves(loc, size):
    x = loc[0]
    y = loc[1]
    result = set()
    for i in range(size):
        # diagonals
        if x-i >= 0 and y-i >= 0:
            result.add((x-i, y-i))
        if x+i < size and y+i < size:
            result.add((x+i, y+i))
        if x-i >= 0 and y+i < size:
            result.add((x-i, y+i))
        if x+i < size and y-i >= 0:
            result.add((x+i, y-i))
    return result

def n_bishops(n, bishop_locs, target):
    """
    Finds the placement of target amount of bishops such that
    no two bishops can attack each other.
    :param n: the length of a side of the board
    :param bishop_locs: the locations of the bishops already on the board
    :param target: the total number of bishops
    """
    board = locs(n)
    for loc in bishop_locs:
        bl = moves(loc, n)
        board = board - bl
    remaining = target - len(bishop_locs)
    # bishop locs, free spots
    agenda = [(bishop_locs, board)]
    while agenda:
        info = agenda.pop()
        biloc = info[0]
        spots = info[1]
        if len(biloc) == target:
            return biloc
        for spot in spots:
            new_biloc = biloc.copy()
            new_biloc.add(spot)
            agenda.append([new_biloc, spots-moves(spot, n)])
    return None

#############
# Problem 2 #
#############

class QuadTree():
    """
    Contains points that range between x values [x_start, x_end) 
    and y values [y_start, y_end).

    If the QuadTree is a leaf node, self.children should be None and 
    self.points should contain a set of at most four points.
    If the QuadTree is an internal (non-leaf) node, self.points should be None and 
    self.children should contain a list of four QuadTree nodes.

    The QuadTree should not have children with ranges that overlap.
    """
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.points = set()
        self.children = None

    def __str__(self, level=0):
        """
        Returns a string representation of the quadtree
        :param level: current level in the quadtree (level = 0 if node is the root)
        """
        ret = "\t"*level+"start:("+str(self.x_start)+", "+str(self.y_start)+\
                "), end:("+str(self.x_end)+", "+str(self.y_end)+")\n"
        if self.children is not None:
            for child in self.children:
                ret += child.__str__(level+1)
        else:  
            if len(self.points) == 0:
                ret += "\t"*(level+1)+"<No points>\n"
            for (x, y) in self.points:
                ret += "\t"*(level+1)+"("+str(x)+", "+str(y)+")\n"
        return ret

    def insert(self, point):
        """
        Insert a point into this quadtree by modifying the tree 
        directly, without returning anything.
        :param point: a tuple of 2 integers (x, y)
        """
        raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
