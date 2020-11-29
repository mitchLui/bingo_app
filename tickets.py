from loguru import logger
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.platypus.tables import TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import unittest
import os


class Tickets:
    def create_ticket(self, name="tickets/1/ticket.pdf") -> Canvas:
        doc = SimpleDocTemplate(name, pagesize=A4)
        return doc

    def get_body_style(self):
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet["BodyText"]
        body_style.fontSize = 11
        return body_style

    def add_name_to_ticket(self, elements: list, name: str) -> list:
        text = f"<b>Name</b>: {name}"
        elements.append(Paragraph(text, self.get_body_style()))
        return elements

    def add_number_to_ticket(
        self, elements: list, game_number: int, ticket_number: int
    ) -> list:
        text = f"<b>Serial Number</b>: {game_number}-{ticket_number}"
        elements.append(Paragraph(text, self.get_body_style()))
        return elements

    def add_amount_to_ticket(self, elements: list, amount: int) -> list:
        text = f"<b>Amount</b>: {float(amount)}<br />"
        elements.append(Paragraph(text, self.get_body_style()))
        return elements

    def add_grid_to_ticket(self, elements: list, numbers: list) -> list:
        t = Table(
            data=numbers,
            colWidths=len(numbers[0]) * [0.4 * inch],
            rowHeights=len(numbers) * [0.4 * inch],
        )
        t.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ]
            )
        )
        elements.append(t)
        return elements

    def create_dir(self, game_number: int) -> None:
        try:
            os.mkdir("tickets")
            os.chdir("tickets")
            os.mkdir(f"game_{game_number}")
        except Exception:
            pass

    def generate_ticket(self, ticket: dict, game_number=1) -> None:
        original_path = os.getcwd()
        self.create_dir(game_number)
        os.chdir(f"{os.getcwd()}/tickets/game_{game_number}")
        ticket_number = len(os.listdir()) + 1
        path = f"ticket_{ticket_number}.pdf"
        logger.debug(os.getcwd())
        logger.debug(path)
        doc = self.create_ticket(path)
        elements = []
        elements = self.add_name_to_ticket(elements, ticket["name"])
        elements = self.add_number_to_ticket(elements, game_number, ticket_number)
        elements = self.add_amount_to_ticket(elements, ticket["amount"])
        elements = self.add_grid_to_ticket(elements, ticket["numbers"])
        doc.build(elements)
        logger.info(f"Ticket {game_number}-{ticket_number} Generated.")
        os.chdir(original_path)
        logger.debug(os.getcwd())
        path = f"game_{game_number}/{path}"
        return path


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_class = Tickets()

    def test_generate_ticket(self) -> None:
        dummy_ticket_data = {
            "name": "test",
            "numbers": [[1, 2, 3, 4, 5, 6]],
            "amount": 100,
        }
        self.test_class.generate_ticket(dummy_ticket_data, 1, 1)


if __name__ == "__main__":
    unittest.main()
