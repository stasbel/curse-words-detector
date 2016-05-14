import collections
from time import time

import src.main.pymorph_nf

# TODO как улучшить?
# TODO 1) использовать другую структуру данных
# TODO 2) частота употребления: ераном редко, ебаном чаще

RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUSSIAN_ALPHABET_SET = set(RUSSIAN_ALPHABET)
REPLACES = {  # рядом по клавиауре, похоже пишутся, парные, частые ошибки
    'а': 'увсмпек' + 'оя', 'б': 'ьолдю' + 'пвг', 'в': 'ычсакуц' + 'фбо', 'г': 'нролш' + 'пкч', 'д': 'лшщзжюб' + 'тр',
    'е': 'капрн' + 'эёяои', 'ё': 'эхъ' + 'еоая', 'ж': 'щдюэхз' + 'шч', 'з': 'щджэх' + 'сц', 'и': 'мапрт' + 'еэ',
    'й': 'фыц' + 'иёъ', 'к': 'увапе' + 'гдб', 'л': 'огшщдбь' + 'у', 'м': 'свапи' + 'нйж', 'н': 'епрог' + 'мий',
    'о': 'рнгшльт' + 'ёеаэ', 'п': 'акенрим' + 'б', 'р': 'пенготи' + 'сду', 'с': 'чывам' + 'зж', 'т': 'ипроь' + 'дкг',
    'у': 'цывак' + 'дею', 'ф': 'ячыцй' + 'вшщ', 'х': 'зжэёъ' + 'шч', 'ц': 'йфыву' + 'чшщ', 'ч': 'яфывс' + 'цшщж',
    'ш': 'голдщ' + 'жзчц', 'щ': 'шлджз' + 'чц', 'ъ': 'хэё' + 'ьбы', 'ы': 'йфячвуц' + 'ъьэ', 'ь': 'тролб' + 'ъы',
    'э': 'жзхъё' + 'яыюе', 'ю': 'блдж' + 'еяыэу', 'я': 'фыч' + 'аэе',
}


class Purifier:
    def __init__(self, path_to_dict=None, hide_symbol='*',
                 normal_form=src.main.pymorph_nf.normal_form, is_in_dict=src.main.pymorph_nf.is_in_ruscorpra,
                 alphabet=RUSSIAN_ALPHABET, alphabet_set=RUSSIAN_ALPHABET_SET, replaces=REPLACES, max_word_len=15):

        if not path_to_dict:
            raise AttributeError

        self.bad_words = self.__train__(self.__words__(open(path_to_dict).read()))
        self.hide_string = hide_symbol
        self.normal_form = normal_form
        self.is_in_dict = is_in_dict
        self.alphabet = alphabet
        self.alphabet_set = alphabet_set
        self.replaces = replaces
        self.max_word_len = max_word_len

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
    def __slices__(word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]

    def __edits1__(self, word):
        slices = self.__slices__(word)
        n = len(slices)
        deletes = [slices[i][0] + slices[i + 1][1] for i in range(n - 1)]
        transposes = [slices[i][0] + slices[i][1][1] + slices[i][1][0] + slices[i + 2][1] for i in range(n - 2)]
        # старый вариант с поиском всех
        # replaces = [slices[i][0] + c + slices[i + 1][1] for i in range(n - 1) for c in self.alphabet]
        replaces = [slices[i][0] + c + slices[i + 1][1] for i in range(n - 1)
                    if slices[i][1][0] in self.alphabet_set for c in self.replaces[slices[i][1][0]]]
        inserts = [slices[i][0] + c + slices[i][1] for i in range(n) for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

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

    @staticmethod
    def __tokenize__(text):
        result = []
        i = 0
        n = len(text)
        while i < n:
            j = i

            if str.isalpha(text[i]):
                while j < n and (str.isalpha(text[j]) or str.isdigit(text[j])):
                    j += 1
            else:
                while j < n and not str.isalpha(text[j]):
                    j += 1
            result.append(text[i:j])

            i = j

        return result

    @staticmethod
    def __word_heuristic__(word):
        return word.lower()

    def purify_text(self, text, length_list=None, time_list=None):
        if length_list is None:
            length_list = []
        if time_list is None:
            time_list = []
        tokens = self.__tokenize__(text)
        for ind, word in enumerate(tokens):
            if str.isalpha(word[0]) and len(word) <= self.max_word_len:
                prev_time = time()

                word = self.__word_heuristic__(word)

                if self.__is_surely_obscene__(word):
                    tokens[ind] = self.hide_string
                else:
                    normal = self.normal_form(word)
                    if normal.is_in_dict:
                        for normal_word in normal.candidates:
                            if self.__is_surely_obscene__(normal_word):
                                tokens[ind] = self.hide_string
                                break
                    else:
                        for normal_word in normal.candidates:
                            curse = self.__correct_obscene__(normal_word)
                            if (0 <= curse.edit_dist <= 1) or (curse.edit_dist == 2 and len(normal_word) >= 4):
                                tokens[ind] = self.hide_string
                                break

                length_list.append(len(word))
                this_time = float(time() - prev_time)
                time_list.append(this_time)

                # if this_time >= 0.3:
                #     print(word)

        return ''.join(tokens)


if __name__ == '__main__':
    purifier = Purifier('../../dicts/vanilla_bad_words.txt')
    before_time = time()
    print(purifier.purify_text('??ах, ты че, совсем ахуела,рмазь? прасто писдец,мда!!@ ебануться, ебожить с ноги))'))
    now_time = time()
    print(now_time - before_time)
