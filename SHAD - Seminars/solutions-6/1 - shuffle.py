import argparse
import codecs
import random
import string


SPLIT_SYMBOLS = string.whitespace + string.punctuation


def split_symbol(text, symbol):
    parts = text.split(symbol)
    result = []
    for part in parts:
        result += [part, symbol]
    return result[:-1]


def parts_split_symbol(parts, symbol):
    new_parts = []
    for part in parts:
        new_parts += split_symbol(part, symbol)
    return new_parts


def shuffle_letters(text, mode):
    parts = [text]
    for symbol in SPLIT_SYMBOLS:
        parts = parts_split_symbol(parts, symbol)

    shuffled_parts = []
    for part in parts:
        if part in SPLIT_SYMBOLS or len(part) <= 2:
            shuffled_parts.append(part)
            continue

        internal_part = part[1:-1]
        if mode == 'random':
            internal_part_symbols = list(internal_part)
            random.shuffle(internal_part_symbols)
            internal_part_shuffled = ''.join(internal_part_symbols)
        elif mode == 'sort':
            internal_part_shuffled = ''.join(sorted(internal_part))

        part_shuffled = part[0] + internal_part_shuffled + part[-1]
        shuffled_parts.append(part_shuffled)

    return ''.join(shuffled_parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['sort', 'random'],
                        help='Mode for words shuffling.')
    parser.add_argument('filename', help='File to work with.')

    args = parser.parse_args()

    with codecs.open(args.filename, encoding='utf-8') as input_file:
        base_text = input_file.read()

    print shuffle_letters(base_text, args.mode).encode('utf-8')


if __name__ == '__main__':
    main()
