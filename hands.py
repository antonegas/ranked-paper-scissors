from enum import Enum

Hand = Enum("Hand", [("ROCK", 0), ("PAPER", 1), ("SCISSORS", 2), ("NONE", 4)])

def beats(one: Hand, two: Hand) -> float:
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
    