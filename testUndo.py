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


if __name__ == "__main__":
	unittest.main()