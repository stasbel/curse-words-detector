# coding=utf-8
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def normal_form(word):
    # word = word.lower()
    # word = word.decode('utf-8')
    result = morph.parse(word)[0].normal_form
    return result


if __name__ == '__main__':
    print normal_form(u'блядями')

