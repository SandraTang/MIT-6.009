#!/usr/bin/env python3
import quiz
import os, unittest, collections, types
from copy import deepcopy

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
##  Problem 1
##################################################

class TestProblem1(unittest.TestCase):
    def test_01(self):
        S = [1, 2]; W = [0.8, 0.7]
        expect = [1.5, 2.3]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)

    def test_02(self):
        S = [1, 5, 6, 7]; W = [1]
        expect = [1, 5, 6, 7]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)

    def test_03(self):
        S = [1, 5, 6, 7]; W = [0.5, 0.5]
        expect = [1.0, 3.0, 5.5, 6.5]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)

    def test_04(self):
        S = [1, 5, 6, 7]; W = [0, 1]
        expect = [1, 1, 5, 6]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)

    def test_05(self):
        S = [1, 5, 6, 7]; W = [1, 0]
        expect = [1, 5, 6, 7]
        result = quiz.trailing_weighted_average(S, W)
        self.assertEqual(expect, result)
        result = quiz.trailing_weighted_average(S, W)
        self.assertEqual(expect, result, "okay on first call, but not second!")

    def test_06(self):
        S = [1, 5, 6, 7]; W = [2, 0, 0, 0, 100]
        expect = [102, 110, 112, 114]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)

    def test_07(self):
        S = list(range(1,18)); W = list(range(10,0,-1))
        expect = [55, 65, 84, 111, 145, 185, 230, 279, 331, 385, 440, 495, 550, 605, 660, 715, 770]
        result = quiz.trailing_weighted_average(deepcopy(S), deepcopy(W))
        self.assertEqual(expect, result)
                

##################################################
##  Problem 2
##################################################

class TestProblem2(unittest.TestCase):
    def test_01(self):
        s = set(range(5))
        n = 1
        expect = {(0,), (1,), (2,), (3,), (4,)}
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_02(self):
        s = set(range(5))
        n = 2
        expect = {(0, 1), (3, 4), (2, 3), (1, 2)}
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_03(self):
        s = set(range(5))
        n = 5
        expect = {(0, 1, 2, 3, 4)}
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_04(self):
        s = set(range(5))
        n = 6
        expect = set()
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_05(self):
        s = set(range(0, 5, 2))
        n = 1
        expect = {(2,), (0,), (4,)}
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

        s = set(range(0, 5, 2))
        n = 2
        expect = set()
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_06(self):
        s = {0, 83, 2, 3, 81, 7, 82}
        n = 2
        expect = {(81, 82), (2, 3), (82, 83)}
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_07(self):
        # big set
        s1 = list(range(50)); r1 = {(a,b,c) for a,b,c in zip(s1,s1[1:],s1[2:])}
        s2 = list(range(200,300,2)); r2 = set() 
        s3 = list(range(100,150)); r3 = {(a,b,c) for a,b,c in zip(s3,s3[1:],s3[2:])}
        s = set(s1) | set(s2) | set(s3)
        n = 3
        expect = r1 | r2 | r3
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

    def test_08(self):
        s = set(range(10))
        n = 11
        expect = set()
        result = quiz.all_consecutives(s, n)
        self.assertEqual(expect, result)

                
##################################################
##  Problem 3
##################################################

class TestProblem3(unittest.TestCase):

    # Tiny cases
    def test_01(self):
        seq1, seq2 = '', ''
        expect = 0
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    def test_02(self):
        seq1, seq2 = 'a', ''
        expect = 1
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

        seq1, seq2 = '', 'a'
        expect = 1
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    def test_03(self):
        seq1, seq2 = 'a', 'b'
        expect = 1
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    def test_04(self):
        seq1, seq2 = 'ab', 'b'
        expect = 1
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

        seq1, seq2 = 'b', 'ab'
        expect = 1
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    def test_05(self):
        seq1, seq2 = 'aa', 'bb'
        expect = 2
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    # Small cases
    def test_06(self):
        subcases = [('mast', 'mast', 0),
                    ('mast', 'must', 1),
                    ('misty', 'must', 2),
                    ('color', 'colour', 1),
                    ('aba', 'bbb', 2),
                    ('aba', 'bab', 2)]
        i = 0
        for seq1, seq2, expect in subcases:
            i += 1
            with self.subTest(subcase=i):
                result = quiz.cost_to_consume(seq1, seq2)
                self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    # Medium cases              
    def test_07(self):
        # Harder cases
        subcases = [('car', 'boat', 3),
                    ('a', 'bbbbbb', 6),
                    ('frog', 'apple', 5)]
        i = 0
        for seq1, seq2, expect in subcases:
            i += 1
            with self.subTest(subcase=i):
                result = quiz.cost_to_consume(seq1, seq2)
                self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    # Long case
    def test_08(self):
        size = 8
        seq1, seq2, expect = ('a'*size, 'b'*size, size)
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")
        
    # Longer case not run on quiz
    def skip_test_09(self):
        size = 9
        seq1, seq2, expect = ('a'*size, 'b'*size, size)
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")
        
    # Hard case not run on quiz
    def skip_test_10(self):
        #
        # Try this one if you want a challenge!
        #
        subcases = [('supercalafragilistic', 'sypercalafragilistic', 1), 
                    ('supercalifragilisticexpialidocious', 'sypercalifragilisticexpialidocious', 1), 
                    ('supercalifragilisticexpialidocious', 'supercalifragilisticexpialidoxious', 1), 
                   ]
        i = 0
        for seq1, seq2, expect in subcases:
            i += 1
            with self.subTest(subcase=i):
                result = quiz.cost_to_consume(seq1, seq2)
                self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")

    # Hard case not run on quiz
    def skip_test_11(self):
        #
        # Try this one if you want an even bigger challenge!
        #
        size = 20
        seq1, seq2, expect = ('a'*size, 'b'*size, size)
        result = quiz.cost_to_consume(seq1, seq2)
        self.assertEqual(expect, result, "wrong cost_to_consume("+repr(seq1)+","+repr(seq2)+")")
        
                
if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
