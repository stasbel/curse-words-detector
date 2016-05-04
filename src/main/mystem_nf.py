# coding=utf-8
from pymystem3 import Mystem


mystem = Mystem()


def normal_form(word):
    # word = word.lower()
    word = mystem.lemmatize(word)[0]
    return word


if __name__ == '__main__':
    print normal_form('ебожить')
