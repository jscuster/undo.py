from time import *
import unittest
from undo import *

#Testing the Undo class.
class TestUndo(unittest.TestCase):

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

	def buildTimedActions(self):
		u = Undo()
		a=[]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.reverse, [], [], "reverse")
		sleep(2)
		u(a.reverse, [], [], "reverse")
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		t=time()
		return (a, u, t)

	def buildUntimedActions(self):
		u = Undo()
		a=[]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.reverse, [], [], "reverse")
		u(a.reverse, [], [], "reverse")
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		u(a.append, [3], [], "append a number", a.pop), [3, 3, 3]
		return (a, u)

	def test_undoFromTime_redoFromTime(self):
		(a, u, t) = self.buildTimedActions()
		self.assertEqual(u.undoCount(), 6)
		self.assertEqual(u.redoCount(), 0)
		t-=1 #a second before
		u.undoFromTime(t) #should've removed 3.
		self.assertEqual(u.undoCount(), 3)
		self.assertEqual(u.redoCount(), 3)
		u.redoFromTime(t) #should've added 3.
		self.assertEqual(u.undoCount(), 6)
		self.assertEqual(u.redoCount(), 0)

	def test_grouping(self):
		(a, u, t) = self.buildTimedActions()
		self.assertEqual(a, [3,3,3,3])
		#groupByDescription
		descGroup = list(u.getUndos(u.groupByDescription))
		self.assertEqual(len(descGroup), 3)
		self.assertEqual([i[0] for i in descGroup], [6,4,2])
		timeGroup = list(u.getUndos(u.groupByTime(1)))
		self.assertEqual(len(timeGroup), 2)
		self.assertEqual([i[0] for i in timeGroup], [6, 3])
		#groupByFunc
		funcGroup = list(u.getUndos(u.groupByFunc))
		self.assertEqual(funcGroup, descGroup) #descriptions changed with function calls, should be equal.

	def test_getUndo_getRedo_clear(self):
		(a, u) = self.buildUntimedActions()
		tmp = list(u.getUndos())
		self.assertEqual(len(tmp), 6)
		u.undo(6)
		tmp = list(u.getRedos())
		self.assertEqual(len(tmp), 6)
		u.clear()
		self.assertEqual(u.undoCount(), 0)
		self.assertEqual(u.redoCount(), 0)

if __name__ == "__main__":
	unittest.main()