# coding=utf-8
import collections
import re
import time

import pymorphy2


def words(text):
    return text.lower().decode('utf-8').splitlines()


def train(features):
    model = collections.defaultdict(lambda: 0)
    for word in features:
        model[word] += 1
    return model


good_words = train(words(file('../../main/resources/bad_words.txt').read()))
russian_alphabet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def edits1(word):
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in russian_alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in russian_alphabet])  # insertion


def known_edits2(edits1_word):
    return set(e2 for e1 in edits1_word for e2 in edits1(e1) if e2 in good_words)


def known(words_list):
    return set(w for w in words_list if w in good_words)


def correct(word):
    if word in good_words:
        return word
    else:
        edits1_word = edits1(word)
        candidates = known(edits1_word) or known_edits2(edits1_word) or [word]
        return max(candidates, key=lambda w: good_words[w])


morph = pymorphy2.MorphAnalyzer()


def normal_form(word):
    # word = word.decode('utf-8')
    word = word.lower()
    word = morph.parse(word)[0].normal_form
    return word


def purify_text(text, length_list, time_list):
    text = text.decode('utf-8')
    for word in re.split('[., ]+', text):
        if (word != None and word != u''):
            prev_time = time.time()
            normal_word = normal_form(word)
            curse_word = correct(normal_word)
            # print word + " " + normal_word + " " + curse_word
            if (good_words[curse_word] > 0 and (
                                word == curse_word or word.lower() == curse_word or normal_word == curse_word)):
                text = text.replace(word, u'*')
            length_list.append(len(word))
            time_list.append(float(time.time() - prev_time))
    return text.encode('utf-8')
