# coding=utf-8
import unittest
from purifier import purify_text
import matplotlib.pyplot as plt
import os
import os.path
import cProfile
import StringIO
import pstats
import numpy as np
from guppy import hpy

path, dirs, files = os.walk("./tests").next()
NUMBER_OF_TESTS = len(files)
tests = []

SCALE = 100
length_list = []
time_list = []


class TestPurifyText(unittest.TestCase):
    def check(self, purified, original):
        self.assertEqual(purified + "\n", purify_text(original, length_list, time_list))

    def test(self):
        for (purified, original) in tests:
            self.check(purified, original)

    pass


if __name__ == '__main__':
    for index in range(NUMBER_OF_TESTS):
        with open("./tests/TEST" + str(index)) as file:
            str1 = file.readline()
            str2 = file.readline()
            tests.append((str2, str1))

    pr = cProfile.Profile()
    pr.enable()

    print "TESTS\n"

    unittest.main(exit=False)

    print "\nCPU PROFILING\n"

    pr.disable()
    s = StringIO.StringIO()
    sort_by = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
    ps.print_stats()
    print s.getvalue()

    print "\nHEAP PROFILING\n"

    print hpy().heap()

    plt.title("Length/time scatter plot of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Time")
    for index in range(len(length_list)):
        plt.scatter(length_list[index], time_list[index], c='yellow')
    # plt.show()
    plt.savefig("correlation.png")

    average = np.average(length_list) / np.average(time_list)
    print "\nAVERAGE SPEED: " + str(average) + " symbols per second"
