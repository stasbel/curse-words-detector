import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def normal_form(word):
    # word = word.decode('utf-8')
    word = word.lower()
    result = morph.parse(word)[0].normal_form
    return result
