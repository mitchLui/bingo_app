from loguru import logger
from bingo_sheet import Create_sheet
from database import Database
import unittest
import random
import os


class App_backend:
    def __init__(self, db_name = "bingo.db") -> None:
        self.db = Database(db_name)

    def create_game(self, combinations: list) -> int:
        game_id = self.db.create_bingo_game(combinations)
        return game_id

    def create_ticket(self, game_id: int, entries: list) -> list:
        cs = Create_sheet(game_id, entries)
        ticket_data = cs.create_tickets()
        ticket_ids = []
        if ticket_data:
            for ticket_datum in ticket_data:
                name = ticket_datum["name"]
                combinations = ticket_datum["numbers"][0]
                amount = ticket_datum["amount"]
                path = ticket_datum["path"]
                ticket_id = self.db.create_bingo_sheet(game_id, path, name, amount, combinations)
                ticket_ids.append(ticket_id)
        return ticket_ids

    def open_game(self, game_id: int) -> tuple(int, list):
        num_of_tickets, tickets = self.db.open_tickets_from_game(game_id)
        return num_of_tickets, tickets

    def open_ticket(self):
        pass


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        db_name = "test.db"
        try:
            os.remove(db_name)
        except Exception:
            pass
        self.test_class = App_backend(db_name)

    def generate_dummy_data(self):
        test_data = [
            {"name": f"test{x}", "amount": random.randint(0, 10001)} for x in range(20)
        ]
        return test_data

    def test_create_ticket(self):
        combinations = list(range(35))
        game_id = self.test_class.create_game(combinations)
        test_data = self.generate_dummy_data()
        self.test_class.create_ticket(game_id, test_data)
        num_of_tickets, tickets = self.test_class.open_game(1)
        logger.info(num_of_tickets)
        logger.info(tickets)


if __name__ == "__main__":
    unittest.main()
