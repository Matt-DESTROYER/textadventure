import sys
from threading import Thread
from time import sleep
from getkey import getkey, keys


class InputThread(Thread):
	def __init__(self, callback):
		self.input_cbk = callback
		super(InputThread, self).__init__(name="input-thread")
		self.start()

	def run(self) -> None:
		while True:
			self.input_cbk(getkey())


_input_thread: InputThread = None
_input_print: bool = True
_input_reading: bool = True
_input_buffer: str = ""
_input_complete: bool = False


def _finish_condition(key):
	pass


_input_initialised: bool = False
def init_input() -> InputThread:
	if _input_initialised:
		return 
	_input_initialised = True
	
	dont_print = [keys.LEFT, keys.RIGHT, keys.UP, keys.DOWN]

	def key_press(key) -> None:
		global _input_print
		global _input_reading
		global _input_buffer
		global _input_complete
		if _finish_condition(key):
			_input_complete = True
			if _input_print:
				sys.stdout.write("\n")
				sys.stdout.flush()
			return
		if _input_reading and not key in dont_print:
			if not _finish_condition(key):
				_input_buffer += key
				if _input_print:
					sys.stdout.write(key)
					sys.stdout.flush()
			else:
				_input_complete = True
				if _input_print:
					sys.stdout.write("\n")
					sys.stdout.flush()

	input_thread = InputThread(key_press)

	return input_thread


def readLine(prompt: str = "", display: bool = True) -> str:
	global _input_print
	global _input_reading
	global _input_buffer
	global _input_complete
	global _finish_condition
	_input_print = display
	_input_reading = True
	_input_buffer = ""
	_input_complete = False

	def finish(key) -> bool:
		return key == keys.ENTER

	_finish_condition = finish
	sys.stdout.write(prompt)
	sys.stdout.flush()
	while not _input_complete:
		sleep(0.001)
	result = _input_buffer
	_input_reading = False
	_input_buffer = ""
	_input_complete = False
	return result


def readKey(prompt: str = "", display: bool = True) -> str:
	global _input_print
	global _input_reading
	global _input_buffer
	global _input_complete
	global _finish_condition
	_input_print = display
	_input_reading = True
	_input_complete = False
	global _key
	_key = None

	def finish(key) -> bool:
		global _key
		_key = key
		return True

	_finish_condition = finish
	sys.stdout.write(prompt)
	sys.stdout.flush()
	while not _input_complete:
		sleep(0.001)
	_input_reading = False
	_input_buffer = ""
	_input_complete = False
	return _key
