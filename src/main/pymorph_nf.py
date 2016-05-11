from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


class NormalFormReturnValue(object):
    def __init__(self, word, is_in_dict):
        self.word = word
        self.is_in_dict = is_in_dict


def is_in_ruscorpra(word):
    return morph.word_is_known(word)


def normal_form(word):
    result = morph.parse(word.lower())[0].normal_form
    return NormalFormReturnValue(result, is_in_ruscorpra(result))


if __name__ == '__main__':
    print(morph.parse('ераном'))
    print(morph.parse('ераном')[0].methods_stack)
