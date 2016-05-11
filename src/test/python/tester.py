import fnmatch
import os
import unittest
from time import time

import matplotlib.pyplot as plt
import numpy as np

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
PLOT_PATH = '../resources/plots'


def load_test(loader, tests, pattern):
    test_cases = unittest.TestSuite()
    test_cases.addTest(Tester())
    return test_cases


def plots(lengths, times):
    plt.figure(0)
    plt.title("Length/time scatter plot of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Time")
    plt.scatter(lengths, times, c='red')

    plt.plot(lengths, np.poly1d(np.polyfit(lengths, times, 1))(lengths))

    # plt.show()
    plt.savefig(PLOT_PATH + '/' + 'length_time_plot.png', bbox_inches='tight')

    """plt.figure(1)
    plt.title("Length/number hist of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Number")
    plt.hist(length_list, bins=np.arange(0, 15 + 1, 1), color='green')
    plt.savefig("../resources/plots/length_number_plot.png")"""


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

    plots(length_list, time_list)

    # print(now_time - before_time)
    # print(len(time_list) / (now_time - before_time))
