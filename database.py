from datetime import date
from sqlite3.dbapi2 import Cursor
from unittest.case import expectedFailure
from loguru import logger
import datetime as dt
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
                    {"name": "created_datetime", "type": "TEXT"},
                ]
            },
            {
                "Tickets": [
                    {"name": "TicketID", "type": "INTEGER", "primary_key": True},
                    {"name": "GameID", "type": "INTEGER", "foregin_key": True, "references": "Games(GameID)"},
                    {"name": "path", "type": "TEXT"},
                    {"name": "name", "type": "TEXT"},
                    {"name": "bet_amount", "type": "INTEGER"},
                    {"name": "combination", "type": "TEXT"},
                    {"name": "created_datetime", "type": "TEXT"},
                ]
            },
        ]
        self.check_for_database()

    def check_for_database(self):
        if not os.path.exists(self.db_name):
            self.init_db()

    def get_datetime(self):
        return dt.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    def init_db(self):
        conn, c = self.connect_db()
        for table in self.db_structure:
            for table_name, fields in table.items():
                statement = f"CREATE TABLE {table_name}"
                field_statement = "("
                for index, field in enumerate(fields):
                    field_name = field["name"]
                    field_type = field["type"]
                    pk = field.get("primary_key", False)
                    if pk:
                        field_statement += f"{field_name} {field_type} PRIMARY KEY ASC"
                    else:
                        field_statement += f"{field_name} {field_type}"
                    fk = field.get("foregin_key", False)
                    if fk:
                        field_statement += f" REFERENCES {field['references']}"
                    if index + 1 != len(fields):
                        field_statement += ", "
                field_statement += ");"
            statement += field_statement
            c.execute(statement)
        conn.commit()
        conn.close()

    def connect_db(self) -> Cursor:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        return conn, c

    def check_for_games(self):
        result = False
        conn, c = self.connect_db()
        try:
            statement = f"SELECT * FROM Games;"
            c.execute(statement)
            games = c.fetchall()
            if len(games) >= 1:
                result = True
        except Exception:
            logger.error(traceback.format_exc())
            conn.rollback()
        finally:
            conn.close()
            return result

    def create_bingo_game(self, combinations: list) -> int:
        game_id = 0
        combinations = [str(x) for x in combinations]
        combinations = ",".join(combinations)
        created_datetime = self.get_datetime()
        statement = f"INSERT INTO Games (combination, created_datetime) VALUES (?, ?);"
        values = (combinations, created_datetime,)
        conn, c = self.connect_db()
        try:
            c.execute(statement, values)
            game_id = c.lastrowid
            conn.commit()
        except Exception:
            logger.error(traceback.format_exc())
            conn.rollback()
        finally:
            conn.close()
            return game_id

    def open_bingo_game(self, game_id=1) -> list:
        results = []
        fields = (game_id,)
        statement = "SELECT * FROM Games WHERE GameID=?;"
        conn, c = self.connect_db()
        try:
            c.execute(statement, fields)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return results

    def get_all_games(self) -> list:
        results = []
        statement = "SELECT * FROM Games;"
        conn, c = self.connect_db()
        try:
            c.execute(statement)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return results

    def create_bingo_sheet(self, game_id: str, path: str, name: str, bet_amount: int) -> int:
        ticket_id = 0
        created_datetime = self.get_datetime()
        statement = f"INSERT INTO Tickets (GameID, path, name, bet_amount, created_datetime) VALUES (?, ?, ?, ?, ?);"
        values = (game_id, path, name, bet_amount, created_datetime)
        conn, c = self.connect_db()
        try:
            c.execute(statement, values)
            ticket_id = c.lastrowid
            conn.commit()
        except Exception:
            logger.error(traceback.format_exc())
            conn.rollback()
        finally:
            conn.close()
            return ticket_id

    def open_specific_bingo_sheet(self, ticket_id: int) -> int:
        results = []
        fields = (ticket_id,)
        statement = "SELECT * FROM Tickets WHERE TicketID=?;"
        conn, c = self.connect_db()
        try:
            c.execute(statement, fields)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return results

    def open_tickets_from_game(self, game_id: int) -> list:
        results = []
        fields = (game_id,)
        statement = "SELECT * FROM Tickets WHERE GameID=?;"
        conn, c = self.connect_db()
        try:
            c.execute(statement, fields)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return results

    def get_all_tickets(self) -> list:
        results = []
        statement = "SELECT * FROM Tickets;"
        conn, c = self.connect_db()
        try:
            c.execute(statement)
            results = c.fetchall()
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return results


class Tests(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("test.db")
        except Exception:
            pass
        self.test_class = Database("test.db")

    def test_games_table(self):
        #* Creating Games
        self.assertEqual(self.test_class.check_for_games(), False)
        self.assertEqual(self.test_class.create_bingo_game([1,2,3,4]), 1)
        self.assertEqual(self.test_class.create_bingo_game([34,5,4,6]), 2)
        self.assertEqual(self.test_class.check_for_games(), True)
        #* Selecting Games
        game_info = self.test_class.open_bingo_game(1)
        game_id, combinations, _ = game_info[0]
        self.assertEqual(game_id, 1)
        self.assertEqual(combinations, "1,2,3,4")
        game_info = self.test_class.open_bingo_game(2)
        game_id, combinations, _ = game_info[0]
        self.assertEqual(game_id, 2)
        self.assertEqual(combinations, "34,5,4,6")
        self.assertEqual(self.test_class.open_bingo_game(3), [])
        game_info = self.test_class.get_all_games()
        game_id1, combinations1, _ = game_info[0]
        game_id2, combinations2, _ = game_info[1]
        self.assertEqual(game_id1, 1)
        self.assertEqual(combinations1, "1,2,3,4")
        self.assertEqual(game_id2, 2)
        self.assertEqual(combinations2, "34,5,4,6")

    def test_tickets_table(self):
        pass

    def test_tickets_without_game(self):
        pass


if __name__ == "__main__":
    unittest.main()
