from os import path
from collections import defaultdict
from datetime import datetime
from hands import Hand, beats
from elo import update

def serialize_match(timestamp: datetime, one: str, two: str, hand_one: Hand, hand_two: Hand):
    matches_file = open(path.join(path.dirname(__file__), "matches.txt"), "a")
    matches_file.write(",".join([timestamp.isoformat(), one, two, str(hand_one.value), str(hand_two.value)]) + "\n")
    matches_file.close()

def deserialize_match(serialized_match: str) -> tuple[datetime, str, str, Hand, Hand]:
    timestamp_string, one, two, a, b = serialized_match.split(",")
    
    timestamp = datetime.fromisoformat(timestamp_string)
    hand_one = Hand(int(a))
    hand_two = Hand(int(b))

    return timestamp, one, two, hand_one, hand_two

def deserialize_matches(players: defaultdict[str, float]):
    matches_file = open(path.join(path.dirname(__file__), "matches.txt"), "r")

    for line in matches_file.readlines():
        _, one, two, hand_one, hand_two = deserialize_match(line)

        # Get back all players from the match file
        update(players, one, two, beats(hand_one, hand_two))

    matches_file.close()