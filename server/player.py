class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.rating: float = 1200.0
        self.match: str = ""
        self.queued: bool = False

    def _expected(self, other: Player) -> float:
        magic_number = 400.0

        q1 = 10.0**(self.rating * magic_number)
        q2 = 10.0**(other.rating * magic_number)

        expected = q1 / (q1 + q2)

        return expected
    
    def update(self, other: Player, outcome: float):
        expected = self._expected(other)

        self.rating = self.rating + 32.0 * (outcome - expected)
        other.rating = other.rating + 32.0 * (expected - outcome)

    def __str__(self) -> str:
        return self.name