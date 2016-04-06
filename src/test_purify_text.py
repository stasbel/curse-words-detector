# coding=utf-8
import StringIO
import cProfile
import os
import os.path
import pstats
import unittest

import matplotlib.pyplot as plt
import numpy as np
from guppy import hpy

from purifier import purify_text

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


def make_tests():
    for index in range(NUMBER_OF_TESTS):
        with open("./tests/TEST" + str(index)) as file:
            str1 = file.readline()
            str2 = file.readline()
            tests.append((str2, str1))


def test():
    print "TESTS\n"
    unittest.main(exit=False)


pr = cProfile.Profile()


def enable_cpu_profiling():
    pr.enable()


def disable_cpu_profiling_and_print():
    print "\nCPU PROFILING\n"
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()


def heap_profiling():
    print "\nHEAP PROFILING\n"
    print hpy().heap()


def plots():
    plt.figure(0)
    plt.title("Length/time scatter plot of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Time")
    for i in range(len(length_list)):
        plt.scatter(length_list[i], time_list[i], c='yellow')
    # plt.show()
    plt.savefig("length_time_plot.png")

    plt.figure(1)
    plt.title("Length/number hist of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Number")
    plt.hist(length_list, bins=np.arange(0, 15 + 1, 1), color='green')
    plt.savefig("length_number_plot.png")


def average():
    average = np.average(length_list) / np.average(time_list)
    print "\nAVERAGE SPEED: " + str(average) + " symbols per second"


if __name__ == '__main__':
    make_tests()

    enable_cpu_profiling()

    test()

    disable_cpu_profiling_and_print()

    heap_profiling()

    plots()

    average()
