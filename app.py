from dearpygui.core import *
from dearpygui.simple import *
from loguru import logger
from app_backend import App_backend
import os
import traceback
from concurrent.futures import ThreadPoolExecutor
import time


class App:
    def __init__(self) -> None:
        self.cwd = os.getcwd()
        logger.info(f"CWD: {self.cwd}")
        self.init = False
        self.app_backend = None

    def check_init(self) -> None:
        if not self.init:
            self.app_backend = App_backend(os.getcwd(), "bingo.db")
            self.init = True

    def verify_game(self, sender, data) -> None:
        try:
            delete_item("Error")
        except:
            pass
        if not self.init:
            delete_item("Load Game")
            self.load_game()
            self.error_window("Please create or choose a game.")

    def close_window(self, sender, data) -> None:
        delete_item(sender)

    def update_game_id_text(self, game_id: int) -> None:
        set_value("game_id_display", f"Game ID: {game_id}")

    def create_game(self, sender, data) -> None:
        self.app_backend.create_game()
        logger.info(f"Created Game ID: {self.app_backend.game_id}")
        delete_item("Create New Game")
        self.update_game_id_text(self.app_backend.game_id)
        self.get_combinations()

    def create_game_window(self, sender, data) -> None:
        try:
            self.close_window("Create New Game", None)
            self.close_window("Load Game", None)
            self.reset_combination()
            self.check_init()
        except Exception:
            pass
        with window("Create New Game", on_close=self.close_window, autosize=True):
            add_button("Confirm", callback=self.create_game)

    def get_combinations(self) -> None:
        combination = self.app_backend.get_combination_from_game()
        if not combination:
            logger.info("No combo")
            add_button("Draw", callback=self.create_combination, parent="Bingo")
        else:
            try:
                delete_item("Draw")
                delete_item("Winning numbers:")
                self.reset_combination(False)
            except Exception:
                pass
            combination = list(reversed(combination.split(",")))
            try:
                #!DEBUG
                run_async_function(
                    self.combination_handler,
                    data=combination,
                    return_handler=self.combination_return_handler,
                )
                logger.debug("End")
            except:
                logger.error(traceback.format_exc())

    def combination_return_handler(self, sender, data) -> None:
        logger.info(f"handler {data}")
        add_text("Winning numbers:", parent="Bingo")
        current = ""
        last = ""
        for elem in data:
            current = elem["source"]
            text = elem["text"]
            if last != current:
                add_text(text, parent="Bingo", source=current)
            else:
                set_value(current, text)
            last = current

    def combination_handler(self, sender, combination) -> list:
        write_text = []
        try:
            logger.debug(combination)
            i = 1
            for index in range(1, len(combination) + 1):
                if (index - 1) % 10 == 0 or (index - 6) % 10 == 0:
                    write_text.append(
                        {"source": f"draw_{i}", "text": f"{combination[index-1]}"}
                    )
                if (index - 2) % 10 == 0 or (index - 7) % 10 == 0:
                    write_text.append(
                        {
                            "source": f"draw_{i}",
                            "text": f"{combination[index-1]} {combination[index-2]}",
                        }
                    )
                if (index - 3) % 10 == 0 or (index - 8) % 10 == 0:
                    write_text.append(
                        {
                            "source": f"draw_{i}",
                            "text": f"{combination[index-1]} {combination[index-2]} {combination[index-3]}",
                        }
                    )
                if (index - 4) % 10 == 0 or (index - 9) % 10 == 0:
                    write_text.append(
                        {
                            "source": f"draw_{i}",
                            "text": f"{combination[index-1]} {combination[index-2]} {combination[index-3]} {combination[index-4]}",
                        }
                    )
                if index % 5 == 0:
                    write_text.append(
                        {
                            "source": f"draw_{i}",
                            "text": f"{combination[index-1]} {combination[index-2]} {combination[index-3]} {combination[index-4]} {combination[index-5]}",
                        }
                    )
                    i += 1
        except Exception as e:
            logger.error(traceback.format_exc())
        finally:
            return write_text

    def reset_combination(self, reset_text=True) -> None:
        try:
            combination = self.app_backend.get_combination_from_game()
            combination = list(reversed(combination.split(",")))
            for index in range(1, len(combination) + 1):
                if index % 5 == 0:
                    delete_item(
                        f"{combination[index-1]} {combination[index-2]} {combination[index-3]} {combination[index-4]} {combination[index-5]}"
                    )
            if reset_text:
                self.update_game_id_text("N/A")
        except:
            pass

    def create_combination(self, sender, data) -> None:
        self.app_backend.generate_winning_combination(self.app_backend.game_id)
        self.get_combinations()

    def open_game(self, sender, data) -> None:
        selected_cell = get_table_selections("Games")
        logger.debug(selected_cell)
        self.app_backend.game_id = selected_cell[0][0] + 1
        logger.debug(self.app_backend.game_id)
        delete_item("Open Game")
        self.update_game_id_text(self.app_backend.game_id)
        self.get_combinations()

    def open_games_table(self) -> None:
        games = self.app_backend.get_all_games()
        table_name = "Games"
        add_table(table_name, ["Game ID", "Created On"], callback=self.open_game)
        for game in games:
            add_row(table_name, [f"{game['game_id']}", f"{game['created_datetime']}"])

    def open_game_window(self, sender, data) -> None:
        try:
            self.close_window("Open Game", None)
            self.close_window("Load Game", None)
            self.check_init()
            self.reset_combination()
        except Exception:
            pass
        with window("Open Game", on_close=self.close_window, width=1000, height=400):
            self.open_games_table()
            add_button("Cancel", callback=self.close_open_game)

    def close_open_game(self, sender, data) -> None:
        delete_item("Open Game")

    def check_numbers(self, numbers: list) -> tuple:
        valid = False
        index = 0
        error = ""
        try:
            for index, number in enumerate(numbers):
                valid_input = 1 <= int(number) <= 48
                if valid_input:
                    valid = True
                else:
                    valid = False
                    error = f"Number is not between 1 and 48. (Number: {index+1})"
                    break
            if len(set(numbers)) != 6:
                valid = False
                error = f"Duplicate numbers. Check input."
        except Exception:
            valid = False
            error = f"Did not enter a number (Number: {index+1})"
        finally:
            return valid, error, numbers

    def check_text(self, text: str) -> tuple:
        if text and not text.isspace():
            text = text.rstrip()
            text = text.lstrip()
            return True, text
        return False, text

    def check_number(self, number: str) -> tuple:
        valid = False
        try:
            number = int(number)
            valid = True
        except:
            pass
        finally:
            return valid, number

    def create_ticket(self, sender, data) -> None:
        self.check_init()
        success = False
        ticket_id = 0
        name = get_value("ticket_name")
        valid_name, name = self.check_text(name)
        bet_amount = get_value("bet_amount")
        valid_amount, bet_amount = self.check_number(bet_amount)
        numbers = [get_value(f"ticket_num_{num}") for num in range(1, 7)]
        valid_numbers, error, numbers = self.check_numbers(numbers)
        if valid_name and valid_numbers and valid_amount:
            numbers = [int(x) for x in numbers]
            entry = {"name": name, "amount": bet_amount, "numbers": numbers}
            game_id = self.app_backend.game_id
            if game_id == 0:
                self.error_window("Please create or choose a game.")
            else:
                ticket_id = self.app_backend.create_ticket(entry)
                success = True
        else:
            if not valid_name:
                error = "Name and/or bet amount is not valid."
            elif not valid_amount:
                error = "Bet amount is not valid."
            self.error_window(error)
        if success:
            delete_item("Create New Ticket")
            with window(
                "Confirm new ticket",
                on_close=self.close_window,
                autosize=True,
            ):
                add_text("Ticket created with the following information: ")
                add_text(f"Name: {name}")
                add_text(f"Bet Amount: {bet_amount}")
                add_text(f"Numbers: {', '.join([str(x) for x in numbers])}")
                add_button(
                    "View Ticket", callback=self.open_ticket, callback_data=ticket_id
                )
                add_button("Close Window", callback=self.close_create_ticket_window)

    def close_create_ticket_window(self, sender, data) -> None:
        delete_item("Confirm new ticket")

    def error_window(self, error: str) -> None:
        with window("Error", on_close=self.close_window):
            add_text(error)
            add_button("OK", callback=self.close_error)

    def close_error(self, sender, data) -> None:
        delete_item("Error")

    def create_ticket_window(self, sender, data) -> None:
        try:
            self.close_window("Create New Ticket", None)
            self.close_window("Load Game", None)
        except Exception:
            pass
        if not self.init:
            self.verify_game(None, None)
        else:
            with window("Create New Ticket", autosize=True, on_close=self.close_window):
                add_input_text("Name", source="ticket_name")
                add_input_text("Amount", source="bet_amount")
                add_input_text("Number 1", source="ticket_num_1")
                add_input_text("Number 2", source="ticket_num_2")
                add_input_text("Number 3", source="ticket_num_3")
                add_input_text("Number 4", source="ticket_num_4")
                add_input_text("Number 5", source="ticket_num_5")
                add_input_text("Number 6", source="ticket_num_6")
                add_button("Create Ticket", callback=self.create_ticket)

    def open_ticket(self, sender, data) -> None:
        if isinstance(data, list):
            path = f"{data[0]}/{data[1]}"
        else:
            path = f"{os.getcwd()}/tickets/game_{self.app_backend.game_id}/ticket_{data}.pdf"
        self.app_backend.open_ticket(path)

    def open_ticket_window(self, sender, data) -> None:
        open_file_dialog(callback=self.open_ticket)

    def load_game(self) -> None:
        with window("Load Game", autosize=True, on_close=self.verify_game):

            add_button("Create new game", callback=self.create_game_window)
            add_button("Load game", callback=self.open_game_window)

    def show(self) -> None:
        with window("Bingo"):
            set_main_window_size(1920, 1080)
            set_main_window_resizable(True)
            set_global_font_scale(1.25)
            with menu_bar("Main Menu Bar"):

                with menu("Game"):
                    add_menu_item("New game", callback=self.create_game_window)
                    add_menu_item("Open game", callback=self.open_game_window)

                with menu("Ticket"):
                    add_menu_item("New ticket", callback=self.create_ticket_window)
                    add_menu_item("Open ticket", callback=self.open_ticket_window)

                with menu("Settings"):
                    add_menu_item("Show style menu", callback=show_style_editor)

            add_text(f"Game ID: N/A", source="game_id_display", parent="Bingo")

        self.load_game()

        start_dearpygui(primary_window="Bingo")


if __name__ == "__main__":
    app = App()
    app.show()
