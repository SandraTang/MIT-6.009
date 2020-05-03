#!/usr/bin/env python3
import os
import ast
import quiz
import types
import unittest
import json
import hashlib

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

class TestProblem1(unittest.TestCase):
    def _test_generator(self, inp, expected):
        result = quiz.split_words(inp)
        self.assertIsInstance(result, types.GeneratorType, msg="split_words should be a generator")
        self.assertEqual(set(result), expected)

    def _test_from_file(self, inp, n):
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'words_%02d.py' % n), 'r') as f:
            self._test_generator(inp, ast.literal_eval(f.read()))

    def test_01(self):
        self._test_generator('cake', {('cake', )})
        self._test_generator('iateanicecreamcone', {('i', 'a', 'tea', 'nice', 'cream', 'cone'), ('i', 'ate', 'a', 'nice', 'cream', 'cone'), ('i', 'ate', 'an', 'ice', 'cream', 'cone')})
        self._test_generator('mycatscaneatcarrots', {('my', 'cat', 'scan', 'eat', 'car', 'rots'), ('my', 'cat', 'scan', 'eat', 'carrots'), ('my', 'cats', 'can', 'eat', 'car', 'rots'), ('my', 'cats', 'can', 'eat', 'carrots'), ('my', 'cats', 'cane', 'at', 'car', 'rots'), ('my', 'cats', 'cane', 'at', 'carrots')})

    def test_02(self):
        self._test_from_file('etudeshakewithholdsmansards', 1)

    def test_03(self):
        self._test_from_file('redissolvebeseeminggrandeurs', 2)

    def test_04(self):
        self._test_from_file('ushersbreaknecktreblingnitrified', 3)
        self._test_from_file('antennasflameoutnothingstrackless', 4)
        self._test_from_file('abatersboardingapproveduntanglingcirrus', 5)
        self._test_from_file('challengetissuesgrippesrivuletsodiumparties', 6)

    def test_05(self):
        self._test_from_file('relationsharesabridgetheisticwithinslingshots', 7)
        self._test_from_file('opensospreytipsgiftedmenmiscallingdisarmsuprooted', 8)
        self._test_from_file('earningsbrawnsflusmopingyourselfmillinerybicyclistsadrenal', 9)
        self._test_from_file('unmistakenracefilterintertwinedeepdefrayexaminingherefords', 10)
        self._test_from_file('semaphoresixpaperingquadrantalbulldozingvelocitypolesolider', 11)
        self._test_from_file('erstwhilesophisticsocialeagerlyasparagustryingforearmstipple', 12)
        self._test_from_file('accidentalbailoutenlargebegirtquakerswashroompromotersdroves', 13)
        self._test_from_file('barbadosmistookannoysbotfliesincubationdetachescatnipicicles', 14)
        self._test_from_file('hamsterraceapprovesproconsulzonkedwantshadyhearkenamplifyides', 15)
        self._test_from_file('multilithhikersinstallingsquirelacingswaggeredintendedsyapped', 16)
        self._test_from_file('buntbrainpansbeardeddashikihelenapageboyssolipsistpatchpippedomaha', 17)
        self._test_from_file('rethinkaviditiesspearswrenchcapturedaversionspaddlesmisquotespajamas', 18)
        self._test_from_file('sequinsamericanabilletfrightfultimpanistsavertedivyexactorimmolateddisappointsow', 19)
        self._test_from_file('intervenedsendingtrimmingpreemptingpersuasionbudgemoochingextortionwhelksjoustbikes', 20)
        self._test_from_file('federalsunheardtelephonesaliasdepositimbruingartifactspositivecurrentpluralistsullying', 21)
        self._test_from_file('sportingpackagecheshireyearlyenfiladedstomachingpersistsailshelteringsulkyoleoresinpolio', 22)
        self._test_from_file('activationemigratethiamineinstincttypesetquoteskindliestapproachedparchmentstenonsadherent', 23)
        self._test_from_file('stragglypalladiumraspiestplatoonsferrousdeceitsduffersbeaconssuperhumancorvettesaugmentingtallying', 24)
        self._test_from_file('arcslanderousreptilehotheadedsympathyeulogistichabituatedcorianderbarbarouscoercionpopulaceultimatum', 25)


##################################################
##  Problem 2 Tests
##################################################

class TestProblem2(unittest.TestCase):
    # First example from write-up
    def test_01(self):
        x = quiz.InfiniteList(lambda x: 0)
        self.assertEqual(x[20], 0)
        self.assertEqual(x[200000], 0)
        self.assertEqual(x[-5000000000000000], 0)
        x[7] = 8
        self.assertEqual(x[7], 8)

    # Second example from write-up
    def test_02(self):
        y = quiz.InfiniteList(abs)
        self.assertEqual(y[-20], 20)
        self.assertEqual(y[20], 20)
        y[20] = 8
        self.assertEqual(y[-20], 20)
        self.assertEqual(y[20], 8)

    # NOTE: this function that we use for tests only checks finitely elements of the infinite list 'obj'!
    # We only look up through the length of regular Python list 'ans'.
    # We don't think it will help you at all to try to write code that doesn't actually work properly
    # but manages to pass our tests because we only look so many positions into a list. ;-)
    def assertMatch(self, obj, ans):
        for a, b in zip(iter(obj), iter(ans)):
            self.assertEqual(a, b)

    # We also sometimes use this one, so that you can pass tests even if your __iter__ isn't working yet.
    def assertMatchWithoutIter(self, obj, ans):
        for i, v in enumerate(ans):
            self.assertEqual(obj[i], v)

    # Iteration
    def test_03(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        self.assertMatch(x, [0, 1, 3, 3, 10, 5, 6, 7, 8, 9])

    # Addition
    def test_04(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        y = quiz.InfiniteList(lambda x: 0)
        y[1] = 7
        y[2] = 30

        self.assertMatchWithoutIter(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

    # Addition plus __iter__
    def test_05(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        y = quiz.InfiniteList(lambda x: 0)
        y[1] = 7
        y[2] = 30

        self.assertMatch(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

    # Multiplication
    def test_06(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        self.assertMatchWithoutIter(x * 2, [0, 2, 6, 6, 20, 10, 12, 14, 16, 18])


##################################################
#  Problem 3
##################################################

class TestProblem3(unittest.TestCase):

    @staticmethod
    def load_data(test_num):
        with open('resources/valid_boards_test%s.json' % test_num, 'r') as f:
            data = json.load(f)
        return data

    def board_equivalents(self, board):

        def horizontal_flip(board):
            return board[::-1]

        def vertical_flip(board):
            new_board = [len(board) - 1 - x for x in board]
            return new_board

        def rotate90(board, n):
            rotated_board = [-1]*n
            for col in range(n):
                row = board[col]
                if row == -1: continue
                new_row = n - col - 1
                new_col = row
                rotated_board[new_col] = new_row
            return rotated_board

        def hash_board(board):
            str_board = str(tuple(board)).encode('utf-8')
            hash_fn = hashlib.sha1
            return hash_fn(str_board).hexdigest()

        equivalents = set([hash_board(board)])
        equivalents.add(hash_board(horizontal_flip(board)))
        equivalents.add(hash_board(vertical_flip(board)))
        for i in range(3):
            board = rotate90(board, len(board))
            equivalents.add(hash_board(board))

        return equivalents


    def validate(self, data, k, n, returned):
        if n <= 0 or k <= 0:
            self.assertIsNone(returned,                                             \
                            f"\nSolutions are not possible for k={k} and size={n}." \
                            f"\nYour solution returned: {returned}.")

        expected = []
        for min_k in data[str(n)]:
            if int(min_k) <= k:
                expected.extend(data[str(n)][str(min_k)])

        if returned is None:
            self.assertTrue(len(expected) == 0,                                 \
                            f"\nSolutions are possible for k={k} and size={n}." \
                            f"\nYour solution returned None.")
        else:
            self.assertTrue(isinstance(returned, list),                                      \
                            f"\nYour solution did not return a list for k={k} and size={n}." \
                            f"\nIt returned a object of type: {type(returned)}")

            self.assertTrue(all([isinstance(value, int) or isinstance(value, float) for value in returned]), \
                            f"\nYour solution did not return a list of numbers for k={k} and size={n}."      \
                            f"\nIt returned a list of objects of types: {set([type(value) for value in returned])}")

            self.assertEqual(n, len(returned),                                                   \
                            f"\nYour solution is not the correct length for k={k} and size={n}." \
                            f"\nYour solution is length: {len(returned)}, but the board is of size: {n}.")

            number_of_queens = [x for x in returned if x > -1]
            self.assertLessEqual(len(number_of_queens), k,                                 \
                            f"\nYour solution has too many queens for k={k} and size={n}." \
                            f"\nYour solution placed {len(number_of_queens)} queens, but you must place less than or equal to {k} queens.")

            returned_equivalents = self.board_equivalents(returned)
            self.assertTrue(any([equivalent in expected for equivalent in returned_equivalents]), \
                            f"\nYour solution is not a valid solution for k={k} and size={n}."    \
                            f"\nYour solution returned {returned}, which either has conflicting queens or does not cover every cell.")
    def test_01(self):
        """ The 1x1 board."""
        data = self.load_data('1')
        self.validate(data, 1, 1, quiz.k_queens_coverage(1, 1))

    def test_02(self):
        """ The 2x2 board for k in (1, 2)."""
        data = self.load_data('2')
        n = 2
        for k in range(1, n+1):
            self.validate(data, k, n, quiz.k_queens_coverage(k, n))

    def test_03(self):
        """ The 3x3 board for k in (1, 2, 3)."""
        data = self.load_data('3')
        n = 3
        for k in range(1, n+1):
            self.validate(data, k, n, quiz.k_queens_coverage(k, n))

    def test_04(self):
        """ Medium boards between than 4x4 and 6x6 with k that produce solutions."""
        data = self.load_data('4')
        self.validate(data, 3, 4, quiz.k_queens_coverage(3, 4))
        self.validate(data, 4, 4, quiz.k_queens_coverage(4, 4))

        self.validate(data, 3, 5, quiz.k_queens_coverage(3, 5))
        self.validate(data, 4, 5, quiz.k_queens_coverage(4, 5))
        self.validate(data, 5, 5, quiz.k_queens_coverage(5, 5))

        self.validate(data, 4, 6, quiz.k_queens_coverage(4, 6))
        self.validate(data, 5, 6, quiz.k_queens_coverage(5, 6))
        self.validate(data, 6, 6, quiz.k_queens_coverage(6, 6))

    def test_05(self):
        """ Medium boards between than 4x4 and 6x6 with k that do not produce solutions."""
        data = self.load_data('5')
        self.validate(data, 1, 4, quiz.k_queens_coverage(1, 4))
        self.validate(data, 2, 4, quiz.k_queens_coverage(2, 4))

        self.validate(data, 1, 5, quiz.k_queens_coverage(1, 5))
        self.validate(data, 2, 5, quiz.k_queens_coverage(2, 5))

        self.validate(data, 1, 6, quiz.k_queens_coverage(1, 6))
        self.validate(data, 2, 6, quiz.k_queens_coverage(2, 6))
        self.validate(data, 3, 6, quiz.k_queens_coverage(3, 6))

    def test_06(self):
        """ Large boards greater than 6x6 with small k that produce solutions."""
        data = self.load_data('6-7')
        self.validate(data, 3, 7, quiz.k_queens_coverage(3, 7))
        self.validate(data, 4, 7, quiz.k_queens_coverage(4, 7))
        self.validate(data, 5, 7, quiz.k_queens_coverage(5, 7))
        self.validate(data, 6, 7, quiz.k_queens_coverage(6, 7))

        self.validate(data, 5, 8, quiz.k_queens_coverage(5, 8))
        self.validate(data, 6, 8, quiz.k_queens_coverage(6, 8))

    def test_07(self):
        """ Large boards greater than 6x6 with large k that produce solutions."""
        data = self.load_data('6-7')
        self.validate(data, 7, 7, quiz.k_queens_coverage(7, 7))

        self.validate(data, 7, 8, quiz.k_queens_coverage(7, 8))
        self.validate(data, 8, 8, quiz.k_queens_coverage(8, 8))

    def test_08(self):
        """ Large boards greater than 6x6 with k that do not produce solutions."""
        data = self.load_data('8')
        self.validate(data, 1, 7, quiz.k_queens_coverage(1, 7))
        self.validate(data, 2, 7, quiz.k_queens_coverage(2, 7))

        self.validate(data, 1, 8, quiz.k_queens_coverage(1, 8))
        self.validate(data, 2, 8, quiz.k_queens_coverage(2, 8))
        self.validate(data, 3, 8, quiz.k_queens_coverage(3, 8))
        self.validate(data, 4, 8, quiz.k_queens_coverage(4, 8))

    def test_09(self):
        """ Impossible values of k."""
        data = self.load_data('9')
        for n in range(1, 9):
            self.validate(data, 0, n, quiz.k_queens_coverage(0, n))




if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
