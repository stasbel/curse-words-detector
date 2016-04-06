# coding=utf-8
import collections
import re
import pymorphy2
import cProfile
import StringIO
import pstats
import time
from guppy import hpy


def words(text): return text.lower().decode('utf-8').splitlines()


def train(features):
    model = collections.defaultdict(lambda: 0)
    for f in features:
        model[f] += 1
    return model


NWORDS = train(words(file('bad_words.txt').read()))
alphabet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def edits1(word):
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alphabet])  # insertion


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words_list): return set(w for w in words_list if w in NWORDS)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=lambda w: NWORDS[w])


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
            # length_list.append(len(word))
            normal_word = normal_form(word)
            curse_word = correct(normal_word)
            # print word + " " + normal_word + " " + curse_word
            if (NWORDS[curse_word] > 0 and (
                                word == curse_word or word.lower() == curse_word or normal_word == curse_word)):
                text = text.replace(word, u'*')
            length_list.append(len(word))
            time_list.append(float(time.time() - prev_time))
    return text.encode('utf-8')


def test_oxxxy():
    pr = cProfile.Profile()
    pr.enable()
    run_oxxxy()
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()


h = hpy()

if __name__ == '__main__':
    print purify_text("h")
    # test_oxxxy()
    # length_list = [0, 1, 2, 2]
    # plt.hist(length_list, bins=[i for i in range(0, 15)])
    # plt.show()
    # print h.heap()
    # ptasd
    # run_oxxxy()
