from loguru import logger
from tickets import Tickets
from copy import deepcopy
import unittest
import traceback
import random


class Create_sheet:
    def __init__(self, game_number: int, entries: list) -> None:
        self.ticket_generator = Tickets()
        self.game_number = game_number
        self.entries = entries
        self.num_range = list(range(1, 49))
        self.numbers_needed = 6

    def create_grid(self) -> list:
        grid = []
        i = 0
        num_range = deepcopy(self.num_range)
        while i != self.numbers_needed:
            random_index = random.randint(0, len(num_range) - 1)
            number = num_range.pop(random_index)
            grid.append(number)
            i += 1
        grid = [grid]
        return grid

    def create_ticket_data(self) -> list:
        tickets = []
        for person in self.entries:
            ticket = {}
            ticket.update(
                {
                    "name": person["name"],
                    "numbers": self.create_grid(),
                    "amount": person["amount"],
                }
            )
            tickets.append(ticket)
        return tickets

    def create_ticket(self, ticket_data: list) -> None:
        for ticket_number, ticket in enumerate(ticket_data, 1):
            logger.debug(ticket)
            self.ticket_generator.generate_ticket(
                ticket, self.game_number, ticket_number
            )

    def main(self) -> int:
        try:
            ticket_data = self.create_ticket_data()
            self.create_ticket(ticket_data)
            return 0
        except Exception:
            logger.error(traceback.format_exc())
            return 1


class Tests(unittest.TestCase):
    def setUp(self):
        names_list = [
            {"name": f"test{num}", "amount": random.randint(1, 100)}
            for num in range(1, 51)
        ]
        self.test_class = Create_sheet(1, names_list)

    def test_create(self):
        return_code = self.test_class.main()
        self.assertEqual(return_code, 0)


if __name__ == "__main__":
    unittest.main()
