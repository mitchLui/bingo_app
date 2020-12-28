from datetime import datetime
from loguru import logger
from bingo_sheet import Create_sheet
from database import Database
from game import Game
import unittest
import random
import shutil
import os
import webbrowser


class App_backend:
    def __init__(self, directory: str, db_name="bingo.db") -> None:
        logger.info(directory)
        self.db = Database(directory, db_name)
        self.game = Game(db = self.db)
        self.game_id = 0

    def create_game(self, combinations="test") -> None:
        self.game_id = self.db.create_bingo_game(combinations)

    def create_ticket(self, entry: dict) -> int:
        cs = Create_sheet(self.game_id, entry)
        ticket_data = cs.create_tickets()
        ticket_id = 0
        if ticket_data:
            name = ticket_data["name"]
            combinations = ticket_data["numbers"][0]
            amount = ticket_data["amount"]
            path = ticket_data["path"]
            ticket_id = self.db.create_bingo_sheet(
                self.game_id, path, name, amount, combinations
            )
        return ticket_id

    def get_all_games(self) -> list:
        games = self.db.get_all_games()
        games = [
            {
                "game_id": game_id,
                "combinations": combination,
                "created_datetime": c_datetime,
            }
            for (game_id, combination, c_datetime) in games
        ]
        return games

    def open_game(self) -> tuple:
        tickets = []
        num_of_tickets, ticket_data = self.db.open_tickets_from_game(self.game_id)
        for ticket_datum in ticket_data:
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

    def open_ticket(self, filepath: str) -> None:
        webbrowser.open(f"file://{filepath}")

    def generate_winning_combination(self, game_id: int) -> None:
        combination = self.game.generate_winning_combination(game_id)
        self.game.add_combination_to_database(game_id, combination)


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        db_name = "test.db"
        try:
            shutil.rmtree("tickets")
            os.remove(db_name)
        except Exception:
            pass
        self.test_class = App_backend(os.getcwd(), db_name)

    def generate_dummy_data(self):
        test_data = {
            "name": f"test",
            "amount": random.randint(0, 1000),
            "numbers": [random.randint(1, 49) for _ in range(6)],
        }
        return test_data

    def test_create_ticket(self):
        combinations = list(range(35))
        self.test_class.create_game(combinations)
        test_data = self.generate_dummy_data()
        self.test_class.create_ticket(test_data)
        num_of_tickets, tickets = self.test_class.open_game()
        logger.info(num_of_tickets)
        logger.info(tickets)

        self.test_class.open_ticket(
            f"{os.getcwd()}/tickets/game_{self.test_class.game_id}/ticket_1.pdf"
        )

    def test_get_all_games(self):
        for _ in range(4):
            self.test_class.create_game()
        self.test_class.get_all_games()


if __name__ == "__main__":
    unittest.main()
