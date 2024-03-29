#! /usr/bin/env python3.10

import sys
import yaml
import json


def _debug(*args, **kwargs) -> None:
	"""
	Display debug statement to stdout only if --debug flag set
	@param args: list of arguments
	@param kwargs: list of keyword arguments
	"""

	if '--debug' in sys.argv:
		print('\033[38;2;248;153;47m\033[48;2;46;47;46m [DEBUG] ', *args, **kwargs, sep=' ', end='')
		print('\033[0m')


def _warn(warning_str:str) -> None:
	"""
	Display warning text to stdout
	@param warning_str: string to be displayed as warning during execution
	"""
	print(f"\033[38;2;202;254;1m\033[48;2;0;0;0m !!! \033[38;2;0;0;0m\033[48;2;202;254;1m {warning_str} \033[0m")


def _help() -> None:
	"""
	Display help text to stdout
	"""
	print("\n\t\033[38;2;0;0;0m\033[48;2;202;254;1m [tkml help]                                         \033[0m\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌ VERSION [0.0.1 in-dev]                            ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌ AUTHORS [NateMount, DeadPixil]                    ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌ \033[38;2;0;0;0m\033[48;2;202;254;1m Usage \033[38;2;202;254;1m\033[48;2;0;0;0m ./tkml command path [flags]               ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌ \033[38;2;0;0;0m\033[48;2;202;254;1m[ Commands ]\033[38;2;202;254;1m\033[48;2;0;0;0m                                      ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌        run - live runs the tkml code in the tkml  ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌              interpreter                          ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌     render - creates a python executable file     ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌              from tkml source file                ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌    compile - creates a windows executable file    ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌              from tkml sourve file                ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌      debug - debugs a tkml source file            ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌ \033[38;2;0;0;0m\033[48;2;202;254;1m[ Flags ]\033[38;2;202;254;1m\033[48;2;0;0;0m                                         ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌       form - sets format of tkml file             ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌              [yaml / xml / json]                  ▐\n\t\033[38;2;202;254;1m\033[48;2;0;0;0m▌                                                   ▐\n\t\033[38;2;0;0;0m\033[48;2;202;254;1m                                          [end help] \033[0m\n")
	sys.exit()

def _read(path:str):
	"""
	Used to read file into memory
	@param path: path to file to read
	"""
	
	try:
		if 'yaml' in sys.argv:
			return yaml.load(open(path, 'r'), Loader=yaml.FullLoader)
		elif 'json' in sys.argv:
			return json.load(open(path, 'r'))
		else:
			return {'init': {'loadframe':'_'}}
	except FileNotFoundError:
		_warn("File does not exist")
		sys.exit()
