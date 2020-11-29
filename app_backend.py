from loguru import logger
from bingo_sheet import Create_sheet
from database import Database
import unittest
import random
import shutil
import os


class App_backend:
    def __init__(self, db_name="bingo.db") -> None:
        self.db = Database(db_name)
        self.game_id = 0

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
                ticket_id = self.db.create_bingo_sheet(
                    game_id, path, name, amount, combinations
                )
                ticket_ids.append(ticket_id)
        return ticket_ids

    def open_game(self, game_id: int) -> tuple:
        tickets = []
        num_of_tickets, ticket_data = self.db.open_tickets_from_game(game_id)
        for ticket_datum in ticket_data:
            logger.debug(ticket_datum)
            (
                ticket_id,
                game_id,
                path,
                name,
                amount,
                combinations,
                created_datetime,
            ) = ticket_datum
            tickets.append(
                {
                    "ticket_id": ticket_id,
                    "game_id": game_id,
                    "path": path,
                    "name": name,
                    "amount": amount,
                    "combinations": combinations,
                    "created_datetime": created_datetime,
                }
            )
        return num_of_tickets, tickets

    def open_ticket(self, ticket_id: int):
        ticket_info = self.db.open_specific_bingo_sheet(ticket_id)
        return ticket_info


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        db_name = "test.db"
        try:
            shutil.rmtree("tickets")
            os.remove(db_name)
        except Exception:
            pass
        self.test_class = App_backend(db_name)

    def generate_dummy_data(self):
        test_data = [
            {
                "name": f"test{x}",
                "amount": random.randint(0, 1000),
                "combination": [random.randint(1, 49) for _ in range(6)],
            }
            for x in range(20)
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

        ticket_info = self.test_class.open_ticket(2)


if __name__ == "__main__":
    unittest.main()
