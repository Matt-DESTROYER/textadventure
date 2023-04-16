from sys import stdout as output
from time import sleep


def typewriter(text: str, delay: float = 0.07) -> None:
	for character in text:
		output.write(character)
		output.flush()
		sleep(delay)


def clear():
	print("\033[H\033[2J", end="", flush=True)
