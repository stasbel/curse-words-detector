import fnmatch
import os
import unittest
from time import time

from src.main.purifier import Purifier


class Tester(unittest.TestCase):
    pass


def test_generator(correct, suspect, purifier, length_list, time_list):
    def test_this(self):
        self.assertEqual(correct,
                         purifier.purify_text(suspect, length_list, time_list))

    return test_this


"""def __init__(self, method_name='runTest', correct=None, suspect=None, file_name='', purifier=None):
        super(Tester, self).__init__(method_name)

        self.correct = correct
        self.suspect = suspect
        self.file_name = file_name
        self.purifier = purifier

    def runTest(self):
        self.assertEqual(self.correct,
                         self.purifier.purify_text(self.suspect, self.length_list, self.time_list))"""

TEST_DIR = '../resources/tests'
DICT_PATH = '../../../dicts/vanilla_bad_words.txt'


def load_test(loader, tests, pattern):
    test_cases = unittest.TestSuite()
    test_cases.addTest(Tester())
    return test_cases


"""def load_tests(loader, tests, pattern):
    test_cases = unittest.TestSuite()

    purifier = Purifier(DICT_PATH)

    tester = Tester()

    for file_name in os.listdir(TEST_DIR):
        if fnmatch.fnmatch(file_name, 'test[0-9]*.txt'):
            file = open(TEST_DIR + '/' + file_name)
            str1 = file.readline().rstrip()
            str2 = file.readline().rstrip()
            test_name = 'test_' + file_name
            test = test_generator(str1, str2)
            setattr(Tester, test_name, test)

    test_cases.addTest(tester)

    # TODO change file listing
    for file_name in os.listdir(TEST_DIR):
        if fnmatch.fnmatch(file_name, 'test[0-9]*.txt'):  # fix this to avoid some unnecessary tests
            file = open(TEST_DIR + '/' + file_name)
            str1 = file.readline().rstrip()
            str2 = file.readline().rstrip()
            test_cases.addTest(Tester(correct=str2, suspect=str1, file_name=file_name, purifier=purifier))

    return test_cases"""

if __name__ == '__main__':
    purifier = Purifier(DICT_PATH)
    length_list = []
    time_list = []

    for file_name in os.listdir(TEST_DIR):
        if fnmatch.fnmatch(file_name, 't[0-9].txt'):
            file = open(TEST_DIR + '/' + file_name)
            str1 = file.read()
            str2 = open(TEST_DIR + '/' + file_name.replace('.', 's.')).read()
            test_name = 'test_' + file_name
            test = test_generator(str2, str1, purifier, length_list, time_list)
            test.__name__ = test_name
            setattr(Tester, test.__name__, test)

    before_time = time()

    unittest.main(exit=False)

    now_time = time()

    print(now_time - before_time)
    print(len(time_list) / (now_time - before_time))
