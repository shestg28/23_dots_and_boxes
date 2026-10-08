import unittest

from game import DotsAndBoxes


class UndoTests(unittest.TestCase):
    def test_undo_with_no_history(self):
        g = DotsAndBoxes()
        self.assertFalse(g.undo())

    def test_undo_non_scoring_move(self):
        g = DotsAndBoxes()
        g.apply_move("H", 0, 0)  # P1
        self.assertEqual(g.current, 1)
        self.assertTrue(g.undo())
        self.assertFalse(g.board.horizontal[0][0])
        self.assertEqual(g.current, 0)
        self.assertEqual(g.scores, [0, 0])

    def test_undo_completing_move(self):
        g = DotsAndBoxes()
        g.apply_move("H", 0, 0)  # P1 -> P2
        g.apply_move("H", 1, 0)  # P2 -> P1
        g.apply_move("V", 0, 0)  # P1 -> P2
        g.apply_move("V", 0, 1)  # P2 completes box (0,0), plays again
        self.assertEqual(g.scores, [0, 1])
        self.assertEqual(g.current, 1)
        self.assertIn((0, 0), g.board.completed)

        self.assertTrue(g.undo())
        self.assertFalse(g.board.vertical[0][1])
        self.assertNotIn((0, 0), g.board.completed)
        self.assertEqual(g.scores, [0, 0])
        self.assertEqual(g.current, 1)  # P2 made the undone move

    def test_multiple_undos(self):
        g = DotsAndBoxes()
        g.apply_move("H", 0, 0)
        g.apply_move("V", 0, 0)
        g.undo()
        g.undo()
        self.assertEqual(g.current, 0)
        self.assertFalse(g.undo())


if __name__ == "__main__":
    unittest.main()