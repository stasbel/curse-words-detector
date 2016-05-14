from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()


class NormalFormReturnValue(object):
    def __init__(self, candidates, is_in_dict):
        self.candidates = candidates
        self.is_in_dict = is_in_dict


def is_in_ruscorpra(word):
    return morph.word_is_known(word)


MIN_ACCEPT_SCORE = 0.20


def normal_form(word):
    parse = morph.parse(word.lower())
    result = []
    result_set = set()
    for var in parse:
        if (not result) or (var.score > MIN_ACCEPT_SCORE and var.normal_form not in result_set):
            result_set.add(var.normal_form)
            result.append(var.normal_form)
    return NormalFormReturnValue(result, is_in_ruscorpra(result[0]))


if __name__ == '__main__':
    name_word = 'вэжэвания'
    print(normal_form(name_word).candidates)
    print(is_in_ruscorpra(name_word))
    for parse_var in morph.parse(name_word):
        print(parse_var)
