from app.routers.progress import _server_interactive_challenge


def test_interactive_challenges_honor_difficulty_for_all_languages():
    expected_counts = {1: 3, 2: 4, 3: 5}

    for language in ("ar", "fr", "en"):
        for difficulty, expected_count in expected_counts.items():
            memory, memory_solution = _server_interactive_challenge(
                "memory", language, difficulty
            )
            assert len(memory["cards"]) == expected_count * 2
            assert memory_solution["pair_count"] == expected_count
            assert len(memory_solution["pairs"]) == expected_count * 2

            matching, matching_solution = _server_interactive_challenge(
                "matching", language, difficulty
            )
            assert len(matching["left"]) == expected_count
            assert len(matching["right"]) == expected_count
            assert matching_solution["pair_count"] == expected_count
            assert len(matching_solution["pairs"]) == expected_count

            ordering, ordering_solution = _server_interactive_challenge(
                "ordering", language, difficulty
            )
            assert len(ordering["items"]) == expected_count
            assert len(ordering_solution["target"]) == expected_count
            assert {item["id"] for item in ordering["items"]} == set(
                ordering_solution["target"]
            )


def test_interactive_challenge_ids_are_unique():
    for game_id in ("memory", "matching", "ordering"):
        challenge, solution = _server_interactive_challenge(game_id, "en", 3)

        if game_id == "memory":
            ids = [card["id"] for card in challenge["cards"]]
            assert len(ids) == len(set(ids))
            assert set(ids) == set(solution["pairs"])
        elif game_id == "matching":
            left_ids = [item["id"] for item in challenge["left"]]
            right_ids = [item["id"] for item in challenge["right"]]
            assert len(left_ids) == len(set(left_ids))
            assert len(right_ids) == len(set(right_ids))
            assert set(left_ids) == set(solution["pairs"])
            assert set(right_ids) == set(solution["pairs"].values())
        else:
            ids = [item["id"] for item in challenge["items"]]
            assert len(ids) == len(set(ids))
            assert ids != solution["target"]
            assert set(ids) == set(solution["target"])
