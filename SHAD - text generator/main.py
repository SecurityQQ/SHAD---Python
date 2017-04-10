# parser = argparse.ArgumentParser()
#     parser.add_argument('mode', choices=['sort', 'random'],
#                         help='Mode for words shuffling.')
#     parser.add_argument('filename', help='File to work with.')
#
#     args = parser.parse_args()
#
#     with codecs.open(args.filename, encoding='utf-8') as input_file:
#         base_text = input_file.read()
#
#     print shuffle_letters(base_text, args.mode).encode('utf-8')
#
import string
from collections import Counter, defaultdict

class Utils(object):

    @staticmethod
    def split_symbol(text, symbol, drop_symbol=False):
        if drop_symbol:
            return text.split(symbol)

        parts = text.split(symbol)
        result = []
        for part in parts:
            result += [part, symbol]
        return result[:-1]

    @staticmethod
    def parts_split_symbol(parts, symbol, drop_symbol=False):
        new_parts = []
        for part in parts:
            new_parts += Utils.split_symbol(part, symbol, drop_symbol)
        return [*filter(lambda x: len(x) != 0, new_parts)]

    @staticmethod
    def split(text, delimiters, delimiters_to_drop=[]):
        """

        :param text: type(str)
        :param delimiters: to split text
        :param delimiters_to_drop: to split text and not include to result
        :return: splitted text with delimiters and w/o delimiters_to_drop
        """
        parts = [text]

        for symbol in delimiters_to_drop:
            parts = Utils.parts_split_symbol(parts, symbol, drop_symbol=True)

        for symbol in delimiters:
            parts = Utils.parts_split_symbol(parts, symbol, drop_symbol=False)

        return parts

    @staticmethod
    def tokenize(text, depth=1, drop_whitespace=False):
        """

        :param text: type(str)
        :param depth: length of words chain
        :param drop_whitespace: if true, drops whitespaces in final list
        :return: list of tokens
        """
        delimiters = []
        delimiters_to_drop = []
        if drop_whitespace:
            delimiters = string.punctuation
            delimiters_to_drop = string.whitespace
        else:
            delimiters = string.punctuation + string.whitespace

        splited = Utils.split(text, delimiters, delimiters_to_drop)
        return [tuple(splited[i:i + depth]) for i in range(0, len(splited) - depth + 1)]

    @staticmethod
    def get_chains(text, depth=1):
        chains_with_future = Utils.tokenize(text, depth + 1, drop_whitespace=True)
        chains = dict()
        for item in chains_with_future:
            if item[:depth] not in chains:
                chains[item[:depth]] = []
            chains[item[:depth]] += item[depth:]
        return chains

    @staticmethod
    def count_probabilities(chains):
        probabilities = dict()
        for key, values in chains.items():
            counts = Counter(values)
            total = len(values)
            next_words = []
            for v in values:
                next_words += [(v, counts[v] / total)]
            probabilities[key] = Utils.unique(next_words)
        return probabilities

    @staticmethod
    def unique(l):
        """
        :param l:
        :return: unique elements of list
        """
        return list(set(l))

class TokenizeTask(object):
    def __init__(self, text):
        self.text = text
        self.tokens = Utils.tokenize(self.text)

    def __str__(self):
       return '\n'.join([s[0] for s in self.tokens])


class CalculateProbabilitiesTask(object):
    def __init__(self, text, depth=1):
        self.text = text.replace('\n', '')
        self.chains = [Utils.get_chains(text, depth=i) for i in range(0, depth + 1)]
        self.probabilities = [list(Utils.count_probabilities(chain).items()) for chain in self.chains]
        for chain in self.probabilities:
            chain.sort(key=lambda x: x[0])  # sorting by history of chain
            for hist_to_future in chain:
                hist_to_future[1].sort(key=lambda x: x[0])  # sorting by next_word

    # def __str__(self):
    #     retu
    #     for chain in self.probabilities:
    #
    #
    #     ans = []
    #     for token in sorted(Utils.unique(self.tokens)):
    #         ans.append("  {}: {:.2}\n".format(' '.join(token), self.probabilities_per_word[token]))
    #     return ''.join(ans)


s = """First test sentence
       aecond test line test sentence becond"""
# print(TokenizeTask('Hello, shitty world! Hello!'))

# print(Utils.tokenize('Hello, shitty world! Hello!', 3, drop_whitespace=True)) #, 1, drop_whitespace=False))

# print(CalculateProbabilitiesTask(s, depth=1))

# print(Utils.get_chains(s, depth=0))
from pprint import pprint
pr = CalculateProbabilitiesTask(s, depth=3).probabilities
ans = []
for depth in range(len(pr)):

    # print(pr[depth])
    # for chain in self.probabilities:
    #     chain.sort(key=lambda x: x[0])  # sorting by history of chain
    #     for hist_to_future in chain:
    #         hist_to_future[1].sort(key=lambda x: x[0])  # sorting by next_word

    for hist_to_future in pr[depth]:
        # print(hist_to_future)
        history, future = hist_to_future
        if len(history) != 0:  # we don't want extra \n in beginning
            ans.append(' '.join(history))
        for next_word, p in future:
            ans.append('  {}: {:0.2}'.format(next_word, p))

print('\n'.join(ans))