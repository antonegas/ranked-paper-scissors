from uuid import uuid4
from player import Player
from players import Players
from hands import Hand
from datetime import datetime, timedelta
from os import path

class Match:
    def __init__(self, timestamp: datetime, one: Player, two: Player):
        self.match_id: str = str(uuid4())
        self.timestamp: datetime = timestamp
        self.players: list[Player] = [one, two]
        self.hands: list[Hand] = [Hand.NONE, Hand.NONE]
        self.applied: bool = False

    def done(self) -> bool:
        if datetime.now() - self.timestamp > timedelta(seconds=10):
            return True

        return self.hands[0] != Hand.NONE and self.hands[1] != Hand.NONE
    
    def outcome(self) -> float:
        one, two = self.hands

        if one == Hand.NONE and two == Hand.NONE:
            return 0.5
        if one == Hand.NONE:
            return 0.0
        if two == Hand.NONE:
            return 1.0

        if one.value + 1 % 3 == two.value:
            return 0.0
        elif one == two:
            return 0.5
        else:
            return 1.0
        
    def _names(self) -> tuple[str, str]:
        return self.players[0].name, self.players[1].name
        
    def play(self, name: str, hand: Hand):
        if name not in self._names():
            return

        index = self._names().index(name)
        
        if self.hands[index] != Hand.NONE:
            return
        
        self.hands[index] = hand
        
    def apply(self):
        if not self.applied:
            self.applied = True
            self.players[0].update(self.players[1], self.outcome())
        
    def write(self, file_path: str = path.join(path.dirname(__file__), "matches.txt")):
        matches_file = open(file_path, "a")
        matches_file.write(self.__str__() + "\n")
        matches_file.close()

    @staticmethod
    def deserialize(serialized: str, players: Players) -> Match:
        isotimestamp, name_one, name_two, hand_one, hand_two = serialized.split(",")

        deserialized = Match(
            datetime.fromisoformat(isotimestamp),
            players.get(name_one),
            players.get(name_two)
        )

        deserialized.play(name_one, Hand[hand_one])
        deserialized.play(name_two, Hand[hand_two])

        return deserialized

    def __str__(self) -> str:
        return ",".join([
            self.timestamp.isoformat(), 
            str(self.players[0]), 
            str(self.players[1]), 
            str(self.hands[0].name), 
            str(self.hands[1].name)
        ])