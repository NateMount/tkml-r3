#! /usr/bin/env python3.10

import sys
from tkinter import *
from .util import _read, _warn

WIDGETS = {'Button', 'Label', 'Canvas', 'Frame', 'Scrollbar', 'LabelFrame', 'CheckButton', 'Entry', 'Spinbox', 'Scale', 'PanedWindow', 'Menu', 'Menubutton', 'Notebook', 'Combobox', 'Progressbar', 'Seperator', 'Sizegrip', 'Treeview'}

def run(path:str) -> None:
	"""Live runs tkml app on top of tkml interpreter"""

	if not (_data := _read(path)):
		_warn("No data recovered from file")
		sys.exit()

	if 'init' not in _data:
		_warn("Init frame not found")
		sys.exit()

	_win_load_configs(_data)

	_win_init(_data)
	
	if 'loadframe' in _data['init']:
		_win_loadframe(_data, _data['init']['loadframe'])
	
	_win_main()


def _win_init(data:dict) -> None:
	"""Initialize the Tkinter window environment"""

	globals()['root'] = Tk()

	#Creating init var for simplicity
	_init:dict = data['init']

	#Getting user screen dimensions
	_screen_x:int = root.winfo_screenwidth()
	_screen_y:int = root.winfo_screenheight()

	#Retriving window properties
	_win_title:str = 'App' if 'title' not in _init else _init['title']	
	_win_x, _win_y = (500, 500) if 'dim' not in _init else map(int, _init['dim'].split('x'))
	_win_pos_x, _win_pos_y = (_screen_x//2 - _win_x//2, _screen_y//2 - _win_y//2)
	_win_bg = '#000000' if 'bg' not in _init else _init['bg']
	_win_scale_x, _win_scale_y = (True, True) if 'scale' not in _init else map(bool, _init['scale'].split())
	_win_max_x, _win_max_y = (1200, 1200) if 'max' not in _init else map(int, _init['max'].split('x'))
	_win_min_x, _win_min_y = (300, 300) if 'min' not in _init else map(int, _init['min'].split('x'))
	_win_icon_path:str = None if 'icon' not in _init else _init['icon']

	#Setting root window attributes
	root.title(_win_title)
	root.geometry(f"{_win_x}x{_win_y}+{_win_pos_x}+{_win_pos_y}")
	root.resizable(_win_scale_x, _win_scale_y)
	root.minsize(_win_min_x,_win_min_y)
	root.maxsize(_win_max_x,_win_max_y)

	if _win_icon_path:
		root.iconbitmap(_win_icon_path)
	
	root.configure(bg=_win_bg)


def _win_load_configs(data:dict) -> None:
	"""Loads in data from configs header"""

	if 'configs' not in data:
		return
	
	if 'use' in data['configs']:
		for _module in data['configs']['use']:

			_win_load_module(_module)


def _win_clear() -> None:
	"""Clears current window state of all widgets"""

	[_c.destroy() for _c in root.winfo_children() if _c]


def _win_mod_params(widget:str, params:dict) -> dict:
	"""Modifies the types of the params to match types for Tkinter"""

	#TODO Implement vetting for parameters

	return params


def _win_render_widget(data:dict) -> Widget:
	"""Renders a widget from given data"""

	if 'type' not in data:
		_warn(f"Undefined widget type [{name}]")
		return None
	elif data['type'] not in WIDGETS:
		_warn(f"Illegal widget type")
		return None

	#Tuple of all universally legal parameters
	_legal:tuple = ('activebackground', 'activeforeground', 'anchor', 'background', 'bd', 'bg', 'bitmap', 'borderwidth', 'command', 'compound', 'cursor', 'default', 'disabledforeground', 'fg', 'font', 'foreground', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'image', 'justify', 'overrelief', 'padx', 'pady', 'relief', 'repeatdelay', 'repeatinterval', 'state', 'takefocus', 'text', 'textvariable', 'underline', 'width', 'wraplength', 'closeenough', 'confine', 'insertbackground', 'insertborderwidth', 'insertofftime', 'insertontime', 'insertwidth', 'offset', 'scrollregion', 'selectbackground', 'selectborderwidth', 'selectforeground', 'xscrollcommand', 'xscrollincrement', 'yscrollcommand', 'yscrollincrement', 'class', 'colormap', 'container', 'visual', 'activerelief', 'elementborderwidth', 'jump', 'orient', 'troughcolor', 'labelanchor', 'labelwidget', 'indicatoron', 'offrelief', 'offvalue', 'onvalue', 'selectcolor', 'selectimage', 'tristateimage', 'tristatevalue', 'variable', 'disabledbackground', 'exportselection', 'invalidcommand', 'invcmd', 'readonlybackground', 'show', 'validate', 'validatecommand', 'vcmd', 'buttonbackground', 'buttoncursor', 'buttondownrelief', 'buttonuprelief', 'format', 'from', 'increment', 'to', 'values', 'wrap', 'bigincrement', 'digits', 'label', 'length', 'resolution', 'showvalue', 'sliderlength', 'sliderrelief', 'tickinterval', 'handlepad', 'handlesize', 'opaqueresize', 'proxybackground', 'proxyborderwidth', 'proxyrelief', 'sashcursor', 'sashpad', 'sashrelief', 'sashwidth', 'showhandle', 'activeborderwidth', 'postcommand', 'tearoff', 'tearoffcommand', 'title', 'direction', 'menu', 'padding', 'style', 'mode', 'maximum', 'value', 'phase', 'columns', 'displaycolumns', 'selectmode')


	_w_params:dict = _win_mod_params(data['type'], {_k : data[_k] for _k in data if _k in _legal})
	_w_master = root if 'master' not in data else globals()[data['master']]

	return globals()[data['type']](_w_master, **_w_params)


def _win_loadframe(data:dict, frame:str) -> None:
	"""Loads a frame to be rendered"""

	try:
		data[frame]
	except KeyError:
		_warn(f"Frame [{frame}] not found")
		return
	
	_win_clear()

	for _w in data[frame]:
		
		_w_master = root if 'master' not in _w else _w['master']

		_w_pos_x, _w_pos_y = ((root.winfo_screenwidth()//2),(root.winfo_screenheight()//2)) if 'pos' not in _w else map(int, data[frame][_w]['pos'].split('x'))
		_w_pad_x, _w_pad_y = (0,0) if 'pad' not in _w else map(int, data[frame][_w]['pad'].split('x'))
		_w_span_x, _w_span_y = (1,1) if 'span' not in _w else map(int, data[frame][_w]['span'].split('x'))
		_w_align = "" if 'align' not in _w else data[frame][_w]['align'].upper()

		globals()[_w] = _win_render_widget(data[frame][_w])
		globals()[_w].grid(row=_w_pos_y, column=_w_pos_x, padx=_w_pad_x,pady=_w_pad_y, columnspan=_w_span_x, rowspan=_w_span_y, sticky=_w_align)


def _win_main(events:tuple = ()) -> None:
	"""Initialize the main window view"""
	while True:
		try:
			root.update()
		except TclError:
			sys.exit()

		[_e() for _e in events]
