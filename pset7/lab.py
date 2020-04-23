#!/usr/bin/env python3
"""6.009 Lab 7: carlae Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!


class EvaluationError(Exception):
    """
    Exception to be raised if there is an error during evaluation other than a
    NameError.
    """
    pass


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """
    lines = source.splitlines()
    new = pre = ''
    chars = ('(', ')', ' ')
    for line in lines:
        new += ' '
        for c in line:
            if c == ';':
                break
            if c in chars:
                new += pre
                pre = ''
                new += ' ' + c + ' '
            else:
                pre += c
        new += pre
        pre = ''
    new += pre
    return new.split()


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    if tokens.count('(') != tokens.count(')'):
        raise SyntaxError
    def convert(thing):
        try:
            return int(thing)
        except:
            try:
                return float(thing)
            except:
                return thing
    def parse_expression(index, sub):
        # if first item is not '(' then must be standalone int, float, or var
        if sub[0] == ')':
            raise SyntaxError
        if sub[0] != '(':
            # return only item and index after last (0+1)
            if len(sub) == 1:
                return (convert(sub[0]), len(sub))
            else:
                raise SyntaxError
        else:
            result = []
            # start at 1, assume first item is '('
            i = 1
            # start past first '(', count it in
            left = 1
            right = 0
            while i < len(sub):
                # print('IR', i, result)
                t = sub[i]
                if t == '(':
                    left += 1
                    # print(i, sub[i:])
                    s, end = parse_expression(i, sub[i:])
                    # print("SE", s, end)
                    result.append(s)
                    i = end
                    # print('>>>', i, sub, len(sub))
                    if i == len(sub):
                        end = i-1
                        break
                    else:
                        t = sub[i]
                elif t == ')':
                    right += 1
                    i += 1
                else:
                    result.append(convert(t))
                    i += 1
                if left == right:
                    # print('LR', left, right, i, index, sub)
                    end = i-1
                    break
                if right > left:
                    raise SyntaxError
            return (result, end+1+index)
    return parse_expression(0, tokens)[0]

def mult(lis):
    prod = 1
    for i in lis:
        prod *= i
    return prod

def div(lis):
    quo = lis[0]
    for i in lis[1:]:
        quo /= i
    return quo

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': mult, 
    '/': div
}


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    # not list
    if not isinstance(tree, list):
        return tree
    # list
    if tree[0] in carlae_builtins.keys():
        # if something is a list
        if not all(not isinstance(item, list) for item in tree):
            for index, item in enumerate(tree):
                if isinstance(item, list):
                    tree[index] = evaluate(tree[index])
        # if all numbers
        result = carlae_builtins[tree[0]](tree[1:])
    else:
        raise EvaluationError
    return result


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    inp = ''
    while (inp != 'QUIT'):
        inp = input("Input: ")
        print("Output:", evaluate(inp))
