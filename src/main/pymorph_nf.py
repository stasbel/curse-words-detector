from pymorphy2 import MorphAnalyzer


class Analyzer:
    def __init__(self, min_accept_score=0.2):
        self.morph = MorphAnalyzer()
        self.min_accept_score = min_accept_score

    def is_in_ruscorpra(self, word):
        return self.morph.word_is_known(word)

    class NormalFormReturnValue(object):
        def __init__(self, candidates):
            self.candidates = candidates

    def normal_form(self, word):
        parse = self.morph.parse(word.lower())
        result = []
        result_set = set()
        for var in parse:
            if (not result) or (var.score > self.min_accept_score and var.normal_form not in result_set):
                result_set.add(var.normal_form)
                result.append(var.normal_form)
        return self.NormalFormReturnValue(result)


if __name__ == '__main__':
    parser = Analyzer()
    name_word = 'вэжэвания'
    print(parser.normal_form(name_word).candidates)
    print(parser.is_in_ruscorpra(name_word))
    for parse_var in parser.morph.parse(name_word):
        print(parse_var)
