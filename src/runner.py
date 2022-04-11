#! /usr/bin/env python3.10

import os, sys
from tkinter import *
from .util import _read, _warn, _debug

WIDGETS = {
	'Button',
	'Label',
	'Canvas',
	'Frame',
	'Scrollbar',
	'LabelFrame',
	'CheckButton',
	'Entry',
	'Spinbox',
	'Scale',
	'PanedWindow',
	'Menu',
	'Menubutton',
	'Notebook',
	'Combobox',
	'Progressbar',
	'Seperator',
	'Sizegrip',
	'Treeview'
}

def run(path:str) -> None:
	"""
	Live runs tkml app on top of tkml interpreter
	@param path: path to tkml file to be run
	"""

	_debug("FUNCTION [_run] CALLED")

	if not (_data := _read(path)):
		_warn("No data recovered from file")
		sys.exit()
	
	_debug(f"DATA : {_data}")

	if 'init' not in _data:
		_warn("Init frame not found")
		sys.exit()

	_win_load_configs(_data)
	_win_init(_data)
	
	if 'loadframe' in _data['init']:
		_win_loadframe(_data, _data['init']['loadframe'])
	
	_events = {} if 'events' not in _data else _data['events']
	
	_debug(f"EVENTS : {_events}")

	_win_main(_events)


def _win_init(data:dict) -> None:
	"""
	Initialize the Tkinter window environment
	@param data: dictionary containing frame structure data
	@post: global variable root created
	"""

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

	_debug("WINDOW INITIALIZED")


def _win_load_module(module:str) -> None:
	"""
	Loads in important data from module
	@param module: Name of module to be loaded for execution
	@post: module custom widgets added to widgets list 
	"""

	if module not in (*os.listdir(), *os.listdir('./modules')):
		_warn(f"Module [{module}] not found")
		return
	
	_module_data = open(module, 'r').read()
	exec(_module_data)
	for line in _module_data.split('\n'):
		if line.startswith('def WIDGET_'):
			globals()['WIDGETS'].append(line.split('WIDGET_')[-1].split('(')[0].strip())


def _win_load_configs(data:dict) -> None:
	"""
	Loads in data from configs header
	@param data: dictionary containing frame structure data
	@post: config data added to global namespace
	"""

	if 'configs' not in data:
		return
	
	if 'use' in data['configs']:
		for _module in data['configs']['use']:

			_win_load_module(_module)


def _win_clear() -> None:
	"""
	Clears current window state of all widgets
	@post: all children of root destroyed
	"""
	_debug("WINDOW CLEARED")
	[_c.destroy() for _c in root.winfo_children() if _c]


def _win_render_widget(data:dict) -> Widget:
	"""
	Renders a widget from given data
	@param data: dictionary containing data for widget
	@return: widget built from passed params
	"""

	if 'type' not in data:
		_warn(f"Undefined widget type [{name}]")
		return None
	elif data['type'] not in WIDGETS:
		_warn(f"Illegal widget type")
		return None

	#Tuple of all universally legal parameters
	_legal:tuple = ('activebackground', 'activeforeground', 'anchor', 'background', 'bd', 'bg', 'bitmap', 'borderwidth', 'command', 'compound', 'cursor', 'default', 'disabledforeground', 'fg', 'font', 'foreground', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'image', 'justify', 'overrelief', 'padx', 'pady', 'relief', 'repeatdelay', 'repeatinterval', 'state', 'takefocus', 'text', 'textvariable', 'underline', 'width', 'wraplength', 'closeenough', 'confine', 'insertbackground', 'insertborderwidth', 'insertofftime', 'insertontime', 'insertwidth', 'offset', 'scrollregion', 'selectbackground', 'selectborderwidth', 'selectforeground', 'xscrollcommand', 'xscrollincrement', 'yscrollcommand', 'yscrollincrement', 'class', 'colormap', 'container', 'visual', 'activerelief', 'elementborderwidth', 'jump', 'orient', 'troughcolor', 'labelanchor', 'labelwidget', 'indicatoron', 'offrelief', 'offvalue', 'onvalue', 'selectcolor', 'selectimage', 'tristateimage', 'tristatevalue', 'variable', 'disabledbackground', 'exportselection', 'invalidcommand', 'invcmd', 'readonlybackground', 'show', 'validate', 'validatecommand', 'vcmd', 'buttonbackground', 'buttoncursor', 'buttondownrelief', 'buttonuprelief', 'format', 'from', 'increment', 'to', 'values', 'wrap', 'bigincrement', 'digits', 'label', 'length', 'resolution', 'showvalue', 'sliderlength', 'sliderrelief', 'tickinterval', 'handlepad', 'handlesize', 'opaqueresize', 'proxybackground', 'proxyborderwidth', 'proxyrelief', 'sashcursor', 'sashpad', 'sashrelief', 'sashwidth', 'showhandle', 'activeborderwidth', 'postcommand', 'tearoff', 'tearoffcommand', 'title', 'direction', 'menu', 'padding', 'style', 'mode', 'maximum', 'value', 'phase', 'columns', 'displaycolumns', 'selectmode')


	_w_params:dict = {_k : data[_k] for _k in data if _k in _legal}
	_debug(f"WIDGET PARAMS {_w_params}")
	_w_master = root if 'master' not in data else globals()[data['master']]

	return globals()[data['type']](_w_master, **_w_params)


def _win_loadframe(data:dict, frame:str) -> None:
	"""
	Loads a frame to be rendered
	@param data: dictionary containing frame structure data
	@param frame: name of frame to be loaded
	"""

	try:
		data[frame]
	except KeyError:
		_warn(f"Frame [{frame}] not found")
		return
	
	_win_clear()

	for _w in data[frame]:
		
		_debug(f"LOADING WIDGET : [{_w}]")
		_debug(f"WIDGET DATA: ", data[frame][_w])
		_w_master = root if 'master' not in _w else _w['master']

		_w_pos_x, _w_pos_y = (0,0) if 'pos' not in data[frame][_w] else map(int, data[frame][_w]['pos'].split('x'))
		_w_pad_x, _w_pad_y = (0,0) if 'pad' not in data[frame][_w] else map(int, data[frame][_w]['pad'].split('x'))
		_w_span_x, _w_span_y = (1,1) if 'span' not in data[frame][_w] else map(int, data[frame][_w]['span'].split('x'))
		_w_align = "" if 'align' not in data[frame][_w] else data[frame][_w]['align'].upper()

		_debug(f"WIDGET MASTER [{_w_master}]")
		_debug(f"WIDGET POS [{_w_pos_x}][{_w_pos_y}]")
		globals()[_w] = _win_render_widget(data[frame][_w])
		globals()[_w].grid(row=_w_pos_y, column=_w_pos_x, padx=_w_pad_x,pady=_w_pad_y, columnspan=_w_span_x, rowspan=_w_span_y, sticky=_w_align)

	_debug("FRAME LOADED")


def _win_main(events:dict) -> None:
	"""
	Initialize the main window view
	@param events: Optional dict parameter containing function objects to be called each tick
		       Keys are function names 
		       Values are function parameters
	"""

	while True:
		try:
			root.update()
		except TclError:
			sys.exit()

		[globals()[_e](**events[_e]) for _e in events]
