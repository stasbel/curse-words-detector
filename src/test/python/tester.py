import cProfile
import fnmatch
import os
import pstats
import unittest
from time import time

import matplotlib.pyplot as plt
import numpy as np
from pympler import tracker

from src.main.purifier import Purifier


class Tester(unittest.TestCase):
    pass


def test_generator(_correct, _suspect, _purifier):
    def test_this(self):
        self.assertEqual(_correct,
                         _purifier.purify_text(_suspect))

    return test_this


TEST_DIR = '../resources/tests'
DICT_PATH = '../../../dicts/vanilla_bad_words.cyr.lc'
PLOT1_PATH = '../resources/plots/length_time_plot.png'
PLOT2_PATH = '../resources/plots/length_number_plot.png'
STAT_PATH = '../resources/stats/restats'


def load_test():
    test_cases = unittest.TestSuite()
    test_cases.addTest(Tester())
    return test_cases


def set_tests(_purifier):
    for file_name in os.listdir(TEST_DIR):
        if fnmatch.fnmatch(file_name, 't[0-9].txt'):
            file = open(TEST_DIR + '/' + file_name, 'r')
            str1 = file.read()
            str2 = open(TEST_DIR + '/' + file_name.replace('.', 's.'), 'r').read()
            test_name = 'test_' + file_name
            test = test_generator(str2, str1, _purifier)
            test.__name__ = test_name
            setattr(Tester, test.__name__, test)


def plots(_statisticer):
    # main
    plt.figure(0)
    plt.title("Length/time scatter plot of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Time, sec")
    plt.scatter(_statisticer.length_list, _statisticer.time_list, marker='o', c='red', label='word', s=12)

    # y ticks
    max_time = max(_statisticer.time_list)
    step = 0.0001
    plt.yticks([y for y in np.arange(0, max_time + step, step)], fontsize=6)
    plt.gca().set_ylim([0 - step, max_time + step])

    # x ticks
    max_length = max(_statisticer.length_list)
    plt.xticks([x for x in range(1, max_length + 2)])

    # mean line
    plt.plot([x for x in range(1, max_length + 2)], [_statisticer.bad_time] * (max_length + 1),
             c='green', label='fast', linestyle='--')

    # old average line
    # plt.plot(lengths, np.poly1d(np.polyfit(lengths, times, 1))(lengths), linewidth=1.0)

    # average line
    ax, ay = zip(
        *sorted((x, np.mean([y for a, y in zip(_statisticer.length_list, _statisticer.time_list) if x == a]))
                for x in set(_statisticer.length_list)))
    plt.plot(ax, ay, c='blue', label='average')
    average = _statisticer.get_average_speed()
    plt.annotate('average speed: ' + str(average) + ' w/s', xy=(1.5, (ay[0] + ay[1]) / 2), xytext=(1, 0.001),
                 arrowprops=dict(facecolor='blue', shrink=0.05),
                 horizontalalignment='mid', verticalalignment='mid',
                 fontsize=7)

    # legend
    plt.legend(scatterpoints=1, loc="best")

    # save
    plt.savefig(PLOT1_PATH, bbox_inches='tight')

    # length hist
    plt.figure(1)
    plt.title("Length/number hist of purify_text execution")
    plt.xlabel("Length")
    plt.ylabel("Number")
    plt.hist(_statisticer.length_list, bins=np.arange(max_length + 1) - 0.5, color='green')
    plt.xticks([x for x in range(max_length + 1)])
    plt.xlim([0.5, max_length + 0.5])
    plt.savefig(PLOT2_PATH)


def run_with_time_profiling():
    cProfile.run('unittest.main(exit=False)', STAT_PATH)
    stats = pstats.Stats(STAT_PATH)
    stats.sort_stats('cumulative').print_stats(20)
    stats.print_callers(.5, 'purify_text')
    stats.print_callers(.5, 'normal_form')
    stats.print_callers(.5, 'correct_obscene')


def run_with_memory_profiling():
    tr = tracker.SummaryTracker()
    unittest.main(exit=False)
    tr.print_diff()


if __name__ == '__main__':
    # set
    purifier = Purifier(DICT_PATH)
    set_tests(purifier)

    # run
    before_time = time()
    unittest.main(exit=False)
    # run_with_time_profiling()
    # run_with_memory_profiling()
    now_time = time()

    # statistic
    statisticer = purifier.statisticer
    plots(statisticer)
    statisticer.print_full_information()
