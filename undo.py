from time import time
class Undo:
	"""Class to add undo and redo functionality to your project.
To use, create an Undo object.
u = Undo()
Call the undo object with instructions to do and undo an action. Note the action will be carried out immediately.
u(func, doArgs, undoArgs, description = "", undoFunc = False).
func: the function to carry out the do action.
doArgs: the arguments to carry out the action.
undoArgs: the arguments to undo the action.
description: an optional textual description of the action.
undoFunc: an optional function used to undo the action.

If no description is provided, a blank string is used.
If undoFunc is not provided, func is used.
To see how this works, check out the example at the bottom of the undo module file.
Examine the functions in this class to see how to
undo and redo the action, list actions, and more."""

	class UndoAction:
		"""This is an internal class which keeps track of how to do and undo one action.
Creating a new object:
UndoAction(func, doArgs, undoArgs, description = "", undoFunc = False).
func: the function to carry out the do action.
doArgs: the arguments to carry out the action.
undoArgs: the arguments to undo the action.
description: an optional textual description of the action.
undoFunc: an optional function used to undo the action.

If no description is provided, a blank string is used.
If undoFunc is not provided, func is used.
Example.
a = []
u = UndoAction(a.append, [3], [], "append 3 to a list", a.pop)
#at this point, no action has been taken.
u() #now the action is done.
u() #now it's undone.
u() #Now it's done.
#calling the object, IE u(), toggles the action. 
#Of course, if something else is done to the list,
a.append(9)
#the action is invalid.
u() #undoes the action by calling pop, but
#pop removed 9, not 3.
#the Undo class, also in this module, keeps track of state, and has an undo and redo function.
To see how this works, check out the example at the bottom of the undo module file.
"""

		def __init__(self, func, doArgs, undoArgs, description = "", undoFunc = False):
			self.func = func
			self.doArgs = doArgs
			self.undoArgs = undoArgs
			self.description = description
			self.undoFunc = undoFunc if undoFunc else func
			self.time = time()
			self.did = False

		def __call__(self):
			"""toggles doing and undoing the action.
This will not work if something has changed between toggling, unless state is restored."""
			self.did = not self.did
			if not self.did: #remember opposite not, did was toggled.
				return self.undoFunc(*self.undoArgs)
			else:
				 return self.func(*self.doArgs)

	#now the Undo class __init__
	def __init__(self):
		self.undoBuffer = []
		self.redoBuffer = []

	def __call__(self, func, doArgs, undoArgs, description = "", undoFunc = False):
		"""provides instructions to carry out and undo an action.
The action is carried out immediately, the result is returned."""
		u = self.UndoAction(func, doArgs, undoArgs, description, undoFunc)
		self.undoBuffer.append(u)
		self.redoBuffer = [] #state will be changed, can't redo.
		return u()

	def canUndo(self, count = 1):
		"""Returns True if undo can be called <count> times, or <count> can be passed to undo as an argument."""
		return len(self.undoBuffer) >= count

	def canRedo(self, count = 1):
		"""Returns True if redo can be called <count> times, or <count> can be passed to redo as an argument."""
		return len(self.redoBuffer) >= count

	def act(self, actions):
		"""This is an internal function which carries out requested undo or redo actions."""
		actions.reverse() #must be carried out in reverse.
		r = [i() for i in actions]
		if len(r) == 1:
			return r[0] #only one result, just return it.
		else:
			return r #return the list of results.

	def redo(self, count = 1):
		"""redo(count): redo <count> actions. Count defaults to 1."""
		if not self.canRedo(count):
			raise ValueError("Not enough actions in the buffer.")
		c=len(self.redoBuffer) - count #going to take <count> items from the end
		a = self.redoBuffer[c:]
		self.redoBuffer = self.redoBuffer[:c]
		self.undoBuffer += a
		return self.act(a)

	def undo(self, count = 1):
		"""undo(count): undo <count> actions. Count defaults to 1."""
		if not self.canUndo(count):
			raise ValueError("Not enough actions in the buffer.")
		c=len(self.undoBuffer) - count #going to take <count> items from the end
		a = self.undoBuffer[c:]
		self.undoBuffer = self.undoBuffer[:c]
		self.redoBuffer += a
		return self.act(a)

	def undoFromTime(self, t):
		"""undoFromTime(t): undoes from a specific time.
For example, to kill all actions taken in the last 5 minutes,
undoFromTime(time.time() - (60*5)) #time in seconds.""" 
		l = len(self.undoBuffer)
		i = l - 1
		while i >= 0 and self.undoBuffer[i].time >= t:
			i-= 1
		i += 1 #remember, i was the invalid condition where the test failed.
		return self.undo(l-i)

	def redoFromTime(self, t):
		"""redoFromTime(t): redoes from a specific time.
For example, to restore all actions taken in the last 5 minutes,
redoFromTime(time.time() - (60*5)) #time in seconds.""" 
		l = len(self.redoBuffer)
		i = l - 1
		while i >= 0 and self.redoBuffer[i].time >= t:
			i-=1
		i += 1 #remember, i was the invalid condition where the test failed.
		return self.redo(l-i)

	def group(self, buf, cmp):
		"""This is an internal function that applys most of the filter functions."""
		e = enumerate(buf)
		l = len(buf) 
		if l == 1:
			yield(next(e))
			return
		(starti, starta) = next(e)
		for (i, a) in e:
			if not cmp(starta, a):
				yield((l-starti, starta))
				(starti, starta) = (i, a)
		yield((l-starti, starta))

#filter functions
	def allActions(self, a, b):
		"""This is a filter function. Ironic, since it filters nothing, but...
This function is a filter used for the getUndos and getRedos functions, this returns all actions."""
		return False #false = include.

	#filters that group
	def groupByTime(self, dt = 1):
		"""A filter that groups actions by time. groups all actions that occured within dt. This is the only function that bust be called."""
		return lambda a, b: abs(b.time - a.time) <= dt

	def groupByDescription(self, a, b):
		"""A filter that groups items by description."""
		return a.description == b.description

	def groupByFunc(self, a, b):
		"""A filter that condenses by items that have the same undo function."""
		return a.func == b.func

	def getUndos(self, filter = None):
		"""gets all possible undoable actions, filtered by the function passed to <filter>, or the allActions filter if none is provided."""
		if filter == None:
			filter = self.allActions
		return self.group(self.undoBuffer, filter)

	def getRedos(self, filter = None):
		"""gets all possible redoable actions, filtered by the function passed to <filter>, or the allActions filter if none is provided."""
		if filter == None:
			filter = self.allActions
		return self.group(self.redoBuffer, filter)

	def clear(self):
		"""clears all action from the undo and redo buffers."""
		self.undoBuffer = []
		self.redoBuffer = []

	def undoCount(self):
		"""Returns the number of actions that can be undone."""
		return len(self.undoBuffer)

	def redoCount(self):
		"""Returns the number of actions that can be redone."""
		return len(self.redoBuffer)

