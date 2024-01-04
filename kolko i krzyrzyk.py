
class Board:
    def __init__(self, field_dimension=3):
        self.field_dimension = field_dimension

        self.field = []
        for _ in range(field_dimension):
            self.field.append([None] * field_dimension)
        self.next_move = "X"
        self.result = None
        self.game_is_over = False
        self.last_move_coordinates = None

    def is_coords_inside(self, coords):
        return (
                0 <= coords[0] < self.field_dimension
                and 0 <= coords[1] < self.field_dimension
            )

    def check_if_game_is_over(self):
        if self.last_move_coordinates is None:
            return

        in_a_row_to_win = 5 if self.field_dimension >= 5 else 3

        symbol_to_check = self.field[self.last_move_coordinates[0]][self.last_move_coordinates[1]]

        for coordinates_to_change in ((0, ), (1, ), (0, 1)):
            currently_in_a_row = 0
            coordinates_to_check = list(self.last_move_coordinates)
            for i in range(-in_a_row_to_win + 1, in_a_row_to_win):
                for single_coordinate in coordinates_to_change:
                    coordinates_to_check[single_coordinate] += i

                row_to_check, col_to_check = coordinates_to_check

                if not self.is_coords_inside((row_to_check, col_to_check)):
                    continue

                if self.field[row_to_check][col_to_check] == symbol_to_check:
                    currently_in_a_row += 1
                    if currently_in_a_row == in_a_row_to_win:
                        self.game_is_over = True
                        self.result = f"Winner: {symbol_to_check}"
                        break
                else:
                    currently_in_a_row = 0

            if self.game_is_over is True:
                break


class View:
    def draw_board(self, board):
        for row in board.field:
            for cell in row:
                print((cell or " "), end="|")

            print()
            print("--" * board.field_dimension)

    def print_message(self, message):
        print(message)


class Controller:
    def __init__(self, view, board):
        self.view = view
        self.board = board

    def place_move(self, position: tuple):
        self.board.field[position[0]][position[1]] = self.board.next_move
        self.board.next_move = "X" if self.board.next_move == "0" else "0"
        self.board.last_move_coordinates = position

    def get_next_move(self):
        self.view.print_message(f"Print coordinates of your next move: {self.board.next_move} ")

        inputted_row, inputted_column = None, None
        while True:
            inputted_coordinates = input()
            try:
                inputted_row, inputted_column = inputted_coordinates.split(",")
                inputted_row = int(inputted_row)
                inputted_column = int(inputted_column)

            except Exception:
                self.view.print_message("Print coordinates like: Row, column")
                continue

            if not self.board.is_coords_inside((inputted_row, inputted_column)):
                self.view.print_message("Coordinates may be in board")
                continue

            if self.board.field[inputted_row][inputted_column] is not None:
                self.view.print_message("This field is taken")
                continue

            break

        return inputted_row, inputted_column

    def start_game(self):
        self.view.print_message("Game started!")
        while not self.board.game_is_over:
            self.view.draw_board(self.board)
            next_move = self.get_next_move()
            self.place_move(next_move)
            self.board.check_if_game_is_over()
        self.view.draw_board(self.board)

        self.view.print_message(f"Result - {self.board.result}")


if __name__ == "__main__":
    controller = Controller(View(), Board())
    while True:
        controller.start_game()
        play_again = input("Play again?")
        if not play_again or play_again.lower() in ["no", "n", "nie"]:
            break


