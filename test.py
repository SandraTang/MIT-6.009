#!/usr/bin/env python3
import json
import os
import pickle
import quiz
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
#  Problem 1
##################################################

class TestProblem1(unittest.TestCase):

    def test_01(self):
        """Passes if anything is returned"""
        data = [1]
        result = quiz.get_mode(data)
        self.assertTrue(True) if result else self.assertFalse(True)

    def test_02(self):
        """Single element"""
        data = [1]
        expect = 1
        result = quiz.get_mode(data)
        self.assertEqual(expect, result)

    def test_03(self):
        """Multiple elements, one candidate appearing twice"""
        data = [3, 94, 44, 68, 5, 44]
        expect = 44
        result = quiz.get_mode(data)
        self.assertEqual(expect, result)

    def test_04(self):
        """Multiple elements, two candidates appearing twice"""
        data = [57, 87, 7, 17, 34, 7, 92, 17]
        expect = 17
        result = quiz.get_mode(data)
        self.assertEqual(expect, result)

    def test_05(self):
        """Multiple elements, multiple candidates appearing multiple times"""
        data = [87, 0, 23, 39, 65, 0, 16, 16, 23, 16, 56, 3, 99, 0, 16, 39]
        expect = 16
        result = quiz.get_mode(data)
        self.assertEqual(expect, result)


##################################################
#  Problem 2
##################################################

class TestProblem2(unittest.TestCase):
    def test_01(self):
        """ Tests that None is returned when no words are anagrams of each other """
        N = 2
        result = quiz.find_anagram_groups(["dog", "cat", "tree", "barn"], N)
        self.assertEqual(result, None)
        
    def test_02(self):
        """ Tests that the correct index is returned when the every word is an anagram of each other """
        N = 4
        result = quiz.find_anagram_groups(['leapt', 'palet', 'plate', 'petal', 'pleat'], N)
        self.assertEqual(result, 3)
        
    def test_03(self):
        """ Tests that the correct index is returned when there are several different anagram groups """
        N = 3
        result = quiz.find_anagram_groups(['reset', 'rail', 'rated', 'terse', 'liar', 'tread', 'trade', 'lair', 'resort', 'tared'], N)
        self.assertEqual(result, 6)
        
    def test_04(self):
        """ Tests that the correct index is returned for a small N with many words """
        # Should find that steam and meats are anagrams of each other
        result = quiz.find_anagram_groups(
                ["stem", "movement", "optometry", "steam", "smith", "equal", "zebra", "horse", "cat", "dog", "python", "lisp",
                "official", "MIT", "computers", "roster", "develop", "laptop", "mouse", "water", "fire",
                "earth", "toddler", "vegetarian", "ferocity", "wolf", "branch", "tree", "lake", "river",
                "mountain", "city", "state", "country", "robust", "stereo", "overlay", "plump", "copy", "list", "array",
                "dictionary", "set", "society", "powerful", "fast", "meats", "algorithm", "cup", 
                "pad", "left", "right", "key", "tuple", "resort"], 2)
        self.assertEqual(result, 46)
        
    def test_05(self):
        """ Tests that the correct index is returned for a large N with a very large number of words """
        with open("test_inputs/{}".format("test_problem2_many_words.json")) as input_file:
            words = json.load(input_file)
        result = quiz.find_anagram_groups(words, 8)
        self.assertEqual(result, 61371)


##################################################
#  Problem 3
##################################################

class TestProblem3(unittest.TestCase):

    # Override the long output produced by high verbosity in test cases.
    longMessage = False

    @staticmethod
    def _load_expected_and_results(f_name):
        with open("test_inputs/{}".format(f_name), "rb") as input_file:
            stream = pickle.load(input_file)
            result = quiz.find_duplicates(stream)
        with open("test_outputs/{}".format(f_name), "rb") as output_file:
            expected = set(pickle.load(output_file))
        return expected, result

    @staticmethod
    def _truncated_failure_message(expected, result, max_diff=50):
        # Determine any missing and extra elements and craft the first message
        # from those.
        missing_elements = expected - result
        extra_elements = result - expected
        message = "Result has {0} missing elements and {1} additional elements.".format(len(missing_elements),
                                                                                        len(extra_elements))
        if not missing_elements:
            message = "Result had {0} additional elements.".format(len(extra_elements))
        elif not extra_elements:
            message = "Result had {0} missing elements.".format(len(missing_elements))

        # Create a diff based on the results.
        message += "\nShowing up to {0} differences.\n\n".format(max_diff)
        if missing_elements:
            message += "Missing elements in solution:\n{0}\n".format(set(list(missing_elements)[:max_diff]))
        if extra_elements:
            message += "Additional elements in solution:\n{0}\n".format(set(list(extra_elements)[:max_diff]))

        return message

    def test_01(self):
        """ A simple case of a single duplicate. """
        stream = ["a", "b", "c", "a"]
        result = quiz.find_duplicates(stream)
        expected = {"a"}
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_02(self):
        """ A simple nested case of no duplicates. """
        stream = {"a": "b", "c": ["d", "e"]}
        result = quiz.find_duplicates(stream)
        expected = set()
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_03(self):
        """ A simple nested case of one duplicate. """
        stream = ["a", "b", ("c", "a"), "d"]
        result = quiz.find_duplicates(stream)
        expected = {"a"}
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_04(self):
        """ Another simple case of duplicates. """
        stream = (["one"], {"two", ("three", ("one", ("two",)))})
        result = quiz.find_duplicates(stream)
        expected = {"one", "two"}
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_05(self):
        """ A simple nested case of no duplicates. """
        stream = ["a", "b", ("c", "d"), {("e", "f"): {"g": ["h"]}}]
        result = quiz.find_duplicates(stream)
        expected = set()
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_06(self):
        """ A normal case of nested duplicates """
        stream = ["one", "two", ["three", ("one", {"four": "five", ("two", "one"): ["eight", "five"]})]]
        result = quiz.find_duplicates(stream)
        expected = {"one", "two", "five"}
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_07(self):
        """ A large case where there are no duplicates. """
        f_name = "test_problem3_large_no_duplicates.pkl"
        expected, result = self._load_expected_and_results(f_name)
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_08(self):
        """ A large case where there are many duplicates. """
        f_name = "test_problem3_large_many_duplicates.pkl"
        expected, result = self._load_expected_and_results(f_name)
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_09(self):
        """ A very large case where there are a few duplicates. """
        f_name = "test_problem3_very_large_few_duplicates.pkl"
        expected, result = self._load_expected_and_results(f_name)
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))

    def test_10(self):
        """ A very large case where there are many duplicates. """
        f_name = "test_problem3_very_large_duplicates.pkl"
        expected, result = self._load_expected_and_results(f_name)
        self.assertEqual(expected, result, self._truncated_failure_message(expected, result))


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
