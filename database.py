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
                "games": [
                    {"name": "GameID", "type": "integer", "primary_key": True},
                    {"name": "created_datetime", "type": "datetime"},
                    {"name": "combination", "type": "string"},
                ]
            },
            {
                "tickets": [

                ]
            }
        ]
        self.check_for_database()

    def check_for_database(self):
        if not os.path.exists(self.db_name):
            self.init_db()

    def init_db(self):
        c = self.connect_db()

        raise Exception("Please implement")

    def connect_db(self) -> Cursor:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        logger.debug(type(c))
        return c

    def create_bingo_game(self, combinations: list):
        combinations = ','.join(combinations)
        statement = "INSERT INTO games "

    def open_bingo_game(self, game_id = 1):
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

    def create_bingo_sheet(self, path: str):
        pass

    def open_bingo_sheet(self, game_id: int, ticket_id: int):
        pass


class Tests(unittest.TestCase):
    def setUp(self):
        self.test_class = Database("test.db")

    def test_database(self):
        self.test_class.connect_db()


if __name__ == "__main__":
    unittest.main()
