from time import time

from src.main.pymorph_nf import Analyzer

# TODO как улучшить?
# TODO 1) использовать другую структуру данных (память)
# TODO 2) две вставки это много? (скорость)
# TODO 3) частота употребления: ераном редко, ебаном чаще, можно дать матам частоту и скачать словарь частотности
# TODO совсем редкие слова можно пропускать (точность)
# TODO 4) Mystem? (???)


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
                 bad_time=0.003):
        """
        :param path_to_vanilla: путь с словарю с плохими словами
        :param hide_symbol: на что заменяем плохое слово
        :param is_dict: функция для проверки словарного слова
        :param normal_form: функция для поиска нормальных форм
        :param alphabet: алфавит
        :param replaces: словарь умных замен
        :param bad_time: плохое время для анализа слова
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

        self.bad_time = bad_time

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
            return self.CorrectObsceneReturnValue(self.edits1_dict[word], 1)

        edits1_word = self.__edits1__(word, fast_return_if_dict=True, clever_replaces=True)
        if isinstance(edits1_word, str):  # вернулись досрочно = просто строка
            return self.CorrectObsceneReturnValue(edits1_word, -1)

        for e1 in edits1_word:
            if self.is_edit1(e1):  # тут тоже все ясно
                return self.CorrectObsceneReturnValue(self.edits1_dict[e1], 2)

        return self.CorrectObsceneReturnValue(word, -1)

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

    def purify_text(self, text, length_list=None, time_list=None, bottleneck_list=None):
        if length_list is None:
            length_list = []
        if time_list is None:
            time_list = []
        if bottleneck_list is None:
            bottleneck_list = []

        tokens = self.__tokenize__(text)
        for ind, word in enumerate(tokens):
            if str.isalpha(word[0]):
                prev_time = time()

                word = self.__word_heuristic__(word)

                if self.is_bad(word):  # плохое - баним
                    tokens[ind] = self.hide_string
                else:  # иначе нужны хорошие нормальные формы
                    normal = self.normal_form(word)
                    if self.is_dict(normal.candidates[0]):  # не работает предиктор - слово было в словаре
                        for normal_word in normal.candidates:  # на одинаковой дистанции, маты важнее обыных слов
                            if self.is_bad(normal_word):
                                tokens[ind] = self.hide_string
                                break
                    else:  # изначальное слово и все его хорошие нф не в словаре матов и не в обычном словаре
                        for normal_word in normal.candidates:
                            curse = self.__correct_obscene__(normal_word)
                            if (0 <= curse.edit_dist <= 1) or (curse.edit_dist == 2 and len(normal_word) >= 4):
                                tokens[ind] = self.hide_string
                                break

                this_time = float(time() - prev_time)
                time_list.append(this_time)
                length_list.append(len(word))

                if this_time >= self.bad_time:
                    bottleneck_list.append(word)

        return ''.join(tokens)


if __name__ == '__main__':
    purifier = Purifier('../../dicts/vanilla_bad_words.txt')
    before_time = time()
    print(purifier.purify_text('??ах, ты че, совсем ахуела,рмазь? прасто писдец,мда!!@ ебануться, ебожить с ноги))'))
    # print(purifier.purify_text('ростик шамбарова меня не жэляют это тебя жэлеют тваи видео гавно'))
    # print(purifier.purify_text('В деньгах, блять, в тачке? \nКогда пиздатая мобила? '))
    now_time = time()
    print(now_time - before_time)
