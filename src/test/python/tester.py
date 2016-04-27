# coding=utf-8
import fnmatch
import os

from nose.tools import assert_equal

from main.python.purifier import purify_text

TESTS_DIR_PREFIX = '../resources/tests'

length_list = []
time_list = []


def test_run():
    for file_name in os.listdir('../resources/tests'):
        if fnmatch.fnmatch(file_name, 'test[0-2]*.txt'): # fix this to avoid some unnecessary tests
            yield assert_equals, file_name


def assert_equals(test_name):
    with open(TESTS_DIR_PREFIX + '/' + test_name) as file:
        str1 = file.readline().split('\n')[0]
        str2 = file.readline()
        assert_equal(str2, purify_text(str1, length_list, time_list), "Test name: " + test_name)


if __name__ == '__main__':
    # print normal_form('пизде')
    print purify_text('ах ты сука, пизда ёбаная', length_list, time_list)
