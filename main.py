from serialization import deserialize_matches
import atexit
from collections import defaultdict, deque
from datetime import datetime
from hands import Hand
from matchmaking import clean_matches, queue_player

from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

def handle_exit():
    clean_matches(players, player_queued, busy, matches)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/name", methods=["POST"])
def register_name():
    name = request.form.get('name')

    if name in players:
        return jsonify({"name", ""})

    return jsonify({"name": name})

@app.route("/queue", methods=["POST"])
def add_to_queue():
    name: str = request.form.get('name')

    queue_player(name, queue, players, player_queued, busy, matches)

    if name in players:
        return jsonify({"name", ""})

    return jsonify({"name": name})

if __name__ == "__main__":
    players: defaultdict[str, float] = defaultdict(lambda: 1200.0)
    busy: defaultdict[str, str] = defaultdict(str)
    queue: deque[str] = deque()
    player_queued: defaultdict[str, bool]
    matches: dict[str, tuple[datetime, str, str, Hand, Hand]]
    
    atexit.register(handle_exit)
    deserialize_matches(players)