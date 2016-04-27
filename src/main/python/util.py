# coding=utf-8


PREFIX_BAD_WORDS_PATH = '../../main/resources/'
VANILLA_BAD_WORDS_PATH = PREFIX_BAD_WORDS_PATH + 'vanilla_bad_words.txt'
EDITS1_BAD_WORDS_PATH = PREFIX_BAD_WORDS_PATH + 'edits1_bad_words.txt'
RUSSIAN_ALPHABET_UTF8 = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def words(text):
    return text.lower().decode('utf-8').splitlines()


def edits1(word, alphabet):
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alphabet])  # insertion
