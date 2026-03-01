from match import Match
from players import Players
from os import path

class Matches:
    def __init__(self):
        self.matches: list[Match] = list()
        self.players: Players = Players()

    def add(self, _match: Match):
        self.matches.append(_match)

    def save(self, path: str = path.join(path.dirname(__file__), "matches.txt")):
        for _match in self.matches:
            _match.write(path)

    @staticmethod
    def load(path: str = path.join(path.dirname(__file__), "matches.txt")):
        matches = Matches()

        for line in open(path, "r").readlines():
            _match = Match.deserialize(line, matches.players)
            matches.add(_match)
            _match.apply()

        return matches