from time import time

from src.main.analyzer import Analyzer
from src.main.heurister import Heurister
from src.main.tokenizer import Tokenizer
from src.test.python.statisticer import Statisticer

"""
:const RUSSIAN_ALPHABET: русский алфавит
:const REPLACES: умные замены букв: рядом по клавиатуре, похоже пишутся, парные, похоже слышатся, частые ошибки
"""
RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
REPLACES = {
    'а': 'увсмпек' + 'оя', 'б': 'ьолдю' + 'пвг', 'в': 'ычсакуц' + 'фбо', 'г': 'нролш' + 'пкч', 'д': 'лшщзжюб' + 'тр',
    'е': 'капрн' + 'эёяои', 'ё': 'эхъ' + 'еоая', 'ж': 'щдюэхз' + 'шч', 'з': 'щджэх' + 'сц', 'и': 'мапрт' + 'еэ',
    'й': 'фыц' + 'иёъ', 'к': 'увапе' + 'гдб', 'л': 'огшщдбь' + 'у', 'м': 'свапи' + 'нйж', 'н': 'епрог' + 'мий',
    'о': 'рнгшльт' + 'ёеаэ', 'п': 'акенрим' + 'б', 'р': 'пенготи' + 'сду', 'с': 'чывам' + 'зж', 'т': 'ипроь' + 'дкг',
    'у': 'цывак' + 'дею', 'ф': 'ячыцй' + 'вшщ', 'х': 'зжэёъ' + 'шч', 'ц': 'йфыву' + 'чшщ', 'ч': 'яфывс' + 'цшщж',
    'ш': 'голдщ' + 'жзчц', 'щ': 'шлджз' + 'чц', 'ъ': 'хэё' + 'ьбы', 'ы': 'йфячвуц' + 'ъьэ', 'ь': 'тролб' + 'ъы',
    'э': 'жзхъё' + 'яыюе', 'ю': 'блдж' + 'еяыэу', 'я': 'фыч' + 'аэе',
}


class Purifier:
    @staticmethod
    def __words__(raw_text):
        return raw_text.splitlines()

    def __make_edits1_dict__(self):
        result = dict()
        for bad_word in self.bad_words:
            for e1 in self.__edits1__(bad_word, clever_replaces=True):
                result[e1] = bad_word
        return result

    def __train__(self, features):
        self.max_bad_length = 0
        for word in features:
            self.max_bad_length = max(self.max_bad_length, len(word))
        return set(features)

    def __init__(self, path_to_vanilla=None, hide_symbol='*',
                 is_dict=None, normal_form=None,
                 alphabet=RUSSIAN_ALPHABET, replaces=REPLACES,
                 statisticer=Statisticer(),
                 tokenizer=Tokenizer(),
                 heurister=Heurister()):
        """
        :param path_to_vanilla: путь с словарю с плохими словами
        :param hide_symbol: на что заменяем плохое слово
        :param is_dict: функция для проверки словарного слова
        :param normal_form: функция для поиска нормальных форм
        :param alphabet: алфавит
        :param replaces: словарь умных замен
        :param statisticer: класс для сбора статистики
        :param tokenizer: класс для разбиения на слова и не слова
        :param heurister: эвристическая замена не русских букв и больших на маленькие
        :return: новый класс
        """

        self.alphabet = alphabet
        self.alphabet_set = set(self.alphabet)
        self.replaces = replaces

        if not path_to_vanilla:
            raise AttributeError
        self.bad_words = self.__train__(self.__words__(open(path_to_vanilla).read()))
        self.is_bad = lambda w: w in self.bad_words

        self.edits1_dict = self.__make_edits1_dict__()
        self.is_edit1 = lambda w: w in self.edits1_dict

        self.hide_string = hide_symbol

        if (not is_dict) or (not normal_form):
            analyzer = Analyzer()

            if not is_dict:
                self.is_dict = analyzer.is_in_ruscorpra

            if not normal_form:
                self.normal_form = analyzer.normal_form

        self.statisticer = statisticer

        self.tokenizer = tokenizer

        self.heurister = heurister

        self.processed = dict()

    @staticmethod
    def __slices__(word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]

    def __edits1__(self, word, include_inserts=True, fast_return_if_dict=False, clever_replaces=False):
        """
        :param word: изначальное слово
        :param include_inserts: надо ли генерить вставки пропущенной буквы
        :param fast_return_if_dict: надо ли быстро возвращать словарное слово
        :param clever_replaces: надо ли использовать умные замены
        :return: множество слов с расстоянием 1 до изначального
        """

        slices = self.__slices__(word)
        n = len(slices)

        result = set()

        # deletes
        for i in range(n - 1):
            new_word = slices[i][0] + slices[i + 1][1]
            if fast_return_if_dict and self.is_dict(new_word):
                return new_word
            result.add(new_word)

        # transposes
        for i in range(n - 2):
            new_word = slices[i][0] + slices[i][1][1] + slices[i][1][0] + slices[i + 2][1]
            if fast_return_if_dict and self.is_dict(new_word):
                return new_word
            result.add(new_word)

        # replaces
        if clever_replaces:
            def replace_list(char):
                return self.replaces[char]
        else:
            def replace_list(*_):
                return self.alphabet
        for i in range(n - 1):
            if slices[i][1][0] in self.alphabet_set:
                for c in replace_list(slices[i][1][0]):
                    new_word = slices[i][0] + c + slices[i + 1][1]
                    if fast_return_if_dict and self.is_dict(new_word):
                        return new_word
                    result.add(new_word)

        # inserts
        if include_inserts:
            for i in range(n - 1):
                for c in self.alphabet:
                    new_word = slices[i][0] + c + slices[i][1]
                    if fast_return_if_dict and self.is_dict(new_word):
                        return new_word
                    result.add(new_word)

        return result

    class CorrectObsceneReturnValue(object):
        def __init__(self, word, edit_dist):
            """
            :param word: найденное плохое слово
            :param edit_dist: расстояние от изначального до плохого слова или -1 если не нашли такого
            :return: новый класс
            """
            self.word = word
            self.edit_dist = edit_dist

    def __correct_obscene__(self, word):
        if len(word) > self.max_bad_length + 2:  # слишком большая длина
            return self.CorrectObsceneReturnValue(word, -1)

        if self.is_edit1(word):  # тут все понятно
            self.statisticer.edit1_list.append(word)
            return self.CorrectObsceneReturnValue(self.edits1_dict[word], 1)

        edits1_word = self.__edits1__(word, fast_return_if_dict=True, clever_replaces=True)
        if isinstance(edits1_word, str):  # вернулись досрочно = просто строка
            self.statisticer.edit1_list.append(word)
            return self.CorrectObsceneReturnValue(edits1_word, -1)

        self.statisticer.edit2_list.append(word)

        for e1 in edits1_word:
            if self.is_edit1(e1):  # тут тоже все ясно
                return self.CorrectObsceneReturnValue(self.edits1_dict[e1], 2)

        return self.CorrectObsceneReturnValue(word, -1)

    def __is_obscene__(self, raw_word):
        result = False

        # запоминаем начальное время
        prev_time = time()

        if raw_word in self.processed:  # если уже обрабатывали, что ок
            result = self.processed[raw_word]
        else:
            # приводим к нижнему регистру, заменяем английские буквы и цифры на русские
            word = self.heurister.transform_word(raw_word)

            if self.is_bad(word):  # плохое - баним
                result = True
            else:  # иначе нужны хорошие нормальные формы
                normal = self.normal_form(word)
                if self.is_dict(normal.candidates[0]):  # не работает предиктор - слово было в словаре
                    for normal_word in normal.candidates:  # на одинаковой дистанции, маты важнее обыных слов
                        if self.is_bad(normal_word):
                            result = True
                            break
                else:  # изначальное слово и все его хорошие нф не в словаре матов и не в обычном словаре
                    for normal_word in normal.candidates:
                        curse = self.__correct_obscene__(normal_word)
                        if (0 <= curse.edit_dist <= 1) or (curse.edit_dist == 2 and len(normal_word) >= 4):
                            result = True
                            break

            self.processed[raw_word] = result
            self.processed[word] = result

        # статистика
        this_time = float(time() - prev_time)
        self.statisticer.time_list.append(this_time)
        self.statisticer.length_list.append(len(raw_word))
        self.statisticer.count += 1
        if result:
            self.statisticer.bad_count += 1
        if this_time > self.statisticer.bad_time:
            self.statisticer.bottleneck_list.append(raw_word)

        return result

    def purify_text(self, text):
        # TODO утебя = у тебя или = ут!!!ЕБЯ!!! => slicer

        tokens = self.tokenizer.tokenize_text(text)

        for ind, (token, is_word) in enumerate(tokens):
            if is_word:
                tokens[ind] = self.hide_string if self.__is_obscene__(token) else token
            else:
                tokens[ind] = token

        return ''.join(tokens)


if __name__ == '__main__':
    purifier = Purifier('../../dicts/vanilla_bad_words.txt')
    before_time = time()
    print(purifier.purify_text('??ах, ты че, совсем ахуела,рм@зь? прасто писдец,мда!!@ 3бануться, ебожить с ноги))'))
    now_time = time()
    print(now_time - before_time)
