#!/usr/bin/env python3
import quiz
import os, unittest, collections, types
from copy import deepcopy

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
##  Problem 1
##################################################

# class TestProblem1(unittest.TestCase):
#     tree1 = [13,
#              [7],
#              [8,
#               [99],
#               [16,
#                [77]],
#               [42]]]

#     tree2 = [7,
#              [3,
#               [4],
#               [1,
#                [7]],
#               [2]],
#              [8,
#               [1]]]

#     def validate(self, expect, result):
#         for e in expect:
#             self.assertEqual(expect.count(e), result.count(e))

#     def test_01(self):
#         tree = self.tree2
#         depth = 0
#         expect = [7]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_02(self):
#         tree = self.tree2
#         depth = 1
#         expect = [3, 8]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_03(self):
#         tree = self.tree2
#         depth = 2
#         expect = [4, 1, 2, 1]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.validate(expect, result)

#     def test_04(self):
#         tree = self.tree2
#         depth = 3
#         expect = [7]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_05(self):
#         tree = self.tree2
#         depth = 4
#         expect = []
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_06(self):
#         tree = []
#         depth = 1
#         expect = []
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_07(self):
#         # multiple depths for tree1
#         tree = self.tree1

#         depth = 0
#         expect = [13]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#         depth = 1
#         expect = [7, 8]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#         depth = 2
#         expect = [99, 16, 42]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#         depth = 4
#         expect = []
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.assertEqual(expect, result, "wrong result at depth "+str(depth))

#     def test_08(self):
#         # big tree
#         count, rep = 200, 3
#         tree = self.make_tree([i%rep for i in range(count)])
#         depth = 4
#         expect = [1, 0, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 2]
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.validate(expect, result)

#     def test_09(self):
#         # big tree
#         count, rep = 200, 70
#         tree = self.make_tree([i%rep for i in range(count)])
#         depth = 4
#         expect = []
#         result = quiz.vals_at_depth(deepcopy(tree), depth)
#         self.validate(expect, result)

#     def make_tree(self, L):
#         n = len(L)
#         if n == 0: return []
#         val = L[0]
#         if n == 1: return [val]
#         split = (n-1)//2
#         left = self.make_tree(L[1:split+1])
#         right = self.make_tree(L[split+1:])
#         return [val, left, right] if left else [val, right]


##################################################
##  Problem 2
##################################################

# class TestProblem2(unittest.TestCase):

#     def test_01(self):
#         seq1 = ['a', 'a']
#         seq2 = ['b', 'b']
#         expect = ['a', 'b', 'a', 'b']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_02(self):
#         seq1 = [1, 2]
#         seq2 = [3, 4, 5, 6]
#         expect = [1, 3, 2, 4, 5, 6]
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_03(self):
#         seq1 = [1, 2]
#         seq2 = [1, 3]
#         expect = [1, 3, 2]
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_04(self):
#         seq1 = ['a', 'b']
#         seq2 = ['b', 'c']
#         expect = ['a', 'b', 'c']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_05(self):
#         seq1 = ['a', 'b', 'd']
#         seq2 = ['a', 'c']
#         expect = ['a', 'c', 'b', 'd']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_06(self):
#         seq1 = list('abccae')
#         seq2 = list('babbaf')
#         expect = ['a', 'b', 'c', 'a', 'c', 'b', 'a', 'b', 'e', 'a', 'f']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_07(self):
#         seq1 = ['a']*10
#         seq2 = ['b']
#         expect  = ['a','b','a']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#         seq1 = ['b']
#         seq2 = ['a']*10
#         expect  = ['b','a']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_08(self):
#         # should work for spaces and zeros too
#         seq1 = ['a', ' ', 'b']
#         seq2 = ['d', 'e', 'f']
#         expect  = ['a','d', ' ', 'e', 'b', 'f']
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#         seq1 = [0, 0]
#         seq2 = [1, 3]
#         expect  = [0, 1, 0, 3]
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)

#     def test_09(self):
#         seq1 = list('this is a long random sentence and sequence we want to weave')
#         seq2 = list('and another longish sentence to see what gibberish results')
#         expect = list('tahnids iasn oat hleorn gl ornagnidsohm sentence taon '
#                       'ds eseq uwehnacte wgei bwbaenrti stho wresauvlets')
#         result = quiz.weave(seq1, seq2)
#         self.assertEqual(expect, result)
            
                
##################################################
##  Problem 3
##################################################

class TestProblem3(unittest.TestCase):
    world1 = {"nrows": 5, "ncols": 6,
              "grid": [[None, None, 'G', None, 'R', None],
                       ['R', 'R', 'R', 'R', None, None],
                       [None, None, None, 'R', None, None],
                       ['B', 'B', None, 'G', 'G', 'G'],
                       ['B', 'B', None, None, None, None]]}
    world_empty = {"nrows": 1, "ncols": 1, "grid": [[None]]}

    def test_01(self):
        # empty world
        world = deepcopy(self.world_empty)
        expect = []
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_02(self):
        # single blob, single square
        world = {"nrows": 1, "ncols": 3, 
                 "grid": [[None, 'R', None]]}
        expect = [['R', {(0,1)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_03(self):
        # single blob, multiple squares
        world = {"nrows": 1, "ncols": 3, 
                 "grid": [['R', 'R', None]]}
        expect = [['R', {(0,0), (0,1)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_04(self):
        # single bigger blob
        world = {"nrows": 2, "ncols": 3, 
                 "grid": [['R', 'R', 'R'],
                          ['R', 'R', 'R']]}
        expect = [['R', {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_05(self):
        # two blobs, same value
        world = {"nrows": 1, "ncols": 3, 
                 "grid": [['R', None, 'R']]}
        expect = [['R', {(0,0)}], ['R', {(0,2)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_06(self):
        # two blobs, different values
        world = {"nrows": 2, "ncols": 3, 
                 "grid": [['R', 'R', None],
                          [None, 'B', 'B']]}
        expect = [['R', {(0,0), (0,1)}],
                  ['B', {(1,1), (1,2)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_07(self):
        # one meandering blob
        world = {"nrows": 2, "ncols": 3, 
                 "grid": [['R', 'R', None],
                          [None, 'R', 'R']]}
        expect = [['R', {(0,0), (0,1), (1,1), (1,2)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_08(self):
        # many blobs (world1 from example)
        world = deepcopy(self.world1)
        expect = [['G', {(0, 2)}], ['R', {(0, 4)}], 
                  ['R', {(1, 2), (1, 3), (1, 0), (2, 3), (1, 1)}], 
                  ['B', {(3, 0), (3, 1), (4, 1), (4, 0)}], 
                  ['G', {(3, 4), (3, 3), (3, 5)}]]
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def test_09(self):
        # intermingled blobs, all with only one square each
        nr = 4; nc = 5
        world = {"nrows": nr, "ncols": nc, 
                 "grid": [['R', 'B', 'R', 'B', 'R'],
                          ['B', 'R', 'B', 'R', 'B'],
                          ['R', 'B', 'R', 'B', 'R'],
                          ['B', 'R', 'B', 'R', 'B']]}
        expect = [['B' if (r+c)%2 else 'R', {(r,c)}]
                    for r in range(nr)
                      for c in range(nc)]
        result = quiz.all_blobs(deepcopy(world))
        self.validate(expect, result)

    def test_10(self):
        # big world
        nr = 40; nc = 50; nh = 5
        grid = []
        expect = []
        for r in range(0,nr,nh):
            part = [str(r%3), set()]
            for h in range(nh):
                grid.append([str(r%3) for c in range(nc)])
                part[1] |= set((r+h,c) for c in range(nc))
            expect.append(part)
        world = {"nrows": nr, "ncols": nc, "grid": grid}
        result = quiz.all_blobs(world)
        self.validate(expect, result)

    def validate(self, expect, result):
        self.assertIsInstance(result, list)
        self.assertEqual(len(expect), len(result), "wrong number of blobs in result")
        for blob in result:
            self.valid_blob(blob)
        for exp in expect:
            self.assertTrue(exp in result, "blob "+repr(exp)+" missing from result")
            
    def valid_blob(self, blob):
        self.assertIsInstance(blob, list, "malformed blob: blob should be a list")
        self.assertEqual(len(blob), 2, "malformed blob: should be of form [<val>, <set>]")
        self.assertIsInstance(blob[1], set, "malformed blob: should be of form [<val>, <set>]")
        self.assertGreaterEqual(len(blob[1]), 1, "malformed blob: blob should have at least one square")
        for square in blob[1]:
            self.assertIsInstance(square, tuple, "malformed blob: squares should be tuples")
            self.assertEqual(2, len(square), "malformed blob: square should be tuples (r, c)")
        return True


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
