from datetime import date
from sqlite3.dbapi2 import Cursor
from loguru import logger
import datetime as dt
import sqlite3
import unittest
import traceback
import os


class Database:
    def __init__(self, cwd: str, db_name="bingo.db") -> None:
        self.db_name = db_name
        self.db_path = f"{cwd}/{db_name}"
        logger.debug(self.db_path)
        self.db_structure = [
            {
                "Games": [
                    {"name": "GameID", "type": "INTEGER", "primary_key": True},
                    {"name": "combination", "type": "TEXT", "notnull": True},
                    {"name": "created_datetime", "type": "TEXT"},
                ]
            },
            {
                "Tickets": [
                    {"name": "TicketID", "type": "INTEGER", "primary_key": True},
                    {
                        "name": "GameID",
                        "type": "INTEGER",
                        "foregin_key": True,
                        "references": "Games (GameID)",
                    },
                    {"name": "path", "type": "TEXT"},
                    {"name": "name", "type": "TEXT"},
                    {"name": "bet_amount", "type": "INTEGER"},
                    {"name": "combination", "type": "TEXT"},
                    {"name": "created_datetime", "type": "TEXT"},
                ]
            },
        ]
        self.check_for_database()

    def check_for_database(self) -> None:
        db_exists = os.path.exists(self.db_path)
        if not db_exists:
            self.init_db()

    def get_datetime(self) -> str:
        return dt.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    def init_db(self) -> None:
        conn, c = self.connect_db()
        c.execute("PRAGMA foreign_keys = 1;")
        for table in self.db_structure:
            statement = f"CREATE TABLE"
            for table_name, fields in table.items():
                statement += f" {table_name}"
                foreign_keys = []
                field_statement = "("
                for index, field in enumerate(fields):
                    field_name = field["name"]
                    field_type = field["type"]
                    pk = field.get("primary_key", False)
                    if pk:
                        field_statement += f"{field_name} {field_type} PRIMARY KEY ASC"
                    else:
                        if field.get("notnull", False):
                            field_statement += f"{field_name} {field_type}"
                        else:
                            field_statement += f"{field_name} {field_type} NOT NULL"
                    if index + 1 != len(fields):
                        field_statement += ", "
                    fk = field.get("foregin_key", False)
                    if fk:
                        foreign_keys.append(
                            {"name": field_name, "references": field["references"]}
                        )
                if foreign_keys:
                    keys = [x["name"] for x in foreign_keys]
                    references = [x["references"] for x in foreign_keys]
                    field_statement += f", FOREIGN KEY ({','.join(keys)}) REFERENCES {','.join(references)}"
                field_statement += ");"
                statement += field_statement
            logger.debug(statement)
            c.execute(statement)
        conn.commit()
        conn.close()

    def connect_db(self) -> Cursor:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        return conn, c

    def check_for_games(self) -> bool:
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

    def create_bingo_game(self) -> int:
        game_id = 0
        created_datetime = self.get_datetime()
        statement = f"INSERT INTO Games (created_datetime) VALUES (?);"
        values = (
            created_datetime,
        )
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

    def create_bingo_sheet(
        self, game_id: str, path: str, name: str, bet_amount: int, combination: list
    ) -> int:
        ticket_id = 0
        created_datetime = self.get_datetime()
        combination = ",".join([str(x) for x in combination])
        statement = f"INSERT INTO Tickets (GameID, path, name, bet_amount, combination, created_datetime) VALUES (?, ?, ?, ?, ?, ?);"
        values = (game_id, path, name, bet_amount, combination, created_datetime)
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

    def open_specific_bingo_sheet(self, ticket_id: int) -> list:
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
        num_of_tickets = 0
        fields = (game_id,)
        statement = "SELECT * FROM Tickets WHERE GameID=?;"
        conn, c = self.connect_db()
        try:
            c.execute(statement, fields)
            results = c.fetchall()
            num_of_tickets = len(results)
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            conn.close()
            return num_of_tickets, results

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

    def update_game_combinations(self, game_id: int, combinations: list) -> None:
        statement = "UPDATE Games SET combination = ? WHERE GameID = ?;"
        conn, c = self.connect_db()
        fields = (
            ",".join(combinations),
            game_id,
        )
        try:
            c.execute(statement, fields)
            conn.commit()
        except Exception:
            conn.rollback()
            logger.error(traceback.format_exc())
        finally:
            conn.close()

    def get_combination(self, game_id: int) -> list:
        results = []
        statement = "SELECT combination FROM Games WHERE GameID=?;"
        fields = (game_id,)
        conn, c = self.connect_db()
        try:
            c.execute(statement, fields)
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
        self.test_class = Database(os.getcwd(), "test.db")

    def tearDown(self) -> None:
        self.setUp()

    def test_games_table(self):
        # * Creating Games
        self.assertEqual(self.test_class.check_for_games(), False)
        self.assertEqual(self.test_class.create_bingo_game([1, 2, 3, 4]), 1)
        self.assertEqual(self.test_class.create_bingo_game([34, 5, 4, 6]), 2)
        self.assertEqual(self.test_class.check_for_games(), True)
        # * Selecting Games
        game_info = self.test_class.open_bingo_game(1)
        game_id, combinations, _ = game_info[0]
        self.assertEqual(game_id, 1)
        self.assertEqual(combinations, "1,2,3,4")
        game_info = self.test_class.open_bingo_game(2)
        game_id, combinations, _ = game_info[0]
        self.assertEqual(game_id, 2)
        self.assertEqual(combinations, "34,5,4,6")
        self.assertEqual(self.test_class.open_bingo_game(3), [])
        # * Getting information from all games
        game_info = self.test_class.get_all_games()
        game_id1, combinations1, _ = game_info[0]
        game_id2, combinations2, _ = game_info[1]
        self.assertEqual(game_id1, 1)
        self.assertEqual(combinations1, "1,2,3,4")
        self.assertEqual(game_id2, 2)
        self.assertEqual(combinations2, "34,5,4,6")

    def test_tickets_table(self):
        # * Creating a Ticket
        # Test FK constraints
        self.assertEqual(
            self.test_class.create_bingo_sheet(
                1, "tickets/game_1/ticket_1.pdf", "test", 100, [1, 2, 3, 4, 5, 6]
            ),
            0,
        )
        # New Sheet
        self.assertEqual(self.test_class.create_bingo_game([1, 2, 3, 4]), 1)
        self.assertEqual(
            self.test_class.create_bingo_sheet(
                1, "tickets/game_1/ticket_1.pdf", "test", 100, [1, 2, 3, 4, 5, 6]
            ),
            1,
        )
        self.assertEqual(
            self.test_class.create_bingo_sheet(
                1, "tickets/game_1/ticket_1.pdf", "test1", 90, [1, 2, 3, 4, 7, 6]
            ),
            2,
        )
        # * Retrieving Tickets From Game
        num_of_tickets, tickets = self.test_class.open_tickets_from_game(1)
        self.assertEqual(num_of_tickets, 2)
        logger.info(f"Tickets: {tickets}")


if __name__ == "__main__":
    unittest.main()
