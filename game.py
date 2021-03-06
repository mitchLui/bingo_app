from database import Database
import random
import unittest
import os


class Game:
    def __init__(self, cwd="", db_name="bingo.db", db=None) -> None:
        if not db:
            self.db = Database(cwd, db_name)
        else:
            self.db = db

    def generate_odds(self, game_id: int) -> list:
        _, tickets = self.db.open_tickets_from_game(game_id)
        count = {str(x): 1 for x in range(1, 49)}
        for ticket in tickets:
            _, _, _, _, _, combinations, _ = ticket
            for num in combinations.split(","):
                try:
                    count[num] += 1
                except:
                    pass
        odds = {x: y / sum(list(count.values())) for x, y in count.items()}
        return odds

    def generate_winning_combination(self, game_id: int) -> list:
        odds = self.generate_odds(game_id)
        picked_values = []
        i = 0
        while i != 35:
            picked_value = random.choices(
                population=list(odds.keys()), weights=list(odds.values())
            )[0]
            picked_values.append(picked_value)
            del odds[picked_value]
            i += 1
        return picked_values

    def add_combination_to_database(self, game_id: int, results: list) -> None:
        self.db.update_game_combinations(game_id, results)


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = Game(os.getcwd(), "test.db", None)

    def test_generate_odds(self):
        self.test_class.generate_winning_combination(1)


if __name__ == "__main__":
    unittest.main()
