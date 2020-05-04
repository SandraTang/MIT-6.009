# No imports!


#############
# Problem 1 #
#############

with open('resources/words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

def split_words(s):
    """
    Takes string
    Yields tuples representing sequences of words
    iateanicecreamcone
    ateanicecreamcone
    teanicecreamcone
    """
    agenda = [['', s]]
    while agenda:
        both = agenda.pop(0)
        word = both[0]
        left = both[1]
        # 'base case'
        if len(left) == 0:
            yield tuple(word.split())
        # 'recursive'
        for i in range(len(left)):
            if is_word(left[:i+1]):
                agenda.append([word + left[:i+1] + ' ' , left[i+1:]])


############################################################
## Problem 2
############################################################

# Infinite lists

class InfiniteList:
    def __init__(self, f, d = None):
        """Create an infinite list where position i contains value f(i)."""
        self.f = f
        if d == None:
            self.d = {}
        else:
            self.d = d

    def __getitem__(self, i):
        """Standard Python method for defining notation ls[i], which expands to ls.__getitem__(i)"""
        if i in self.d.keys():
            return self.d[i]
        return self.f(i)

    def __setitem__(self, i, val):
        """Standard Python method for defining notation ls[i] = val, which expands to ls.__setitem__(i, val)"""
        self.d[i] = val

    def __iter__(self):
        """Standard Python method for producing a generator where called for, e.g. to loop over.
        Note that this iterator has infinitely many values to return, so a usual loop over it will never finish!
        It should yield values from index 0 to infinity, one by one."""
        i = 0
        while True:
            yield self[i]
            i += 1

    def __add__(self, other):
        """Standard Python method for defining notation a + b, which expands to a.__add__(b).
        For this quiz question, other will be another InfiniteList, and the generated InfiniteList should
        add the elements of self and other, at each position."""
        new_d = {}
        keys = set(self.d.keys()) | set(other.d.keys())
        for key in keys:
            new_d[key] = self[key] + other[key]
        return InfiniteList(lambda x: self.f(x) + other.f(x), new_d)

    def __mul__(self, other):
        """Standard Python method for defining notation a * b, which expands to a.__mul__(b).
        For this quiz question, other will be a number, and the generated InfiniteList should
        multiply each position of self by other."""
        for key in self.d.keys():
            self.d[key] = self.d[key]*other
        return InfiniteList(lambda x: self.f(x) * other, self.d)


##################################################
##  Problem 3
##################################################

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
        # horizontal, vertical
        result.add((x, i))
        result.add((i, y))
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

def k_queens_coverage(k, size):
    """
    Checks if it is possible to place less than or equal to 'k' queens on a
    chess board of size 'size' such that every cell on the board is
    reachable by at least one queen and no two queens can attack each other.
    Returns any such board if it is possible, otherwise returns None.

    Given:
        k: the maximum number of queens you may place on the board
        size: size of the chess board

    Returns:
        A 1-D array of length size representing any board that satisfies
        the problem. Each index (i) in the array represents column i of the
        board. If there is a queen placed on column i, array[i] must equal
        the row index of the queen. If no queen is placed on column i,
        array[i] = -1. If there is no such board that satisfies the problem,
        return None.
    """
    agenda = []
    # generate possible locations
    locations = locs(size)
    # try positions in top quarter (first move idential reflected over axes)
    guesses = locs((size+1)//2)
    for guess in guesses:
        # 1D array, free spaces left
        arr = [-1]*5
        arr[guess[1]] = guess[0]
        agenda.append([arr, locations-moves(guess, size)])
    # djikstra's while loop
    while agenda:
        info = agenda.pop(0)
        board = info[0]
        free = info[1]
        if free == set():
            return board
        for spot in free:
            new_board = board.copy()
            new_board[spot[1]] = spot[0]
            agenda.append([new_board, free-moves(spot, size)])
    return None


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
