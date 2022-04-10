import math
from collections import defaultdict
from words import wordle_dict


INFORMATION_FILE = 'dictionary_info.py'


def guess_result_id(answer, guess, base=3):
    """ Create an Id number for a guess result, in base 3 by default and in reversed order (for speed) """
    id = 0
    place = 1
    for position, letter in enumerate(guess):
        if letter == answer[position]:
            answer = f'{answer[: position]}.{answer[position + 1 :]}'
            id += 2 * place
        place *= base
    place = 1
    for position, letter in enumerate(guess):
        if answer[position] != '.':
            if letter in answer:
                answer = answer.replace(letter, '-', 1)
                id += place
        place *= base
    return id


def guess_result_list(id, base=3):
    """ Restore natural order and return a list with results (0, 1, 2) for each letter """
    digits = []
    while id:
        digits.append(int(id % base))
        id //= base
    while len(digits) < 5:
        digits.append(0)
    return digits


def calculate_entropy(entry, entry_pool=wordle_dict):
    histogram = defaultdict(int)
    for answer in entry_pool:
        histogram[guess_result_id(answer, entry)] += 1
    probabilities = [histogram[n] / len(entry_pool) for n in histogram]
    return sum(-p * math.log(p, 2) for p in probabilities)


if __name__ == '__main__':
    entropy_dict = dict((entry, calculate_entropy(entry)) for entry in wordle_dict)

    with open(INFORMATION_FILE, 'w') as output_file:
        output_file.write('# This file was generated by score_dictionary.py\n\n')
        output_file.write('dictionary = [\n')
        for entry in sorted(entropy_dict, key=entropy_dict.get, reverse=True):
            output_file.write(f"    '{entry}',\n")
        output_file.write(']\n\n')

        output_file.write('default_entropy = {\n')
        for entry in sorted(entropy_dict, key=entropy_dict.get, reverse=True):
            output_file.write(f"    '{entry}': {entropy_dict[entry]},\n")
        output_file.write('}\n')