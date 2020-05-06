# No imports!


#############
# Problem 1 #
#############

def constant_fold(expr):
    """Simplify parts of the expression whose constant values we can predict in advance,
    according to the rules set out in the quiz document.

    >>> constant_fold(1)
    1
    >>> constant_fold('x')
    'x'
    >>> constant_fold(('+', 2, 3))
    5
    >>> constant_fold(('+', 'x', ('*', 8, 3)))
    ('+', 'x', 24)
    >>> constant_fold(('*', 'x', ('-', 8, 7)))
    'x'
    """
    def check(expr):
        if isinstance(expr, int) or isinstance(expr, str) or isinstance(expr, float):
            return expr
        # must be list
        if expr[0] == '+' or expr[0] == '-':
            if expr[1] == 0:
                return expr[2]
            elif expr[2] == 0:
                return expr[1]
        elif expr[0] == '*':
            if expr[1] == 0 or expr[2] == 0:
                return 0
            elif expr[1] == 1:
                return expr[2]
            elif expr[2] == 1:
                return expr[1]
        if isinstance(expr[1], int) and isinstance(expr[2], int):
            if expr[0] == '+':
                return expr[1] + expr[2]
            elif expr[0] == '-':
                return expr[1] - expr[2]
            elif expr[0] == '*':
                return expr[1] * expr[2]
            elif expr[0] == '/':
                return expr[1] / expr[2]
        full = ()
        for part in expr:
            full = full + tuple([check(part)])
        return full
    while check(expr) != expr:
        expr = check(expr)
    return expr


#############
# Problem 2 #
#############

allwords = set(open('words2.txt').read().splitlines())

def word_squares(top):
    """ Yield (top, right, bottom, left) word squares """
    raise NotImplementedError


#############
# Problem 3 #
#############


from trie import Trie, RadixTrie


def dictify(t):
    """
    For debugging purposes.  Given a trie (or radix trie), return a dictionary
    representation of that structure, including the value and children
    associated with each node.
    """
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def compress_trie(trie):
    raise NotImplementedError



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
