from player import Player

class Players:
    def __init__(self):
        self.players: dict[str, Player]

    def get(self, name: str) -> Player:
        if name not in self.players:
            self.players[name] = Player(name)

        return self.players[name]