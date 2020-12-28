from loguru import logger
from database import Database
import random
import unittest
import os


class Game:
    def __init__(self, cwd="", db_name="bingo.db", db="") -> None:
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

    def generate_combination_count(self, game_id: int):
        odds = self.generate_odds(game_id)
        logger.debug(odds)
        picked_values = []
        while odds:
            picked_value = random.choices(
                population=list(odds.keys()), weights=list(odds.values())
            )[0]
            print(f"Chosen Value: {picked_value}")
            picked_values.append(picked_value)
            del odds[picked_value]
        return picked_values

    def add_combination_to_database(self, game_id: int, results: list):
        self.db.update_game_combinations(game_id, results)


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = Game(os.getcwd(), "test.db", "")

    def test_generate_odds(self):
        self.test_class.generate_combination_count(1)


if __name__ == "__main__":
    unittest.main()
