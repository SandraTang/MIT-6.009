#!/usr/bin/env python3
import os, unittest, pickle, marshal, types, json
import quiz

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

class TestProblem1(unittest.TestCase):
    def test_01(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', 'b', ('+', ('+', 3, 5), 'c')))),
                         ('+', 'a', ('+', 'b', ('+', 8, 'c'))))

    def test_02(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', ('*', ('+', 3, 5), 6), 'b'))),
                         ('+', 'a', ('+', 48, 'b')))

    def test_03(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', ('*', 'b', 0), 'c'))),
                         ('+', 'a', 'c'))

    def test_04(self):
        self.assertEqual(quiz.constant_fold(('*', 1, ('+', 0, ('*', ('+', 'x', 0), 1)))),
                         'x')

    def test_05(self):
        self.assertEqual(quiz.constant_fold(('+', 7, ('*', 'x', ('-', 7, ('+', 4, 3))))),
                         7)

    def test_06(self):
        self.assertEqual(quiz.constant_fold(('*', 'a', ('-', 'b', 0))),
                         ('*', 'a', 'b'))

    def test_07(self):
        self.assertEqual(quiz.constant_fold(('+', 1, ('*', 2, ('-', 3, 2)))),
                         3)

    def test_08(self):
        self.assertEqual(quiz.constant_fold(('+', 'x', ('+', 'x', 'x'))),
                         ('+', 'x', ('+', 'x', 'x')))


#############
# Problem 2 #
#############

class TestProblem2(unittest.TestCase):
    allwords = frozenset(open('words2.txt').read().splitlines())

    def test_01(self):
        top = 'at'; total_squares = 3
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=3, check_total=-1)

    def test_02(self):
        top = 'is'; total_squares = 2
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=2, check_total=total_squares)
        # Generator should work more than once within same process...
        top = 'ad'; total_squares = 3
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=2, check_total=total_squares)

    def test_03(self):
        top = 'bar'; total_squares = 1743
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=1743, check_total=total_squares)

    def test_04(self):
        top = 'fast'; total_squares = 202505
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=20, check_total=total_squares)

    def test_05(self):
        top = 'drink'; total_squares = 673052
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=20, check_total=total_squares)

    def test_06(self):
        top = 'zoologists'; total_squares = 0
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=total_squares, check_total=total_squares)

    def check_square(self, top, result_gen, check_n=0, check_total=-1):
        self.assertIsInstance(result_gen, types.GeneratorType, "word_squares should be a generator")
        if check_n >= 0: # verify first check_n yields from result_gen
            results = self.get_some(result_gen, check_n)
            self.validate(top, results, check_n)
        if check_total >= 0: # verify total count of items from generator is correct
            results += list(result_gen)
            self.validate(top, results, check_total)

    def validate(self, top, results, count):
        # Validate that list of results are all (non-duplicative)
        # square_word tuples, and the right number of results are
        # provided.
        for res in results:
            self.assertIsInstance(res, tuple, msg="word_squares should yield tuples")
            words = set(res)
            self.assertEqual(len(res), 4, msg="tuples from word_squares should have 4 different strings")
            for w in res:
                self.assertIn(w, TestProblem2.allwords, msg="word in result is not in words2.txt")

            top, right, bot, left = res
            self.assertEqual(top[0], left[0])
            self.assertEqual(top[-1], right[0])
            self.assertEqual(bot[0], left[-1])
            self.assertEqual(bot[-1], right[-1])

        rset = set(results)
        self.assertEqual(len(rset), len(results), msg="word_squares should not yield duplicates")
        self.assertEqual(len(results), count, "wrong number of square_word tuples produced")

    def get_some(self, g, n):
        res = []
        for i in range(n):
            try: res.append(next(g))
            except StopIteration: pass
        return res


#############
# Problem 3 #
#############

from trie import Trie, RadixTrie
from text_tokenize import tokenize_sentences


def dictify(t):
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def make_word_trie(words):
    t = Trie()
    for word, val in words:
        t[word] = val
    return t


def get_words(text):
    return [tuple(i.split()) for i in tokenize_sentences(text, True)]


def is_radix_trie(t):
    if not isinstance(t, RadixTrie):
        return False

    return all(is_radix_trie(i) for i in t.children.values())


class Quiz2TestCase(unittest.TestCase):
    def _run_test(self, n):
        import resource
        resource.setrlimit(resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

        in_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                                '%s_%d_in.pyobj' % (self.test_name, n))
        with open(in_fname, encoding='utf-8') as f:
            inp = eval(f.read())
        out_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                                 '%s_%d_out.pyobj' % (self.test_name, n))
        with open(out_fname, encoding='utf-8') as f:
            expected = eval(f.read())

        result = self.get_result(inp)
        self.assertEqual(result, expected)

class TestProblem3(Quiz2TestCase):
    test_name = 'trie'

    def get_result(self, inp):
        inp = make_word_trie(inp)
        original = dictify(inp)
        out = quiz.compress_trie(inp)
        self.assertEqual(original, dictify(inp), "Your function should not modify the given Trie.")
        self.assertTrue(is_radix_trie(out), "Your function should return an instance of RadixTrie.")
        return dictify(out)

    def test_01(self):
        self._run_test(1)

    def test_02(self):
        self._run_test(2)

    def test_03(self):
        self._run_test(3)

    def test_04(self):
        self._run_test(4)

    def test_05(self):
        self._run_test(5)

    def test_06(self):
        self._run_test(6)

    def test_07(self):
        self._run_test(7)

    def test_08(self):
        self._run_test(8)



if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
