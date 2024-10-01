from sys import stdout as output
from .output import clear
from getkey import keys
from .input import readKey


def menu(title: str, options: list[str]) -> int:
	selection = 0
	while True:
		clear()
		if title.strip() != "":
			output.write(title + "\n")
		for i in range(len(options)):
			if selection == i:
				output.write("> " + options[i] + " <")
			else:
				output.write("  " + options[i])
			output.write("\n")
		output.flush()

		key = readKey("", False)
		if key == keys.ENTER:
			return selection
		elif key == keys.UP:
			selection -= 1
			if selection < 0:
				selection = len(options) - 1
		elif key == keys.DOWN:
			selection += 1
			if selection >= len(options):
				selection = 0
