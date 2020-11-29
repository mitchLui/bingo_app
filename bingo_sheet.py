from unittest.case import expectedFailure
from loguru import logger
from tickets import Tickets
from copy import deepcopy
import unittest
import traceback
import random
import shutil
import os


class Create_sheet:
    def __init__(self, game_number: int, entry: dict) -> None:
        self.ticket_generator = Tickets()
        self.game_number = game_number
        self.entry = entry
        self.num_range = list(range(1, 49))
        self.numbers_needed = 6

    def format_entry(self) -> None:
        logger.debug(self.entry)
        self.entry["numbers"] = [self.entry["numbers"]]

    def generate_ticket(self) -> None:
        path = self.ticket_generator.generate_ticket(self.entry, self.game_number)
        return path

    def create_tickets(self) -> list:
        try:
            self.format_entry()
            path = self.generate_ticket()
            self.entry.update({"path": path})
            return self.entry
        except Exception:
            logger.error(traceback.format_exc())
            return []


class Tests(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree("tickets")
        except Exception:
            pass
        names_list = [
            {
                "name": f"test{num}",
                "amount": random.randint(1, 100),
                "numbers": [random.randint(1, 49) for _ in range(6)],
            }
            for num in range(1, 21)
        ]
        self.test_class = Create_sheet(1, names_list)

    def test_create(self):
        logger.info(self.test_class.create_tickets())


if __name__ == "__main__":
    unittest.main()
