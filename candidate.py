class Candidate:
    def __init__(self, entry=None, scores=None):
        self.entry = entry
        self.scores = scores

    def __lt__(self, other):
        return self.scores < other.scores

    def __str__(self):
        return '{}\t{}'.format(self.entry, '\t'.join(str(round(s, 4)) for s in self.scores))
