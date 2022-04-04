#! /usr/bin/env python3.10

import sys
from tkinter import *
from .util import _read, _warn

def run(path:str) -> None:
	"""Used to live run a tkml file"""
	
	if not (data := _read(path)):
		_warn("No data recovered")
		sys.exit()

	try:
		frame:str = _win_init(data)
	except KeyError:
		_warn("No loadframe found")
		sys.exit()

	if not root:
		_warn("Root not initialized")
		sys.exit()

	_win_loadframe(data, frame)
	_win_main()


def _win_init(data:dict) -> None:
	"""Initializes the tkinter window environment"""

	globals()['root'] = Tk()

	try:
		data['init']
	except KeyError:
		_warn("Init not found")
		sys.exit()
	
	_screen_x:int = root.winfo_screenwidth()
	_screen_y:int = root.winfo_screenheight()

	_win_y:int = 500
	_win_x:int = 500
	_win_pos_x:int = int(_screen_x/2 - 250)
	_win_pos_y:int = int(_screen_y/2 - 250)

	_win_title:str = 'My App'
	_win_bg:str = '#000000'

	_win_scale_x:bool = True
	_win_scale_y:bool = True

	_win_max_x:int = 1200
	_win_max_y:int = 1200
	_win_min_x:int = 300
	_win_min_y:int = 300

	_win_icon:str = None

	if len(data['init']) != 0:
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
				case 'icon':
					_win_icon = data['init']['icon']
				case 'bg':
					_win_bg = data['init']['bg']
	
	#Setting root window attributes
	root.title(_win_title)
	root.geometry(f"{_win_x}x{_win_y}+{_win_pos_x}+{_win_pos_y}")
	root.resizable(_win_scale_x, _win_scale_y)
	root.minsize(_win_min_x,_win_min_y)
	root.maxsize(_win_max_x,_win_max_y)
	if _win_icon:
		root.iconbitmap(_win_icon)
	root.configure(bg=_win_bg)

	#Returning name of first frame to be loaded
	return data['init']['loadframe']


def _win_loadframe(data:dict, frame:str) -> None:
	"""Loads a frame to be rendered"""

	try:
		data[frame]
	except KeyError:
		_warn("Frame ["+frame+"] not found")
		return

	for _c in root.winfo_children():
		_c.destroy()

	for _w in data[frame]:
		_w_master = root if 'master' not in _w else _w['master']

		_w_pos_x, _w_pos_y = ((root.winfo_screenwidth()//2),(root.winfo_screenheight()//2)) if 'pos' not in _w else map(int, data[frame][_w]['pos'].split('x'))
		_w_pad_x, _w_pad_y = (0,0) if 'pad' not in _w else map(int, data[frame][_w]['pad'].split('x'))

		#TODO filter and modify parameters given to widgets

		try:
			globals()[_w] = globals()[data[frame][_w]['type']](_w_master, **{_k: data[frame][_w][_k] for _k in data[frame][_w] if _k in ('text', 'bg', 'fg')})
			globals()[_w].grid(row=_w_pos_y, column=_w_pos_x)
		except KeyError:
			_warn("No type given for widget")
			continue


def _win_main(events:tuple = ()) -> None:
	"""Initialize the mainloop of window"""
	while True:
		#Update main window view
		root.update()

		#For any user defined events call them now
		for _e in events:
			_e()

