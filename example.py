import time
from undo import Undo
myUndo = Undo()
a = []
myUndo(a.append, [3], [], "append a number", a.pop)
#now a is [3] because the action has been carried out.
print(a) #[3]
print("\n")

#undoCount redoCount
print("undoCount = " + str(myUndo.undoCount())) #prints 1, we can undo one time.
print("\n")
print("redoCount = " + str(myUndo.redoCount())) #prints 0, nothing to redo.
print("\n")
myUndo.undo()
print("undoCount = " + str(myUndo.undoCount())) #prints 0, nothing to undo.
print("\n")
print("redoCount = " + str(myUndo.redoCount())) #prints 1, we can redo one time.
print("\n")
myUndo.redo() #restore back for further examples.

#canUndo canRedo
print(myUndo.canUndo()) #prints True, we have 1 undo action in the buffer.
print("\n")
print(myUndo.canRedo()) #prints False, nothing left to redo.
print("\n")
print(myUndo.canUndo(9)) #prints False, there is only 1 undo available.
print("\n")

#undoFromTime, redoFromTime
#Suppose we want to undo anything from the last five minutes.
t = time.time() #= now
t = t - (60 * 5) #time is in seconds, subtract 60 seconds * 5 (5 minutes).
myUndo.undoFromTime(t) #any action carried out in the last 5 minutes has been undone.
#suppose we only want to redo the last 2 minutes.
t += 180 #t was -5 minuts, add 3 minutes to it.
myUndo.redoFromTime(t) #All actions in the last 2 minutes were restored.

#grouping functions and getUndos getRedos
#Remember, myUndo has been modified from undoFromTime redoFromTime.
#lets reset everything.
myUndo.clear()
a=[]
#Lets add some actions to filter.
myUndo(a.append, [1], [], "append a number", a.pop) #a = [1]
myUndo(a.append, [3], [], "append a number", a.pop) #a = [1, 3]
time.sleep(2) #simulate the user doing something else
myUndo(a.append, [5], [], "append a number", a.pop) #a = [1, 3, 5]
myUndo(a.reverse, [], [], "reverse the list") #note no undoFunc is passed, it is the same as the function to carry out the action.
#a = [5, 3, 1]
#let's reverse again to keep the numbers strait.
myUndo(a.reverse, [], [], "reverse the list") #note no undoFunc is passed, it is the same as the function to carry out the action.
#a = [1, 3, 5]
myUndo(a.append, [7], [], "append a number", a.pop) #a = [1, 3, 5, 7]
myUndo(a.append, [9], [], "append a number", a.pop) #a = [1, 3, 5, 7, 9]
#Sorry for this long-winded buildup, but we can't filter actions without actions in the buffer.
#print a to make sure it's what we think.
print(a) #= [1, 3, 5, 7, 9]
print("\n")
#allActions returns every action, so let's move to a grouping filter.
#Let's start with groupByDescription.
descriptionGroup = myUndo.getUndos(myUndo.groupByDescription) #descriptionGroup is an iterator object.
print(list(descriptionGroup))
print("\n")
#on my machine, I get [(7, <undo.Undo.UndoAction object at 0x03164750>), (4, <undo.Undo.UndoAction object at 0x0316D9D0>), (2, <undo.Undo.UndoAction object at 0x0316DA30>)].
#Let's create a function to print the description of the action.

def printActions(actions):
#actions is an iterator that has a tuple that is: (items to undo to get here, the action).
	for (i, a) in actions:
		print("undo " + str(i) + "to undo \"" + a.description + "\".")

#ok, let's try that again.
descriptionGroup = myUndo.getUndos(myUndo.groupByDescription) #descriptionGroup is an iterator object.
printActions(descriptionGroup)
#much better. Now we see this.
"""
undo 7to undo "append a number".
undo 4to undo "reverse the list".
undo 2to undo "append a number".
"""

#The items have been grouped by their description.
#We have 3 items that "append a number", starting at 7 undos.
#We have 2 "reverse the list" items at 4 undos.
#and 2 more "append a number" items starting at 2 undos.

#In other words, to clear all the reverses, and everything that followed, call myUndo.undo(4)

#groupByTime
timeGroup = myUndo.getUndos(myUndo.groupByTime(1)) #this function bust be called to get the filter, in this case, all items that happened within 1 second of eachother.
#remember we had a sleep for 2 seconds, so we should have 2 groups.
printActions(timeGroup)
#We get
"""
undo 7to undo "append a number".
undo 5to undo "append a number".
"""
#This is correct, we appended two numbers, slept, then did other things.

#groupBuFunc
#undoByFunc will be the same as undoByDescription in this case, because the descriptions changed with the function calls.
funcGroup = myUndo.getUndos(myUndo.groupByFunc)
printActions(funcGroup)
#As promiced,
"""
undo 7to undo "append a number".
undo 4to undo "reverse the list".
undo 2to undo "append a number".
"""
