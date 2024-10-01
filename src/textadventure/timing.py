from time import perf_counter
from typing import Callable


def timeEvent(event: Callable, *params) -> tuple[float, any]:
	start_time = perf_counter()
	output = event(*params)
	end_time = perf_counter()
	return (end_time - start_time, output)
