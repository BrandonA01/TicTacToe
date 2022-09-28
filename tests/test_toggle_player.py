import unittest
from Game import TicTacToeGame

class TestGame(unittest.TestCase):

    def test_toggle_player(self):
        new_game = TicTacToeGame()
        self.assertEqual('X', new_game.current_player.label, "not player X")
        new_game.toggle_player()
        self.assertEqual('O', new_game.current_player.label, "not player O")


if __name__ == '__main__':
    unittest.main()