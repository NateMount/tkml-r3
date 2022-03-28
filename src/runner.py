#! /usr/bin/env python3.10

import sys
from tkinter import *
from .util import _read, _warn

def run(path:str) -> None:
	"""Used to live run a tkml file"""
	
	data = _read(path)
	if not data:
		_warn("No data recovered")
		sys.exit()

	try:
		frame = _win_init()
	except KeyError:
		_warn("No loadframe found")
		sys.exit()

	if not root:
		_warn("Root not initialized, tkml core error")
		sys.exit()

	_win_loadframe(frame)


def _win_init() -> None:
	"""Initializes the tkinter window environment"""

	globals()['root'] = Tk()

	if 'init' not in data:
		_warn("Init not found ... terminating program")
		sys.exit()
	
	_screen_x:int = root.winfo_screenwidth()
	_screen_y:int = root.winfo_screenheight()

	_win_y:int = 500
	_win_x:int = 500
	_win_pos_x:int = _screen_x/2 - 250
	_win_pos_y:int = _screen_y/2 - 250

	_win_title:str = 'My App'

	_win_scale_x:bool = True
	_win_scale_y:bool = True

	_win_max_x:int = 600
	_win_max_y:int = 600
	_win_min_x:int = 400
	_win_min_y:int = 400

	_win_opacity:float = 1.0

	_win_icon:str = None

	for _flag in data['init']:
		match _flag:
			case 'title':
				_win_title = data['init']['title']
			case 'width':
				_win_x = int(data['init']['width'])
			case 'height':
				_win_y = int(data['init']['height'])
			case 'geo':
				_win_x, _win_y = map(int, data['init']['geo'].split('x'))
			case 'posX':
				_win_pos_x = int(data['init']['posX'])
			case 'posY':
				_win_pos_y = int(data['init']['posY'])
			case 'pos':
				_win_pos_x, _win_pos_y = map(int, data['init']['pos'].split('x'))
			case 'scaleX':
				_win_scale_x = bool(data['init']['scaleX'])
			case 'scaleY':
				_win_scale_y = bool(data['init']['scaleY'])
			case 'scale':
				_win_scale_x = bool(data['init']['scale'])
				_win_scale_y = bool(data['init']['scale'])
			case 'maxSizeX':
				_win_max_x = int(data['init']['maxSizeX'])
			case 'maxSizeY':
				_win_max_y = int(data['init']['maxSizeY'])
			case 'maxSize':
				_win_max_x, _win_max_y = map(int, data['init']['maxSize'].split('x'))
			case 'minSizeX':
				_win_min_x = int(data['init']['minSizeX'])
			case 'minSizeY':
				_win_min_y = int(data['init']['minSizeY'])
			case 'minSize':
				_win_min_x, _win_min_y = map(int, data['init']['minSize'].split('x'))
			case 'opacity':
				_win_opacity = float(data['init']['opacity'])
			case 'icon':
				_win_icon = data['init']['icon']
	
	root.title(_win_title)
	root.geometry(f"{_win_x}x{_win_y}+{_win_pos_x}+{_win_pos_y}")
	root.resizable(_win_scale_x, _win_scale_y)
	root.minsize(_win_min_x,_win_min_y)
	root.maxsize(_win_max_x,_win_max_y)
	root.attributes('-alpha',_win_opacity)
	if _win_icon:
		root.iconbitmap(_win_icon)
	
	return data['init']['loadframe']

def _win_loadframe(frame:str) -> None:
	"""Loads a frame to be rendered"""
	raise NotImplementedError
