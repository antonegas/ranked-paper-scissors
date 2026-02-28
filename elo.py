from collections import defaultdict

def expected_outcome(one: float, two: float) -> float:
    magic_number = 400.0

    q1 = 10.0**(one * magic_number)
    q2 = 10.0**(two * magic_number)

    expected = q1 / (q1 + q2)

    return expected

def update(players: defaultdict[str, float], one: str, two: str, outcome: float):
    expected = expected_outcome(players[one], players[two])

    players[one] = players[one] + 32.0 * (outcome - expected)
    players[two] = players[two] + 32.0 * (expected - outcome)