MORE_INTERESTING_CHARS = {'@', '$'}


class Tokenizer:
    def __init__(self, more_interesting_chars=MORE_INTERESTING_CHARS):
        self.more_interesting_chars = more_interesting_chars

    def is_interesting(self, char):
        return str.isalnum(char) or (char in self.more_interesting_chars)

    def tokenize_text(self, text):
        result = []
        i = 0
        n = len(text)

        while i < n:
            j = i

            if self.is_interesting(text[i]):
                is_word = True
                while j < n and self.is_interesting(text[j]):
                    j += 1
            else:
                is_word = False
                while j < n and not self.is_interesting(text[j]):
                    j += 1
            result.append((text[i:j], is_word))

            i = j

        return result


if __name__ == '__main__':
    tokenizer = Tokenizer()
    print(tokenizer.tokenize_text('Р@CCE9!!ASd123,2ё2б#'))
