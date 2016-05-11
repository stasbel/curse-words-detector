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


TEST_DIR = '../resources/tests'
DICT_PATH = '../../../dicts/vanilla_bad_words.txt'


def load_test(loader, tests, pattern):
    test_cases = unittest.TestSuite()
    test_cases.addTest(Tester())
    return test_cases


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
