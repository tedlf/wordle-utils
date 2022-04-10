from dictionary_info import dictionary

BOLD = '\033[1m'
END = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

SQUARED_LETTERS = {
    'a': BOLD + "\N{Squared Latin Capital Letter A}" + END,
    'b': BOLD + "\N{Squared Latin Capital Letter B}" + END,
    'c': BOLD + "\N{Squared Latin Capital Letter C}" + END,
    'd': BOLD + "\N{Squared Latin Capital Letter D}" + END,
    'e': BOLD + "\N{Squared Latin Capital Letter E}" + END,
    'f': BOLD + "\N{Squared Latin Capital Letter F}" + END,
    'g': BOLD + "\N{Squared Latin Capital Letter G}" + END,
    'h': BOLD + "\N{Squared Latin Capital Letter H}" + END,
    'i': BOLD + "\N{Squared Latin Capital Letter I}" + END,
    'j': BOLD + "\N{Squared Latin Capital Letter J}" + END,
    'k': BOLD + "\N{Squared Latin Capital Letter K}" + END,
    'l': BOLD + "\N{Squared Latin Capital Letter L}" + END,
    'm': BOLD + "\N{Squared Latin Capital Letter M}" + END,
    'n': BOLD + "\N{Squared Latin Capital Letter N}" + END,
    'o': BOLD + "\N{Squared Latin Capital Letter O}" + END,
    'p': BOLD + "\N{Squared Latin Capital Letter P}" + END,
    'q': BOLD + "\N{Squared Latin Capital Letter Q}" + END,
    'r': BOLD + "\N{Squared Latin Capital Letter R}" + END,
    's': BOLD + "\N{Squared Latin Capital Letter S}" + END,
    't': BOLD + "\N{Squared Latin Capital Letter T}" + END,
    'u': BOLD + "\N{Squared Latin Capital Letter U}" + END,
    'v': BOLD + "\N{Squared Latin Capital Letter V}" + END,
    'w': BOLD + "\N{Squared Latin Capital Letter W}" + END,
    'x': BOLD + "\N{Squared Latin Capital Letter X}" + END,
    'y': BOLD + "\N{Squared Latin Capital Letter Y}" + END,
    'z': BOLD + "\N{Squared Latin Capital Letter Z}" + END,
}


class GuessResult:
    def __init__(self, **kwargs):
        self.green_letters = {}
        self.yellow_letters = {}
        self.gray_letters = set()
        self.entry = None
        self.result_str = None
        self.unicode_result_str = None

        if 'result_str' in kwargs:
            self.result_str = kwargs['result_str']
            if ',' in self.result_str:
                self.entry, letter_types = self.result_str.split(',')
                while len(letter_types) < 5:
                    letter_types += '-'
                for i, (letter, letter_type) in enumerate(zip(self.entry, letter_types)):
                    if letter_type == '2':
                        self.green_letters[i] = letter
                    elif letter_type == '1':
                        self.yellow_letters[i] = letter
                    else:
                        self.gray_letters.add(letter)
            else:
                self.entry = self.result_str
                self.gray_letters = set(self.entry)
            assert self.entry in dictionary, f'ERROR: {self.entry} is not in the dictionary'
        elif 'answer' in kwargs and 'guess' in kwargs:
            answer = kwargs['answer']
            self.entry = kwargs['guess']
            assert answer in dictionary, f'ERROR: {answer} is not in the dictionary'
            assert self.entry in dictionary, f'ERROR: {self.entry} is not in the dictionary'
            answer = list(answer)
            for position, letter in enumerate(self.entry):
                if answer[position] == letter:
                    self.green_letters[position] = letter
                    answer[position] = None
            for position, letter in enumerate(self.entry):
                if position in self.green_letters:
                    continue
                if letter in answer:
                    self.yellow_letters[position] = letter
                    answer[answer.index(letter)] = None
                else:
                    self.gray_letters.add(letter)

    def is_possible(self, guess):
        guess = list(guess)
        for position in self.green_letters:
            if guess[position] != self.green_letters[position]:
                return False
            else:
                guess[position] = None
        for position in self.yellow_letters:
            letter = self.yellow_letters[position]
            if letter not in guess or guess[position] == letter:
                return False
            else:
                guess[guess.index(letter)] = None
        if self.gray_letters & set(guess):
            return False
        return True

    def is_solution(self):
        return len(self.green_letters) == 5

    def __str__(self):
        if self.unicode_result_str is None:
            output_letters = []
            for position, letter in enumerate(self.entry):
                if position in self.green_letters:
                    output_letters.append(GREEN + SQUARED_LETTERS[letter])
                elif position in self.yellow_letters:
                    output_letters.append(YELLOW + SQUARED_LETTERS[letter])
                else:
                    output_letters.append(SQUARED_LETTERS[letter])
            self.unicode_result_str = ' '.join(output_letters)
        return self.unicode_result_str

    def __repr__(self):
        if self.result_str is None:
            letter_types = list('-----')
            for position in self.green_letters:
                letter_types[position] = '2'
            for position in self.yellow_letters:
                letter_types[position] = '1'
            self.result_str = ','.join((self.entry, ''.join(letter_types)))
        return self.result_str
