from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pathlib import Path
import unittest


class Tickets:
    def __init__(self) -> None:
        self.pdf_writer = PdfFileWriter()

    def generate_ticket(self, ticket_data: list, ticket_number):
        for number, ticket in enumerate(ticket_data, 1):
            self.pdf_writer.addPage()
            self.pdf_writer
        raise Exception("Function not implememnted yet.")

    def save_ticket(self):
        pass


class Tests(unittest.TestCase):
    def setUp(self):
        self.test_class = Tickets()

    def test_generate_ticket(self):
        dummy_ticket_data = {"name": "test", "numbers": [1, 2, 3, 4, 5, 6]}
        self.generate_ticket(dummy_ticket_data)


if __name__ == "__main__":
    unittest.main()
