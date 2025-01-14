# Switch-TC-PYTHON

The application tests threaded code generated by the editor of hierarchical state machines. The original scheme can be seen on the __switch_reset.svg__ attached to the project. It's model of a switch affected by two events: __TURN__ and __RESET__. The first switches two states __ON__ and __OFF__, the second resets the state machine to the __OFF__ state regardless of what state it was in before.

## Precondition

The editor's __Planner__ module was supplemented with __PY__ code generator, which automatically create the __switch_reset_helper.py__ file with the transfer functions. This file also contain function __createHelper__ builds __QHsmHelper__ class for processing these functions. A core has also been added to the application, which services the launch of threaded code and the impact of events on it. This is a set of several very simple classes placed to the __tc_core.py__ file: __EventWrapper__, which describes and keep an event, __QHsmHelper__ which contains a container of threaded codes and ensures its execution under the influence of events, __ThreadedCodeExecutor__ - a class ensures the launch of threaded code for a specific state and event.

The generated __switch_reset_helper.py__ file is a skeleton for the logical part of the application, namely the list and bodies of empty transfer functions that can and should be filled with some content. For example, with trace elements in the simplest case. Some functions may not be used and should be deleted or commented out:

>switch_reset_helper.py

```py

#	File switch_reset_helper.py automatically generated at 2025-01-05 10:23:52

from tc_core import QHsmHelper, ThreadedCodeExecutor
from typing import Optional

class Switch_resetHelper :
	def __init__(self) :
		self.helper_ = QHsmHelper('switch')
		self.create_helper()

#	Transfer functions

	# def switch_entry(self, data: Optional[object] = None) :
	# 	pass

	# def switch_init(self, data: Optional[object] = None) :
	# 	pass

	def off_entry(self, data: Optional[object] = None) :
		print('OFF')

	def off_reset(self, data: Optional[object] = None) :
		print('@RESET')

	# def off_exit(self, data: Optional[object] = None) :
	# 	pass

	def off_turn(self, data: Optional[object] = None) :
		print('OFF: TURN')

	def on_entry(self, data: Optional[object] = None) :
		print('ON')

	# def on_exit(self, data: Optional[object] = None) :
	# 	pass

	def on_turn(self, data: Optional[object] = None) :
		print('ON:  TURN')

	def init(self) :
		self.helper_.post('init')

	def run(self, event_name: str) :
		self.helper_.post(event_name)

	def create_helper(self) :
		self.helper_.insert('switch', 'init', ThreadedCodeExecutor(self.helper_, 'off', [
			# self.switch_entry,
			# self.switch_init,
			self.off_entry
		]))

		self.helper_.insert('off', 'RESET', ThreadedCodeExecutor(self.helper_, 'off', [
			self.off_reset,
			# self.off_exit,
			# self.switch_init,
			self.off_entry
		]))

		self.helper_.insert('off', 'TURN', ThreadedCodeExecutor(self.helper_, 'on', [
			self.off_turn,
			self.on_entry
		]))

		self.helper_.insert('on', 'RESET', ThreadedCodeExecutor(self.helper_, 'off', [
			self.off_reset,
			# self.on_exit,
			# self.off_exit,
			# self.switch_init,
			self.off_entry
		]))

		self.helper_.insert('on', 'TURN', ThreadedCodeExecutor(self.helper_, 'off', [
			self.on_turn,
			# self.on_exit,
			# self.off_exit,
			# self.switch_init,
			self.off_entry
		]))


```

## Additional modules

To test the threaded code for hierarchical state machine, need to manually create small module that ensure the launch of the application:

>test_switch.py

```py

from switch_reset_helper import Switch_resetHelper

def test_switch() :
    hsm_helper = Switch_resetHelper()
    hsm_helper.init()
    hsm_helper.run('TURN')
    hsm_helper.run('RESET')
    hsm_helper.run('TURN')
    hsm_helper.run('TURN')
    hsm_helper.run('RESET')

if __name__ == "__main__" :
    test_switch()


```

## Description of the application

The application is created as a __ubuntu console application__ and can be launched via __python3__ app in terminal mode as shown below:

```

micrcx@micrcx-desktop:~/py/switch_tc$ python3 test_switch.py
OFF
OFF: TURN
ON
@RESET
OFF
OFF: TURN
ON
ON : TURN
OFF
@RESET
OFF
micrcx@micrcx-desktop:~/py/switch_tc$

```

## Movie

[python.webm](https://github.com/user-attachments/assets/b550e28c-d1eb-474b-a861-b56e097d3869)



