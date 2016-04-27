# coding=utf-8
import subprocess
import re


def normal_form(word):
    # word = word.decode('utf-8')
    word = word.lower()
    result = subprocess.check_output('echo ' + word + ' | ../../main/python/mystem -nld', shell=True)
    result = re.split('[?|]+', result)[0]
    return result


if __name__ == '__main__':
    print normal_form('програме')
