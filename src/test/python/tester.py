# coding=utf-8
import os
import fnmatch

import unittest
from main.purifier import purify_text

# TODO сделать не глоальными
length_list = []
time_list = []


# TODO change args names
class Tester(unittest.TestCase):
    def __init__(self, method_name='runTest', correct=None, suspect=None, file_name=''):
        super(Tester, self).__init__(method_name)

        self.correct = correct
        self.suspect = suspect
        self.file_name = file_name

    def runTest(self):
        # TODO строка должна печатьться по-русски
        self.assertEqual(self.correct, purify_text(self.suspect, length_list, time_list))


TEST_DIR = '../resources/tests'
SEPARATOR = '/'
TEST_FILE_PATTERN = 'test[0-9]*.txt'


def load_tests(loader, tests, pattern):
    test_cases = unittest.TestSuite()

    # TODO change file listing
    for file_name in os.listdir(TEST_DIR):
        if fnmatch.fnmatch(file_name, TEST_FILE_PATTERN):  # fix this to avoid some unnecessary tests
            file = open(TEST_DIR + SEPARATOR + file_name)
            str1 = file.readline().rstrip()
            str2 = file.readline().rstrip()
            test_cases.addTest(Tester(correct=str2, suspect=str1, file_name=file_name))

    return test_cases


if __name__ == '__main__':
    unittest.main(exit=False)