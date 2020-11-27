from loguru import logger
from bingo_sheet import Create_sheet
from database import Database
import unittest
import random


class App_backend:
    def __init__(self) -> None:
        self.db = Database()

    def create_game(self, combinations: list):
        game_id = self.db.create_bingo_game(combinations)
        return game_id

    def create_ticket(self, game_id: int, entries: list):
        cs = Create_sheet(game_id, entries)
        ticket_path = cs.create_tickets()
        if ticket_path != 1:
            logger.info(ticket_path)
        else:
            raise Exception("Failure occured.")

    def open_game(self, game_id: int):
        num_of_tickets, tickets = self.db.open_tickets_from_game(game_id)
        return num_of_tickets, tickets

    def open_ticket(self):
        pass


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = App_backend()

    def generate_dummy_data(self):
        test_data = [
            {"name": f"test{x}", "amount": random.randint(0, 10001)} for x in range(101)
        ]
        return test_data

    def test_create_ticket(self):
        combinations = list(range(35))
        game_id = self.test_class.create_game(combinations)
        test_data = self.generate_dummy_data()
        self.test_class.create_ticket(game_id, test_data)


if __name__ == "__main__":
    unittest.main()
