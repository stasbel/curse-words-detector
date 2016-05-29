STUPID_ENG_ADN_NUM_TO_RUS = {
    # ONE-LETTER
    '@': 'а', '$': 'с',
    '0': 'о', '1': 'и', '2': 'а', '3': 'е', '4': 'ч', '6': 'б', '8': 'в', '9': 'я',
    'a': 'а', 'b': 'б', 'c': 'с', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'ж', 'h': 'х', 'i': 'и',
    'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'р', 'q': 'к', 'r': 'р',
    's': 'с', 't': 'т', 'u': 'н', 'v': 'в', 'w': 'в', 'x': 'х', 'y': 'у', 'z': 'з',
    # TWO-LETTER
    'zh': 'ж', 'ji': 'л', 'ch': 'ч', 'sh': 'ш', 'bi': 'ы', 'io': 'ю', 'ya': 'я',
    # THREE-LETTER
    'sch': 'щ'
}


class Heurister:
    def __init__(self, replace_dict=STUPID_ENG_ADN_NUM_TO_RUS):
        self.replace_dict = replace_dict

    def transform_word(self, text):
        text = text.lower()

        result = []
        i = 0
        n = len(text)

        while i < n:
            if i < n - 2:
                three_letter = text[i: i + 3]
                if three_letter in self.replace_dict:
                    result.append(self.replace_dict[three_letter])
                    i += 3
                    continue

            if i < n - 1:
                two_latter = text[i: i + 2]
                if two_latter in self.replace_dict:
                    result.append(self.replace_dict[two_latter])
                    i += 2
                    continue

            if text[i] in self.replace_dict:
                result.append(self.replace_dict[text[i]])
                i += 1
                continue

            result.append(text[i])
            i += 1

        return ''.join(result)


if __name__ == '__main__':
    heurister = Heurister()
    print(heurister.transform_word('XJIE6'))
