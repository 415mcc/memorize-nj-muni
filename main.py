import readline
from nj import counties, municipalities
from random import randrange


class Completer:
    def __init__(self, strings):
        self.strings = strings
        self.prefix = None

    def __call__(self, text, state):
        if text != self.prefix:
            self.prefix = text
            matches = [x for x in self.strings if x.startswith(text)]
            if len(matches) == 0:
                return None
            if len(matches) == 1:
                return matches[0]
            return Completer.shared_prefix(matches)
        return None

    @staticmethod
    def shared_prefix(words):
        prefix = []
        for i in zip(*words):
            if not Completer.all_equal(i):
                return ''.join(prefix)
            prefix.append(i[0])

    @staticmethod
    def all_equal(x):
        # yes, I am checking the first element for equality against itself
        # it's more time efficient than x[1:] or range(1, len(x))
        first = x[0]
        for i in x:
            if i != first:
                return False
        return True


class ScoreKeeper:
    def __init__(self):
        self.total = 0
        self.correct = 0

    def add_correct(self):
        self.total += 1
        self.correct += 1

    def add_incorrect(self):
        self.total += 1

    def percent(self):
        if self.total == 0:
            return 100
        else:
            return self.correct / self.total * 100

    def __str__(self):
        return ('You got {} municipalities correct out of {}. {:.2f}%'
                .format(self.correct, self.total, self.percent()))


class Instructor:
    def __init__(self):
        self.incorrects = {}

    def add(self, muni, county):
        s = self.incorrects.get(county)
        if s is None:
            s = set()
            self.incorrects[county] = s
        s.add(muni)

    def __str__(self):
        if len(self.incorrects) == 0:
            return 'No incorrect answers to remember for next time.'
        s = 'Remember these for next time:'
        for county, muniset in sorted(self.incorrects.items(), key=lambda x: x[0]):
            s += '\n  ' + county + ':'
            for muni in sorted(muniset):
                s += '\n    - ' + muni
        return s


def rand_muni():
    return municipalities[randrange(0, len(municipalities))]


def present_muni(score, instructor, muni, county):
    answer = input(muni + ': ')
    if answer == county:
        score.add_correct()
    else:
        score.add_incorrect()
        instructor.add(muni, county)
        print(add_prefix('Incorrect. {} is in {} County.'
                         .format(muni, county)))


def add_prefix(string):
    return '\n'.join(('>>> ' + x for x in string.split('\n')))


def main():
    readline.parse_and_bind('tab: complete')
    readline.set_completer(Completer(counties))
    # Cape May has a space in it so default must be changed
    readline.set_completer_delims('\n')
    print(add_prefix('Exit with ^C'))
    print(add_prefix('Municipalities that share names will be presented with '
                     'a number denoting\nits place in order from north to '
                     'south among the identically named\nmunicipalities. The '
                     'following are shared names: Fairfield Township,\n'
                     'Franklin Township, Greenwich Township, Hamilton '
                     'Township, Hopewell\nTownship, Lawrence Township, '
                     'Mansfield Township, Monroe Township, Ocean\nTownship, '
                     'Springfield Township, Union Township, Washington '
                     'Township. When\nnecessary northern-most points are '
                     'compared.'))
    score = ScoreKeeper()
    instructor = Instructor()
    try:
        while True:
            present_muni(score, instructor, *rand_muni())
    except KeyboardInterrupt:
        pass
    finally:
        print('\n' + add_prefix(str(instructor)))
        print(add_prefix(str(score)))


if __name__ == '__main__':
    main()
