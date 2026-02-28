from uuid import uuid4
from collections import defaultdict, deque
from datetime import datetime, timedelta
from hands import Hand, beats
from serialization import serialize_match
from elo import update

def find_matchup(player: str, queue: deque[str], players: defaultdict[str, float]) -> str:
    queue_ratings = [players[other] for other in queue]
    return queue[queue_ratings.index(min([abs(players[player] - rating) for rating in queue_ratings]))]

def add_match(one: str, two: str, player_queued: defaultdict[str, bool], busy: defaultdict[str, str], matches: dict[str, tuple[datetime, str, str, Hand, Hand]]) -> str:
    match_id = str(uuid4())

    busy[one] = match_id
    busy[two] = match_id
    player_queued[one] = True
    player_queued[two] = True

    matches[match_id] = (datetime.now(), one, two, Hand.NONE, Hand.NONE)

    return match_id

def match_done(match_id: str, matches: dict[str, tuple[datetime, str, str, Hand, Hand]]) -> bool:
    if match_id not in matches:
        return True
    
    timestamp, _, _, one, two = matches[match_id]

    if datetime.now() - timestamp > timedelta(seconds=10):
        return True

    return one != Hand.NONE and two != Hand.NONE

def remove_match(match_id: str, players: defaultdict[str, float], player_queued: defaultdict[str, bool], busy: defaultdict[str, str], matches: dict[str, tuple[datetime, str, str, Hand, Hand]]):
    timestamp, one, two, hand_one, hand_two = matches[match_id]

    update(players, one, two, beats(hand_one, hand_two))

    busy[one] = ""
    busy[two] = ""
    player_queued[one] = False
    player_queued[two] = False

    del matches[match_id]

    serialize_match(timestamp, one, two, hand_one, hand_two)

def clean_matches(players: defaultdict[str, float], player_queued: defaultdict[str, bool], busy: defaultdict[str, str], matches: dict[str, tuple[datetime, str, str, Hand, Hand]]):
    for match_id in matches:
        if match_done(match_id, matches):
            remove_match(match_id, players, player_queued, busy, matches)

def queue_player(player: str, queue: deque[str], players: defaultdict[str, float], player_queued: defaultdict[str, bool], busy: defaultdict[str, str], matches: dict[str, tuple[datetime, str, str, Hand, Hand]]):
    clean_matches(players, player_queued, busy, matches)

    if busy[player] or player_queued[player]:
        return
    
    queue.append(player)