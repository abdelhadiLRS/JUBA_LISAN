import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

# Also runnable without the FastAPI/SQLAlchemy test environment.
path = Path(__file__).parents[1] / "app/services/game_arena.py"
spec = importlib.util.spec_from_file_location("arena", path)
arena = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arena)
bank = [SimpleNamespace(word=w, definition=d) for w, d in [
    ("book", "a written work"), ("water", "a drink"),
    ("school", "a place to study"), ("friend", "a person you like"),
    ("sun", "a bright star"), ("door", "an entrance"),
]]


def move(state, kind, **kwargs):
    return dict(action_id=f"move-{len(state['log'])}", version=len(state["log"]),
                kind=kind, **kwargs)


class ArenaTests(unittest.TestCase):
    def test_hidden_deck_has_no_labels_or_pair_keys(self):
        state = arena.create("memory", bank, 1, now=0)
        visible = arena.public(state)
        self.assertTrue(all(card["label"] is None for card in visible["cards"]))
        self.assertNotIn("questions", visible)
        self.assertNotIn("log", visible)
        self.assertTrue(all("pair" not in c and "pair_key" not in c for c in visible["cards"]))

    def test_flip_is_validated_and_replay_does_not_double_count(self):
        state = arena.create("memory", bank, 1, now=0)
        first = state["cards"][0]
        second = next(c for c in state["cards"] if c["pair"] == first["pair"] and c != first)
        request = move(state, "flip", value=first["id"])
        self.assertTrue(arena.apply(state, request, now=1))
        self.assertFalse(arena.apply(state, request, now=2))
        self.assertEqual(len(state["opened"]), 1)
        arena.apply(state, move(state, "flip", value=second["id"]), now=2)
        self.assertEqual(state["correct"], 1)
        with self.assertRaises(ValueError):
            arena.apply(state, move(state, "hide"), now=2.1)
        arena.apply(state, move(state, "hide"), now=3)
        with self.assertRaises(ValueError):
            arena.apply(state, move(state, "flip", value=first["id"]), now=4)

    def test_wrong_pairs_and_move_limit_produce_loss(self):
        state = arena.create("memory", bank, 1, now=0)
        state["max_moves"] = 1
        a = state["cards"][0]
        b = next(c for c in state["cards"] if c["pair"] != a["pair"])
        arena.apply(state, move(state, "flip", value=a["id"]), now=1)
        arena.apply(state, move(state, "flip", value=b["id"]), now=2)
        self.assertEqual(state["phase"], "finished")
        self.assertFalse(arena.score(state)["won"])
        self.assertEqual(arena.score(state)["xp"], 0)

    def test_memory_can_be_won(self):
        state = arena.create("memory", bank, 3, now=0)
        pairs = {}
        for card in state["cards"]:
            pairs.setdefault(card["pair"], []).append(card["id"])
        for index, ids in enumerate(pairs.values()):
            for card_id in ids:
                arena.apply(state, move(state, "flip", value=card_id), now=index*3)
            if state["phase"] != "finished":
                arena.apply(state, move(state, "hide"), now=index*3+1)
        self.assertTrue(arena.score(state)["won"])
        self.assertEqual(arena.score(state)["xp"], 25)

    def test_letter_builder_requires_each_tile_once(self):
        state = arena.create("word_scramble", bank, 1, now=0)
        question = state["questions"][0]
        with self.assertRaises(ValueError):
            arena.apply(state, move(state, "answer", order=[question["tiles"][0]["id"]]*len(question["tiles"])))
        tiles = list(question["tiles"])
        order = []
        for char in arena.letters(question["word"]):
            tile = next(t for t in tiles if t["label"] == char)
            order.append(tile["id"])
            tiles.remove(tile)
        arena.apply(state, move(state, "answer", order=order), now=1)
        self.assertEqual(state["correct"], 1)
        self.assertEqual(state["phase"], "feedback")
        self.assertEqual(arena.public(state)["feedback"]["answer"], question["word"])

    def test_server_clock_rejects_late_correct_choice(self):
        state = arena.create("quick_choice", bank, 3, now=0)
        answer = state["questions"][0]["definition"]
        with self.assertRaises(ValueError):
            arena.apply(state, move(state, "timeout"), now=1)
        arena.apply(state, move(state, "answer", value=answer), now=100)
        self.assertEqual(state["correct"], 0)
        self.assertEqual(state["lives"], 2)

    def test_relaxed_mode_has_no_clock(self):
        state = arena.create("quick_choice", bank, 1, relaxed=True, now=0)
        arena.apply(state, move(state, "answer", value=state["questions"][0]["definition"]), now=1000)
        self.assertEqual(state["correct"], 1)

    def test_invalid_stale_and_id_reuse_rejected(self):
        state = arena.create("memory", bank, 1, now=0)
        first = move(state, "flip", value=state["cards"][0]["id"])
        arena.apply(state, first)
        with self.assertRaises(ValueError):
            arena.apply(state, dict(first, value=state["cards"][1]["id"]))
        with self.assertRaises(ValueError):
            arena.apply(state, dict(first, action_id="stale"))
        with self.assertRaises(ValueError):
            arena.apply(state, move(state, "flip", value="unknown"))

    def test_combining_marks_and_repeated_letters(self):
        self.assertEqual(arena.letters("مَاء"), ["مَ", "ا", "ء"])
        self.assertEqual(arena.letters("letter").count("t"), 2)

    def test_no_unrelated_fallback_when_content_missing(self):
        for game in arena.GAMES:
            with self.assertRaises(ValueError):
                arena.create(game, [], 1)


if __name__ == "__main__":
    unittest.main()
