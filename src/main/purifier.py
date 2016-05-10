import collections
from time import time

import src.main.pymorph_nf


# TODO как улучшить? 1) использовать другую структуру данных


class Purifier:
    def __init__(self, path_to_dict=None, hide_symbol='*',
                 normal_form=src.main.pymorph_nf.normal_form, is_in_dict=src.main.pymorph_nf.is_in_ruscorpra):
        self.RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.bad_words = self.__train__(self.__words__(open(path_to_dict).read()))
        self.hide_symbol = hide_symbol
        self.normal_form = normal_form
        self.is_in_dict = is_in_dict

    @staticmethod
    def __words__(text):
        return text.splitlines()

    @staticmethod
    def __train__(features):
        model = collections.defaultdict(lambda: 0)
        for word in features:
            model[word] += 1
        return model

    @staticmethod
    def __slices__(word, n):
        return [[word[i:j] if i <= j else None for j in range(n + 1)] for i in range(n + 1)]

    def __edits1__(self, word):
        n = len(word)
        slices = self.__slices__(word, n)
        return set([slices[0][i] + slices[i + 1][n] for i in range(n)] +  # deletion
                   [slices[0][i] + word[i + 1] + word[i] + slices[i + 2][n] for i in range(n - 1)] +  # transposition
                   [slices[0][i] + c + slices[i + 1][n] for i in range(n) for c in
                    self.RUSSIAN_ALPHABET] +  # alteration
                   [slices[0][i] + c + slices[i][n] for i in range(n + 1) for c in self.RUSSIAN_ALPHABET])  # insertion

    def __known_edits2__(self, edits1_word):
        return set(e2 for e1 in edits1_word for e2 in self.__edits1__(e1) if e2 in self.bad_words)

    def __known_bad__(self, words_list):
        return set(w for w in words_list if w in self.bad_words)

    class CorrectObsceneReturnValue(object):
        """
        :param word - curse word
        :param edit_dist - edit distance from word to curse word, [0-2] for
        in normal curse word, -1 for not a curse word
        """

        def __init__(self, word, edit_dist):
            self.word = word
            self.edit_dist = edit_dist

    def __find_bad_max__(self, candidates):
        if candidates:
            return max(candidates, key=lambda w: self.bad_words[w])
        else:
            return None

    def __find_good_any__(self, edits1):
        for good_word in edits1:
            if self.is_in_dict(good_word):
                return good_word
        return None

    def __correct_obscene__(self, word):
        # на расстоянии 1: ищу наилучший мат и любое хорошее слово
        edits1_word = self.__edits1__(word)

        bad_candidates1 = self.__known_bad__(edits1_word)
        bad_candidate1 = self.__find_bad_max__(bad_candidates1)
        if bad_candidate1:
            return self.CorrectObsceneReturnValue(bad_candidate1, 1)

        good_candidate = self.__find_good_any__(edits1_word)
        if good_candidate:
            return self.CorrectObsceneReturnValue(good_candidate, -1)

        else:
            # на расстоянии 2: ищу любой мат и любое хорошее слово
            # или можно опять же искать лучший мат, тогда скорость упадет втрое

            bad_candidates2 = self.__known_edits2__(edits1_word)
            candidate2 = self.__find_bad_max__(bad_candidates2)
            if candidate2:
                return self.CorrectObsceneReturnValue(candidate2, 2)

            """for e1 in edits1_word:
                for e2 in self.__edits1__(e1):
                    if e2 in self.bad_words:
                        print(e2)
                        return self.CorrectObsceneReturnValue(e2, 2)
                    if self.is_in_dict(e2):
                        print(e2)
                        return self.CorrectObsceneReturnValue(e2, -1)"""

            return self.CorrectObsceneReturnValue(word, -1)

    def __is_surely_obscene__(self, word):
        return word in self.bad_words

    def __is_surely_not_obscene__(self, word):
        return word not in self.bad_words

    is_a = lambda c: str.isalpha(c)
    n_is_a = lambda c: not str.isalpha(c)

    @staticmethod
    def __tokenize__(text):
        result = []
        i = 0
        n = len(text)
        while i < n:
            if str.isalpha(text[i]):
                func = Purifier.is_a
            else:
                func = Purifier.n_is_a

            j = i
            while j < n and func(text[j]):
                j += 1
            result.append(text[i:j])
            i = j

        return result

    def purify_text(self, text, length_list=None, time_list=None):
        if length_list is None:
            length_list = []
        if time_list is None:
            time_list = []
        tokens = self.__tokenize__(text)
        for ind, word in enumerate(tokens):
            if str.isalpha(word[0]):
                prev_time = time()

                if self.__is_surely_obscene__(word):
                    tokens[ind] = self.hide_symbol
                else:
                    normal = self.normal_form(word)
                    if normal.is_in_dict:
                        if self.__is_surely_obscene__(normal.word):
                            tokens[ind] = self.hide_symbol
                    else:
                        curse = self.__correct_obscene__(normal.word)
                        if (0 <= curse.edit_dist <= 1) or (curse.edit_dist == 2 and len(normal.word) >= 4):
                            tokens[ind] = self.hide_symbol

                length_list.append(len(word))
                time_list.append(float(time() - prev_time))
        return ''.join(tokens)


if __name__ == '__main__':
    purifier = Purifier('../../dicts/vanilla_bad_words.txt')
    before_time = time()
    print(purifier.purify_text('??ах, ты че, совсем ахуела, рмазь? прасто писдец, мда!!@ ебануться, ебожить с ноги))'))
    # print(purifier.__edits1__('abc'))
    # print(purifier.purify_text('нормальный текст без ошибак'))
    # print(Purifier.__slices__('ебанутьсяься', 12))
    # print(purifier.__correct_obscene__('че').word)
    now_time = time()
    print(now_time - before_time)
