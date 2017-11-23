import time
import unittest
from undo import *

#Testing the Undo class.
class testUndo(unittest.TestCase):

	def test___call__(self):
		u = Undo()
		a = []
		u(a.append, [3], [], "append a number", a.pop), [3]
		self.assertEqual(a, [3])

	def test_undo(self):
		u = Undo()
		a = []
		u(a.append, [3], [], "append a number", a.pop), [3]
		u(a.append, [3], [], "append a number", a.pop), [3,3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		self.assertEqual(a, [3, 3, 3])
		self.assertEqual(u.undo(), 3)
		self.assertEqual(u.undo(2), [3, 3])

	def test_redo(self):
		u = Undo()
		a = []
		u(a.append, [3], [], "append a number", a.pop), [3]
		u(a.append, [3], [], "append a number", a.pop), [3,3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		self.assertEqual(a, [3, 3, 3])
		self.assertEqual(u.undo(3), [3, 3, 3])
		self.assertEqual(a, [])
		u.redo()
		self.assertEqual(a, [3])
		u.redo(2)
		self.assertEqual(a, [3, 3, 3])

	def test_undoCount_redoCount_canUndo_canRedo(self):
		u = Undo()
		a = []
		self.assertFalse(u.canUndo())
		self.assertFalse(u.canRedo())
		self.assertEqual(u.undoCount(), 0)
		self.assertEqual(u.redoCount(), 0)
		u(a.append, [3], [], "append a number", a.pop), [3]
		u(a.append, [3], [], "append a number", a.pop), [3,3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		self.assertEqual(a, [3, 3, 3])
		self.assertEqual(u.undoCount(), 3)
		self.assertEqual(u.redoCount(), 0)
		self.assertTrue(u.canUndo())
		self.assertFalse(u.canRedo())
		u.undo()
		self.assertEqual(u.undoCount(), 2)
		self.assertEqual(u.redoCount(), 1)
		self.assertTrue(u.canUndo())
		self.assertTrue(u.canRedo())
		u.undo(2)
		self.assertEqual(u.undoCount(), 0)
		self.assertEqual(u.redoCount(), 3)
		self.assertTrue(u.canRedo())
		self.assertFalse(u.canUndo())
		u.redo()
		self.assertEqual(u.undoCount(), 1)
		self.assertEqual(u.redoCount(), 2)
		self.assertTrue(u.canUndo())
		self.assertTrue(u.canRedo())




if __name__ == "__main__":
	unittest.main()