from sqlite3.dbapi2 import Cursor
from loguru import logger
import sqlite3
import unittest
import traceback
import os


class Database:
    def __init__(self, db_name="bingo.db") -> None:
        self.db_name = db_name
        self.db_structure = [
            {
                "Games": [
                    {"name": "GameID", "type": "INTEGER", "primary_key": True},
                    {"name": "combination", "type": "TEXT"},
                    {"name": "created_datetime", "type": "datetime"},
                ]
            },
            {
                "Tickets": [
                    {"name": "TicketID", "type": "INTEGER", "primary_key": True},
                    {"name": "GameID", "type": "INTEGER"},
                    {"name": "name", "type": "TEXT"},
                    {"name": "bet_amount", "type": "TEXT"},
                    {"name": "created_datetime", "type": "datetime"},
                ]
            },
        ]
        self.check_for_database()

    def check_for_database(self):
        if not os.path.exists(self.db_name):
            self.init_db()

    def init_db(self):
        c = self.connect_db()
        for table in self.db_structure:
            for table_name, fields in table.items():
                statement = f"CREATE TABLE {table_name}"
                field_statement = "("
                for field in fields:
                    field_name = field["name"]
                    field_type = field["type"]
                    pk = field.get("primary_key", False)
                    if pk:
                        field_statement += f"{field_name} {field_type} PRIMARY KEY ASC, "
                    else:
                        field_statement += f"{field_name} {field_type}, "
                field_statement += ")"
            statement += field_statement
            logger.debug(statement)
        raise Exception("Please implement")

    def connect_db(self) -> Cursor:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        return c

    def create_bingo_game(self, combinations: list):
        combinations = ",".join(combinations)
        statement = "INSERT INTO games "

    def open_bingo_game(self, game_id=1):
        results = []
        c = self.connect_db()
        try:
            fields = (game_id,)
            c.execute("SELECT * FROM games WHERE GameID=?", fields)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
            c.close()
        finally:
            return results

    def create_bingo_sheet(self, game_id: str, path: str):
        pass

    def open_bingo_sheet(self, game_id: int, ticket_id: int):
        pass


class Tests(unittest.TestCase):
    def setUp(self):
        self.test_class = Database("test.db")

    def test_form_statement(self):
        self.test_class.init_db()


if __name__ == "__main__":
    unittest.main()
