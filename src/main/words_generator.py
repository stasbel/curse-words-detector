# coding=utf-8
from main.util import *

if __name__ == '__main__':
    vanilla_words = words(file(VANILLA_BAD_WORDS_PATH).read())
    edits1_list = list(edits1(e, RUSSIAN_ALPHABET_UTF8) for e in vanilla_words)
    edits1_words = frozenset().union(*edits1_list)
    file = open(EDITS1_BAD_WORDS_PATH, 'w')
    for word in edits1_words:
        file.write(word.encode('utf-8') + '\n')
    file.close()
