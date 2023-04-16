from .input import readKey, readLine, keys, init_input
from .menu import menu
from .output import clear
from .timing import timeEvent

ACTIONS: list[str] = [
 "SCENE", "GOTO", "TEXT", "OPTIONS", "OPTION", "INTERACTION", "SUCCESS",
 "FAIL", "END"
]
_ACTIONS: list[str] = ["[" + action + "]" for action in ACTIONS]

game_running: bool = False
scenes: dict[str, list] = {}
current_scene: str = None


class Action:
	__slots__ = ()

	def __init__(self) -> None:
		pass

	def action(self) -> None:
		pass


class InvalidActionError(Exception):
	action: str
	message: str
	__slots__ = ("action", "message")

	def __init__(self, action: str) -> None:
		self.action = action
		self.message = f"The action '{action}' is not a valid action."
		super().__init__(self.message)


class Goto(Action):
	scene: str
	__slots__ = ("scene")

	def __init__(self, scene: str) -> None:
		super().__init__()
		self.scene = scene

	def action(self) -> None:
		global current_scene
		current_scene = self.scene


class Text(Action):
	text: str
	__slots__ = ("text")

	def __init__(self, text: str) -> None:
		super().__init__()
		self.text = text

	def action(self) -> None:
		print(self.text)
		readLine("> Continue <\n", False)


class Options(Action):
	text: str
	options: list[str]
	actions: list[str]
	__slots__ = ("text", "options", "actions")

	def __init__(self, text: str, options: list[str]) -> None:
		super().__init__()
		self.text = text
		self.options = [_option[0] for _option in options]
		self.actions = [_option[1] for _option in options]

	def action(self) -> None:
		action = self.actions[menu(self.text, self.options)]
		if action[0:6].upper() == "[GOTO]":
			global current_scene
			current_scene = action[6:].strip()


class Success(Action):
	scene: str
	__slots__ = ("scene")

	def __init__(self, scene: str) -> None:
		super().__init__()
		self.scene = scene

	def action(self) -> None:
		global current_scene
		current_scene = self.scene


class Fail(Action):
	scene: str
	__slots__ = ("scene")

	def __init__(self, scene: str) -> None:
		super().__init__()
		self.scene = scene

	def action(self) -> None:
		global current_scene
		current_scene = self.scene


class Interaction(Action):
	key: str
	timeout: float
	success: Success
	fail: Fail
	__slots__ = ("key", "timeout", "success", "fail")

	def __init__(self, key: str, timeout: float, success: Success,
	             fail: Fail) -> None:
		super().__init__()
		self.key = key.upper()
		self.timeout = timeout
		self.success = success
		self.fail = fail

	def action(self) -> None:

		def checkSuccess(target_key):
			return readKey("", False) == getattr(keys, target_key)

		result = timeEvent(checkSuccess, self.key)
		if result[1]:
			if result[0] < self.timeout:
				self.success.action()
			else:
				self.fail.action()
		else:
			self.fail.action()


class End(Action):
	__slots__ = ()

	def __init__(self) -> None:
		super().__init__()

	def action(self) -> None:
		global game_running
		game_running = False


def index(_: list | tuple, item: any) -> int:
	i = 0
	while i < len(_):
		if _[i] == item:
			return i
		i += 1
	return -1


def load_scenes(file: str) -> None:
	"""Loads all the scenes from the input file based on it's name/path."""
	global ACTIONS
	global _ACTIONS
	global scenes
	global current_scene
	lines = None
	with open(file, "r") as _scenes:
		lines = _scenes.read()
	lines = lines.splitlines()
	scene = None
	i = 0
	while i < len(lines):
		line = lines[i]
		action_idx = index(_ACTIONS, line.split(" ")[0].strip().upper())
		if action_idx != -1:
			action = ACTIONS[action_idx]
			if action == "SCENE":
				scene = line[7:]
				i += 1
				line = lines[i].strip()
				while line != "" and line[0] != "[":
					scene += "\n" + lines[i]
					i += 1
					line = lines[i].strip()
				i -= 1
				scene = scene.strip()
				if current_scene == None:
					current_scene = scene
				scenes[scene] = []
			elif action == "GOTO":
				_scene = line[6:]
				i += 1
				line = lines[i].strip()
				while line != "" and line[0] != "[":
					_scene += "\n" + lines[i]
					i += 1
					line = lines[i].strip()
				i -= 1
				_scene = _scene.strip()
				scenes[scene].append(Goto(_scene))
			elif action == "TEXT":
				text = line[6:]
				i += 1
				line = lines[i].strip()
				while line != "" and line[0] != "[":
					text += "\n" + lines[i]
					i += 1
					line = lines[i].strip()
				scenes[scene].append(Text(text.strip()))
				i -= 1
			elif action == "OPTIONS":
				text = line[9:].strip()
				i += 1
				line = lines[i].strip()
				options = []
				while line[0:8] == "[OPTION]":
					print
					option = line[9:]
					i += 1
					line = lines[i].strip()
					while line != "" and line[0] != "[":
						option += "\n" + lines[i]
						i += 1
						line = lines[i].strip()
					goto = line
					line = lines[i].strip()
					while line != "" and line[0] != "[":
						goto += "\n" + lines[i]
						i += 1
						line = lines[i].strip()
					goto = goto.strip()
					options.append([option, goto])
					i += 1
					line = lines[i].strip()
				scenes[scene].append(Options(text, options))
				i -= 1
			elif action == "INTERACTION":
				key, timeout = line[13:].strip().split(" ")
				i += 1
				command1 = lines[i].strip().upper()
				i += 1
				action1 = lines[i].strip()[6:].strip()
				i += 1
				command2 = lines[i].strip().upper()
				i += 1
				action2 = lines[i].strip()[6:].strip()
				success: Success = None
				fail: Fail = None
				if command1 == "[SUCCESS]":
					success = Success(action1)
				elif command1 == "[FAIL]":
					fail = Fail(action1)
				if command2 == "[FAIL]":
					fail = Fail(action2)
				elif command2 == "[SUCCESS]":
					success = Success(action2)
				scenes[scene].append(Interaction(key, float(timeout), success, fail))
			elif action == "END":
				scenes[scene].append(End())
			elif line == "":
				continue
			else:
				InvalidActionError(action)
		i += 1


def start_game() -> None:
	"""Starts the text adventure game using any already loaded scenes."""
	global game_running
	global scenes
	global current_scene
	game_running = True
	while game_running:
		i = 0
		while i < len(scenes[current_scene]):
			clear()
			scenes[current_scene][i].action()
			i += 1
	clear()
