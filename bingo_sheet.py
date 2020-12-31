from loguru import logger
from tickets import Tickets
import unittest
import traceback
import random
import shutil


class Create_sheet:
    def __init__(self, game_number: int, entry: dict) -> None:
        self.ticket_generator = Tickets()
        self.game_number = game_number
        self.entry = entry

    def format_entry(self) -> None:
        logger.debug(self.entry)
        self.entry["numbers"] = [self.entry["numbers"]]

    def generate_ticket(self) -> str:
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
    def setUp(self) -> None:
        try:
            shutil.rmtree("tickets")
        except Exception:
            pass
        entry = {
            "name": f"test",
            "amount": random.randint(1, 100),
            "numbers": [random.randint(1, 49) for _ in range(6)],
        }
        self.test_class = Create_sheet(1, entry)

    def test_create(self):
        logger.info(self.test_class.create_tickets())


if __name__ == "__main__":
    unittest.main()
