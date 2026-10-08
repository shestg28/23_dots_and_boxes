from board import Board
from rules import valid_move, completed_boxes

class DotsAndBoxes:
    def __init__(self):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]
        # Each entry: (player, orientation, row, col, boxes_completed)
        self.history = []

    def apply_move(self, orientation, row, col):
        """Play a move for the current player and return boxes completed."""
        player = self.current
        before = set(self.board.completed)
        self.board.add_line(orientation, row, col)
        newly_completed = completed_boxes(self.board, before)

        self.history.append((player, orientation, row, col, newly_completed))

        if newly_completed:
            self.scores[player] += newly_completed
        else:
            self.current = 1 - self.current
        return newly_completed

    def undo(self):
        """Undo the last move, returning whether a move was undone."""
        if not self.history:
            return False

        player, orientation, row, col, _ = self.history.pop()
        cleared = self.board.remove_line(orientation, row, col)
        self.scores[player] -= len(cleared)
        self.current = player
        return True

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1")
        print("Enter U to undo your last move.")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            raw = input(f"Player {self.current + 1}, move: ").strip().upper()

            if raw == "U":
                if self.undo():
                    print("Last move undone.")
                else:
                    print("Nothing to undo.")
                continue

            parts = raw.split()

            if len(parts) != 3:
                print("Invalid format.")
                continue

            orientation, row, col = parts
            if not row.isdigit() or not col.isdigit():
                print("Row and column must be numbers.")
                continue

            row, col = int(row), int(col)
            if not valid_move(self.board, orientation, row, col):
                print("Invalid or already-used move.")
                continue

            player = self.current
            newly_completed = self.apply_move(orientation, row, col)

            if newly_completed:
                print(f"Player {player + 1} completed {newly_completed} box(es) and plays again.")

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")
