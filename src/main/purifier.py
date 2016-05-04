# coding=utf-8
import collections
import re
import time

import main.mystem_nf


# TODO перейти на python3 из-за воен с кодировками

def words(text):
    return text.decode('utf-8').splitlines()


def train(features):
    model = collections.defaultdict(lambda: 0)
    for word in features:
        model[word] += 1
    return model


def edits1(word, alphabet):
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alphabet])  # insertion


class Purifier():
    def __init__(self, path_to_dict=None, normal_form=main.mystem_nf.normal_form):
        self.RUSSIAN_ALPHABET_UTF8 = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.good_words = train(words(file(path_to_dict).read()));
        self.normal_norm = normal_form

    def known_edits2(self, edits1_word, alphabet):
        return set(e2 for e1 in edits1_word for e2 in edits1(e1, alphabet) if e2 in self.good_words)

    def known(self, words_list):
        return set(w for w in words_list if w in self.good_words)

    def correct_obscene(self, word):
        if word in self.good_words:
            return word
        else:
            edits1_word = edits1(word, self.RUSSIAN_ALPHABET_UTF8)
            candidates = self.known(edits1_word) or self.known_edits2(edits1_word, self.RUSSIAN_ALPHABET_UTF8) or [word]
            return max(candidates, key=lambda w: self.good_words[w])

    # TODO new version
    """def correct_obscene2(word):
        if word in good_words:
            return word
        else:
            edits1_word ="""

    def purify_text(self, text, length_list=[], time_list=[]):
        text = text.decode('utf-8')
        for word in re.split('[., ]+', text):
            if (word != None and word != ''):
                prev_time = time.time()
                normal_word = self.normal_norm(word)
                curse_word = self.correct_obscene(normal_word)
                if (self.good_words[curse_word] > 0 and
                        (word == curse_word or word.lower() == curse_word or normal_word == curse_word)):
                    text = text.replace(word, u'*')
                length_list.append(len(word))
                time_list.append(float(time.time() - prev_time))
        return text.encode('utf-8')


if __name__ == '__main__':
    purifier = Purifier('../dicts/vanilla_bad_words.txt')
    print purifier.purify_text('ах ты сука, пизда ёбаная')
