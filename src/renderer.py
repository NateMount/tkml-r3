#! /usr/bin/env python3.10

import os, sys
from .util import _read, _warn, _debug

def render(path:str, form:str) -> None:
	"""Generates an executable file from tkml source file"""
	
	_debug("FUNCTION [_render] CALLED")

	if not (_data := _read(path)):
		_warn("No data recovered from file")
		sys.exit()

	_debug(f"DATA : {_data}")

	if 'init' not in _data:
		_warn("Init frame not found")
		sys.exit()
	

	match form:
		case 'html':
			_rend_html(_data)
		case 'cli':
			_rend_cli(_data)
		case 'rui':
			_rend_rui(_data)
		case _:
			_warn("Unrecognized rendering format")
