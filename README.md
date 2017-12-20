#undo.py
##A simple way to implement undo/redo in python
###Creation:
```python
from undo import Undo
myUndo = Undo()
```
###Usage

Instead of calling a function to do something, call myUndo with instructions on how to do and undo the thing. This causes two things to happen. First, myUndo keeps track of the instructions you gave it, enabling undo and redo functionality for this thing. Second, it carries out the action.

```python
myUndo(func, doArgs, undoArgs, description, undoFunc)
```

* func: the function you would call to cary out an action.
* doArgs: a list or tuple containing the arguments you would pass to func, above.
* undoArgs: a list or tuple containing the arguments you would pass to undo the action.
* description: a user readable description of what you are doing. "paste text" for example. If nothing is provided, a blank string will be used.
* undoFunc: the function you would call to undo the action. If nothing is passed, func, above, will be used instead.

When you do this, the action will be carried out immediately.

####Example

```python
a = []
myUndo(a.append, [3], [], "append a number", a.pop)
#now a is [3] because the action has been carried out.
```

###undo and redo

The functions undo and redo have one argument, count, which tells that function how many times to repeat itself. For example, to undo 3 actions, 
```python
undo(3)
```
Count defaults to 1, so undo and redo() undoes or redoes one action by default.

####Continued example

```python
#remember a = [3].
myUndo.undo()
#now a = [].
#this undid the previous action, append(3), by calling pop() on the list.
myUndo.redo()
#now a = [3] again, we redid the action.
```

###undoCount, redoCount

The functions undoCount and redoCount return the number of undo and redo actions in the buffer.

####Example

```python
#from the previous examples
myUndo.undoCount #= 1, we can undo one time.
myUndo.redoCount #= 0, nothing to redo.
myUndo.undo()
myUndo.undoCount #= 0, nothing to undo.
myUndo.redoCount #= 1, we can redo one time.
myUndo.redo() #restore back for further examples.
```

###clear

This function takes no arguments, it clears the buffers. When this is called, the object has the same state as it did when you first created it.

###canUndo canRedo

These functions have one argument, count, which defaults to 1. These functions return true if you can undo or redo count times.

####example

```python
#Continuing from all of our previous examples.
myUndo.canUndo() #True, we have 1 undo action in the buffer.
myUndo.canRedo() #False, nothing left to redo.
myUndo.canUndo(9) #False, there is only 1 undo available.
```

###undoFromTime redoFromTime

These functions undo or redo any actions after a specified time, as shown from time.time. They take one argument, the time desired.

####Example

```python
#continuing from previous examples.
#Suppose we want to undo anything from the last five minutes.
t = time.time() #= now
t = t - (60 * 5) #time is in seconds, subtract 60 seconds * 5 (5 minutes).
myUndo.undoFromTime(t) #any action carried out in the last 5 minutes has been undone.
#suppose we only want to redo the last 2 minutes.
t += 180 #t was -5 minuts, add 3 minutes to it.
myUndo.redoFromTime(t) #All actions in the last 2 minutes were restored.
```

###getUndos getRedos

These functions have one argument, filter. They return all actions in the undo or redo buffer, respectively, filtered by the filter function provided. If no filter is provided, all actions in the respective buffer are returned. See the filter functions below, and the examples that highlight their use.

These functions return a tuple. The first element is the number of undos/redos it would take to get to this action. The second element is the action itself. The action has several fields, but only two are for use.

* description, the text description you provided
* time: the time this action was carried out. 

###allActions

This is a filter function to be passed to getUndos and getRedos. This function is the default, and need not be passed, but it is here for completeness.

There are also 3 functions that group the buffer. They are:

* groupByTime(dt): groups actions that happened within dt seconds of each other.
* groupByDescription: groups functions that have the same description together.
* groupByFunc: groups items that have the same func function.

To better understand how these work, see the below example.

####Example

```python
#grouping functions and getUndos getRedos
#Remember, myUndo has been modified from undoFromTime redoFromTime, above.
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
```

###warning

Please note, undo and redo only works if state has *not been modified* outside the methods explained here.

In our first example, we created a list, then used the Undo class to add a number. If you add another number without using the class, a.append(9) for example, then call myUndo.undo(), you will not remove the 3 we added at the beginning, but the 9 added later. 

In short, if you want to use the Undo class, then make sure that all actions to an object are handled by the Undo class, or behaviour will be unstable.

###The Examples

The examples in this file have been compiled to one file, examples.py, and are pasted below for you to use.

```python
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
```
#Thank you for your time and interest.
