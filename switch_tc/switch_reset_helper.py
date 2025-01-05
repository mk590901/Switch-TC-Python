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

