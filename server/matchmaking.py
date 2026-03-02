from player import Player
from match import Match
from datetime import datetime

class Matchmaking:
    def __init__(self):
        self.queue: dict[str, Player] = dict()

    def enter(self, player: Player):
        if player.name in self.queue:
            return
        
        self.queue[player.name] = player

    def _find(self, player: Player) -> Player:
        queued: list[Player] = list(self.queue.values())
        ratings: list[float] = [other.rating for other in queued]
        closest = min(abs(player.rating - rating) for rating in ratings)
        index = ratings.index(closest)
        
        return queued[index]

    def matchup(self) -> Match:
        name: str = next(iter(self.queue))
        one: Player = self.queue[name]

        del name

        two: Player = self._find(one)

        return Match(datetime.now(), one, two)
    
