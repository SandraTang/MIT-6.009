#!/usr/bin/env python3
import os
import copy
import math
import quiz
import types
import pickle
import hashlib
import unittest

from collections import Counter

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
#  Problem 1
##################################################

# def testfunc1(a, b):
#     return a + b*2

# def testfunc2(a, b):
#     return a - b

# def testfunc3(a, b):
#     return -(a ^ b)

# def testfunc4(a, b):
#     return a

# def testfunc5(a, b):
#     return b

# testfunc6 = (lambda x: (lambda a, b: b-a+x))(3)

# def testfunc7maker():
#     funcs = {
#         0: lambda a, b: a+b,
#         1: lambda a, b: a-b,
#         2: lambda a, b: a+b,
#         3: lambda a, b: b-a,
#     }

#     def _inner(a, b):
#         return funcs[a % 4](a, b)

#     return _inner
# testfunc7 = testfunc7maker()

# class TestProblem1(unittest.TestCase):
#     def _run_test(self, func, test_num):
#         with open(os.path.join(TEST_DIRECTORY, 'test_inputs', f'seq_{test_num:02d}.pickle'), 'rb') as f:
#             inps = pickle.load(f)

#         with open(os.path.join(TEST_DIRECTORY, 'test_outputs', f'seq_{test_num:02d}.pickle'), 'rb') as f:
#             expected = pickle.load(f)

#         for ix, (a, b, indices) in enumerate(inps):
#             seq = quiz.genseq(func, a, b)
#             self.assertIsInstance(seq, types.GeneratorType, msg="genseq should return a generator!")
#             out = []
#             for o in indices:
#                 for _ in range(o):
#                     next(seq)
#                 out.append(next(seq))

#             for got, exp in zip(out, expected[ix]):
#                 self.assertTrue(got == exp)

#     def test_00_fib(self):
#         seq = quiz.genseq(lambda a,b: a+b, 0, 1)
#         self.assertIsInstance(seq, types.GeneratorType, msg="genseq should return a generator!")
#         exp = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
#         for r, e in zip(seq, exp):
#             self.assertEqual(r, e)

#     def test_01(self):
#         self._run_test(testfunc3, 2)

#     def test_02(self):
#         self._run_test(testfunc4, 3)

#     def test_03(self):
#         self._run_test(testfunc5, 4)

#     def test_04(self):
#         self._run_test(testfunc6, 5)

#     def test_05(self):
#         self._run_test(testfunc7, 6)

#     def test_06(self):
#         self._run_test(testfunc2, 1)

#     def test_07(self):
#         self._run_test(testfunc1, 0)


##################################################
#  Problem 2
##################################################

def valid_mapping(results, people, food):
    if results is None:
        return "invalid results: got None, expected something else"

    invalid = set(results) - set(people)
    if invalid:
        return "invalid people in response: %s" % invalid

    not_fed = set(people) - set(results)
    if not_fed:
        return "these people did not get fed: %s" % not_fed

    for p, f in results.items():
        if f not in people[p]:
            return "%s does not want %s but was given them" % (p, f)

    hist = Counter(results.values())
    for f, count in hist.items():
        if count > food[f]:
            return '%s was assigned more than %s times' % (f, food[f])

    return None

# class TestProblem2(unittest.TestCase):
#     def _run_test(self, number):
#         with open(os.path.join(TEST_DIRECTORY, 'test_inputs', f'food_{number:02d}.pickle'), 'rb') as f:
#             inps = pickle.load(f)
#         inps2 = copy.deepcopy(inps)

#         results = []
#         for inp in inps:
#             results.append(quiz.feed(*inp))

#         with open(os.path.join(TEST_DIRECTORY, 'test_outputs', f'food_{number:02d}.pickle'), 'rb') as f:
#             expected = pickle.load(f)

#         for inp, inp2, res, exp in zip(inps, inps2, results, expected):
#             self.assertEqual(inp, inp2, 'Make sure your function does not mutate the inputs!')

#             if exp is False:
#                 self.assertEqual(res, None, 'For inputs:\n%s\n%s\nexpected None, got %s' % (*inp2, res))
#             else:
#                 msg = valid_mapping(res, *inp2)
#                 self.assertEqual(msg, None, 'For inputs:\n%s\n%s\n%s' % (*inp2, msg))

#     def test_00_examples(self):
#         res1 = quiz.feed({'alice': ['pickles'], 'bob': ['ketchup']},
#                          {'pickles': 1, 'ketchup': 1})
#         self.assertEqual(res1, {'alice': 'pickles', 'bob': 'ketchup'})

#         res2 = quiz.feed({'alice': ['pickles'], 'bob': ['pickles']},
#                          {'pickles': 1, 'ketchup': 1})
#         self.assertEqual(res2, None)

#         res3 = quiz.feed({'alice': ['pickles'], 'bob': ['pickles']},
#                          {'pickles': 2, 'ketchup': 1})
#         self.assertEqual(res3, {'alice': 'pickles', 'bob': 'pickles'})

#         res4 = quiz.feed({
#             'alice': ['pickles', 'ketchup'],
#             'bob': ['chips', 'onions'],
#             'candace': ['pie', 'broccoli'],
#             'dave': ['pickles'],
#             'emery': ['onions'],
#             'fergus': ['pie'],
#         }, {
#             'pickles': 1,
#             'ketchup': 1,
#             'chips': 1,
#             'onions': 1,
#             'pie': 1,
#             'broccoli': 1,
#         })
#         self.assertEqual(res4, {
#             'alice': 'ketchup',
#             'bob': 'chips',
#             'candace': 'broccoli',
#             'dave': 'pickles',
#             'emery': 'onions',
#             'fergus': 'pie',
#         })

#         res5 = quiz.feed({
#             'alice': ['cake', 'cheese', 'pie', 'sandwiches'],
#             'bob': ['cake', 'cheese', 'pie'],
#             'candace': ['cake', 'cheese'],
#             'dave': ['cake', 'cheese'],
#             'emery': ['cake', 'cheese']
#         }, {'cake': 2, 'cheese': 1, 'pie': 1, 'sandwiches': 1})
#         self.assertEqual(res5['alice'], 'sandwiches')
#         self.assertEqual(res5['bob'], 'pie')
#         self.assertEqual(sorted((res5['candace'], res5['dave'], res5['emery'])),
#                          ['cake', 'cake', 'cheese'])

#     def test_01(self):
#         self._run_test(0)

#     def test_02(self):
#         self._run_test(1)

#     def test_03(self):
#         self._run_test(2)

#     def test_04(self):
#         self._run_test(3)

#     def test_05(self):
#         self._run_test(4)

#     def test_06(self):
#         self._run_test(5)

#     def test_07(self):
#         self._run_test(6)


##################################################
#  Problem 3
##################################################

class TestProblem3(unittest.TestCase):
    with open(os.path.join(TEST_DIRECTORY, 'test_inputs', 'hanson.txt'), 'rb') as f:
        hanson = f.read().decode('utf-8')

    def _load_test_file(self, name):
        with open(os.path.join(TEST_DIRECTORY, 'test_outputs', name), 'rb') as f:
            return pickle.load(f)

    def _check_pattern_results(self, pattern, text, expected):
        result = [pattern.match(text, ix) for ix in range(len(text))]
        self.assertEqual(result, self._load_test_file(expected))

    def test0_dot(self):
        p = quiz.Dot()
        self.assertEqual(p.match('hello'), (0, 1, 'h'))
        self.assertEqual(p.match('hello', 1), (1, 2, 'e'))
        self.assertEqual(p.match(''), None)
        self._check_pattern_results(p, self.hanson, 'hanson.match.dot.pickle')

    def test1_verbatim(self):
        p = quiz.Verbatim('cat')
        self.assertEqual(p.match('cat'), (0, 3, 'cat'))
        self.assertEqual(p.match(' cat', 1), (1, 4, 'cat'))
        self.assertEqual(p.match(' cat', 0), None)
        self.assertEqual(p.match('ca', 0), None)
        self._check_pattern_results(quiz.Verbatim('Hanson'), self.hanson, 'hanson.match.ver.pickle')
        self._check_pattern_results(quiz.Verbatim('music'), self.hanson, 'hanson.match.ver2.pickle')

    def test2_charfrom(self):
        p = quiz.CharFrom('abc')
        self.assertEqual(p.match('bacdef'), (0, 1, 'b'))
        self.assertEqual(p.match(' cabdef', 1), (1, 2, 'c'))
        self.assertEqual(p.match(' cabdef', 0), None)
        self.assertEqual(p.match('defcab', 2), None)
        self._check_pattern_results(quiz.CharFrom('Hanson'), self.hanson, 'hanson.match.cf.pickle')
        self._check_pattern_results(quiz.CharFrom('music'), self.hanson, 'hanson.match.cf2.pickle')

    def test3_charnotfrom(self):
        p = quiz.CharNotFrom('abc')
        self.assertEqual(p.match('bacdef'), None)
        self.assertEqual(p.match(' fedcab', 1), (1, 2, 'f'))
        self.assertEqual(p.match(' fedcab', 4), None)
        self.assertEqual(p.match(' defcab', 0), (0, 1, ' '))
        self.assertEqual(p.match('defcab', 2), (2, 3, 'f'))
        self._check_pattern_results(quiz.CharNotFrom('Hanson'), self.hanson, 'hanson.match.cnf.pickle')
        self._check_pattern_results(quiz.CharNotFrom('music'), self.hanson, 'hanson.match.cnf2.pickle')

    def test4_star(self):
        p = quiz.Star(quiz.CharFrom('abc'))
        self.assertEqual(p.match('bacdef'), (0, 3, 'bac'))
        self.assertEqual(p.match('bacdef', 1), (1, 3, 'ac'))
        self.assertEqual(p.match('bacdef', 2), (2, 3, 'c'))
        self.assertEqual(p.match('bacdef', 3), (3, 3, ''))
        self.assertEqual(p.match('bacdef', 4), (4, 4, ''))
        self.assertEqual(p.match('abababababababababababababababababababccccccccccccdef', 4), (4, 50, 'abababababababababababababababababcccccccccccc'))
        self.assertEqual(p.match('abababababababababababababababababababccccccccccccdef', 51), (51, 51, ''))
        self._check_pattern_results(quiz.Star(quiz.CharNotFrom('Hanson')), self.hanson, 'hanson.match.star.pickle')
        self._check_pattern_results(quiz.Star(quiz.CharFrom('music')), self.hanson, 'hanson.match.star2.pickle')

    def test5_sequence(self):
        p = quiz.Sequence([quiz.CharFrom('abc'), quiz.CharFrom('df'), quiz.Verbatim('e')])
        self.assertEqual(p.match('bacdef'), None)
        self.assertEqual(p.match('bacdef', 1), None)
        self.assertEqual(p.match('bacdef', 2), (2, 5, 'cde'))
        self.assertEqual(p.match('bacdef', 3), None)
        self.assertEqual(p.match('bacdef', 4), None)
        self.assertEqual(p.match('bacdf', 2), None)
        self._check_pattern_results(quiz.Sequence([quiz.CharFrom('Hanson'), quiz.CharNotFrom('Hanson')]), self.hanson, 'hanson.match.seq.pickle')
        self._check_pattern_results(quiz.Sequence([quiz.Verbatim('at '), quiz.CharFrom('rstlne')]), self.hanson, 'hanson.match.seq2.pickle')

    def test6_alternatives(self):
        p = quiz.Alternatives([quiz.CharFrom('abc'), quiz.CharFrom('df'), quiz.Verbatim('e')])
        self.assertEqual(p.match('bacz1d2ef', 0), (0, 1, 'b'))
        self.assertEqual(p.match('bacz1d2ef', 1), (1, 2, 'a'))
        self.assertEqual(p.match('bacz1d2ef', 2), (2, 3, 'c'))
        self.assertEqual(p.match('bacz1d2ef', 3), None)
        self.assertEqual(p.match('bacz1d2ef', 4), None)
        self.assertEqual(p.match('bacz1d2ef', 5), (5, 6, 'd'))
        self.assertEqual(p.match('bacz1d2ef', 6), None)
        self.assertEqual(p.match('bacz1d2ef', 7), (7, 8, 'e'))
        self.assertEqual(p.match('bacz1d2ef', 8), (8, 9, 'f'))
        self._check_pattern_results(quiz.Alternatives([quiz.CharFrom('Hanson '), quiz.Verbatim('the')]), self.hanson, 'hanson.match.alt.pickle')

    def test7_repeat(self):
        p = quiz.Repeat(quiz.Verbatim('cat'), 2, 4)
        self.assertEqual(p.match('cat', 0), None)
        self.assertEqual(p.match('catcat', 0), (0, 6, 'catcat'))
        self.assertEqual(p.match('catcat', 1), None)
        self.assertEqual(p.match('catcatcatcatcat', 0), (0, 12, 'catcatcatcat'))
        self.assertEqual(p.match('catcatcatcatcat', 4), None)
        self.assertEqual(p.match('catcatcatcatcat', 6), (6, 15, 'catcatcat'))
        self.assertEqual(p.match('catcatcatcatcat', 9), (9, 15, 'catcat'))
        self.assertEqual(p.match('catcatcatcatcat', 12), None)
        self._check_pattern_results(quiz.Repeat(quiz.CharFrom('abcdefghijklm'), 2, 4), self.hanson, 'hanson.match.rep.pickle')
        self._check_pattern_results(quiz.Repeat(quiz.CharFrom('abcdefghijklm'), 2, 2), self.hanson, 'hanson.match.rep2.pickle')

    def test_integration0_date(self):
        p = self._make_patterns()['date']
        self.assertEqual(p.match('2018-12-05'), (0, 10, '2018-12-05'))
        self.assertEqual(p.match('2018-12-92'), None)
        self.assertEqual(p.match('20181205'), None)
        self._check_pattern_results(p, self.hanson, 'hanson.match.date.pickle')

    def test_integration1_ip_address(self):
        p = self._make_patterns()['ip']
        with open(os.path.join(TEST_DIRECTORY, 'test_inputs', 'ip.txt'), 'rb') as f:
            ip_text = f.read().decode('utf-8')
        self._check_pattern_results(p, ip_text, 'ip.match.pickle')
        self._check_pattern_results(p, self.hanson, 'hanson.match.ip.pickle')

    def test_integration2_quoted_text(self):
        p = self._make_patterns()['quoted']
        self._check_pattern_results(p, self.hanson, 'hanson.match.quoted.pickle')

    def test_integration3_url(self):
        p = self._make_patterns()['url']
        self._check_pattern_results(p, self.hanson, 'hanson.match.url.pickle')

    def _find_all_test(self, name):
        pattern = self._make_patterns()[name]
        expected = self._load_test_file('hanson.find_all.%s.pickle' % name)
        result = pattern.find_all(self.hanson)
        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(list(result), expected)

    def test_last_find_all_1(self):
        self._find_all_test('date')

    def test_last_find_all_2(self):
        self._find_all_test('url')

    def test_last_find_all_3(self):
        self._find_all_test('ip')

    def test_last_find_all_4(self):
        self._find_all_test('quoted')

    def test_last_find_all_5(self):
        self._find_all_test('hha')

    def test_last_find_all_deffed(self):
        classes = [quiz.Dot, quiz.Verbatim, quiz.CharFrom, quiz.CharNotFrom,
                   quiz.Star, quiz.Sequence, quiz.Alternatives, quiz.Repeat]
        methods = set()
        for cls in classes:
            find_all = getattr(cls, 'find_all', None)
            self.assertNotEqual(find_all, None, msg='find_all cannot be called from a %s object' % cls.__name__)
            methods.add(find_all)
        self.assertEqual(len(methods), 1, msg='find_all is defined %d times (instead of once)' % len(methods))

    def _make_patterns(self):
        # Hha, an test (non-overlapping)
        hha = quiz.Sequence([quiz.CharFrom('Hha'), quiz.CharFrom('an')])

        # Date
        month = quiz.Alternatives([
            quiz.Sequence([
                quiz.Verbatim('0'),
                quiz.CharFrom('123456789')
            ]),
            quiz.Sequence([
                quiz.Verbatim('1'),
                quiz.CharFrom('012')
            ]),
        ])
        day = quiz.Alternatives([
            quiz.Sequence([
                quiz.Verbatim('0'),
                quiz.CharFrom('123456789')
            ]),
            quiz.Sequence([
                quiz.CharFrom('12'),
                quiz.CharFrom('0123456789')
            ]),
            quiz.Sequence([
                quiz.CharFrom('3'),
                quiz.CharFrom('01')
            ]),
        ])
        year = quiz.Sequence([
            quiz.Alternatives([
                quiz.Verbatim('19'),
                quiz.Verbatim('20'),
            ]),
            quiz.Repeat(quiz.CharFrom('0123456789'), 2, 2)
        ])
        dash = quiz.Verbatim('-')
        date = quiz.Sequence([
            year, dash, month, dash, day
        ])

        # IP Address
        digits = quiz.Repeat(quiz.CharFrom('0123456789'), 1, 3)
        first = quiz.Repeat(quiz.Sequence([digits, quiz.Verbatim('.')]), 3, 3)
        ip = quiz.Sequence([first, digits])

        # Quoted Text
        quote = quiz.CharFrom('"')
        text = quiz.Star(quiz.CharNotFrom('"'))
        quoted = quiz.Sequence([quote, text, quote])

        # URL
        lowerletters = 'abcdefghijklmnopqrstuvwxyz'
        upperletters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        others = r'%_+~#=-.?&'
        protocol = quiz.Sequence([
            quiz.Alternatives([quiz.Verbatim('http'), quiz.Verbatim('https')]),
            quiz.Verbatim('://'),
        ])
        startchar = quiz.CharFrom(lowerletters+upperletters+digits)
        dot = quiz.Verbatim('.')
        start = quiz.Star(quiz.Sequence([quiz.Star(startchar), dot]))
        tld = quiz.Repeat(quiz.CharFrom(lowerletters), 2, 4)
        pathpiece = quiz.Sequence([quiz.Verbatim('/'),
                                   quiz.Star(quiz.CharFrom(lowerletters+upperletters+digits+others))])
        path = quiz.Star(pathpiece)
        url = quiz.Sequence([protocol, start, tld, path])

        return {'date': date, 'url': url, 'ip': ip, 'quoted': quoted,
                'hha': hha}


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
