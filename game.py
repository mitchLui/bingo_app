from loguru import logger
from database import Database
import unittest
import os


class Game:
    def __init__(self, cwd: str, db_name="bingo.db") -> None:
        self.db = Database(cwd, db_name)

    def generate_odds(self, game_id: int) -> list:
        _, tickets = self.db.open_tickets_from_game(game_id)
        count = {str(x): 0 for x in range(1, 49)}
        for ticket in tickets:
            _, _, _, _, _, combinations, _ = ticket
            for num in combinations.split(","):
                try:
                    count[num] += 1
                except:
                    pass
        logger.debug(count)


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = Game(os.getcwd(), "test.db")

    def test_generate_odds(self):
        self.test_class.generate_odds(1)


if __name__ == "__main__":
    unittest.main()
