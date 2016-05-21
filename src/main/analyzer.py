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

    @staticmethod
    def __examine_word__(word, result, result_set):
        if word not in result_set:
            result.append(word)
            result_set.add(word)

    def normal_form(self, word):
        parse = self.morph.parse(word)

        result = []
        result_set = set()
        main_normal_form = parse[0].normal_form
        result.append(main_normal_form)
        result_set.add(main_normal_form)

        for var in parse:
            if var.score >= self.min_accept_score:
                self.__examine_word__(var.normal_form, result, result_set)

                # префиксы и суффиксы
                """for method_stack in var.methods_stack:
                    self.__examine_word__(method_stack[1], result, result_set)"""

        return self.NormalFormReturnValue(result)


if __name__ == '__main__':
    analyzer = Analyzer()
    name_word = 'утебя'
    print(analyzer.normal_form(name_word).candidates)
    print(analyzer.is_in_ruscorpra(name_word))
    for parse_var in analyzer.morph.parse(name_word):
        print(parse_var)
