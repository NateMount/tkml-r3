#! /usr/bin/env python3.10

from .util import _read, _warn

def dbout(debug_statement:str) -> None:
	"""Prints debug info to stdout"""
	print("\033[48;2;253;236;10m\033[38;2;0;0;0m [DEBUG] \033[0m\033[38;2;29;212;119m " + debug_statement)

def debug(path:str) -> None:
	"""Reads in a tkml file to debug"""
	dbout("ON")

	data = _read(path)

	if 'init' not in data:
		dbout("Init header not found")
	else:
		if 'load' not in data['init']:
			dbout("No frame loaded by init")
		else:
			if data['init']['load'] not in data:
				dbout("Frame to be loaded by init not found in data")
