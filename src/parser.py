#! /usr/bin/env python3.10

# TKML Parser Info
# Parser works in a new approach to xml style syntax
# Each line of code is a function or parameter to that function
# It is expected that any external functions will be defined in the pre-proc header
#
# Example:
#
# <funct param1 param2=val>
#
# Or
#
# <funct>
#	param1
#	param2: val
# </funct>

import re

class Node:

	### Object Creation Methods

	def __init__(self, id:str, *data):
		self.n:list = []
		self.d:list = list(data) or []
		self.i:str = id

	### Object Update Methods

	def __add__(self, other):
		if type(other) == type(self) and other != self:
			self.n.append(other)

	# TODO Fix removal method
	def __sub__(self, other):
		if other.i in [ _n.i for _n in self.n]:
			self.n.remove(other)

	def __matmul__(self, other):
		if type(other) == type(self):
			for _n in other.n:
				if _n not in self.n:
					self.n.append(_n)
		else:
			return NotImplemented

	### Access Methods

	def __getitem__(self, key:str):
		return self._find_by_id(key)
	
	def __call__(self, key:str):
		return self._find_by_data(key)
	
	### Misc Methods

	def __len__(self):
		return len(self.n)
	
	def __contains__(self, key):
		return key in self.d
	
	def __str__(self):
		return f"{self.i} [ {self.d} ]"
	
	# NOTE look into __iter__ and __next__ methods

	### Internal Methods


	#TODO Need to fix find methods
	def _find_by_id(self, id:str):
		if id == self.i:
			return self
		for _n in self.n:
			_t = _n._find_by_id(id)
			if _t:
				return _t
		return None
	
	def _find_by_data(self, data):
		if data in self.d:
			return self
		for _n in self.n:
			_t = _n._find_by_data(data)
			if _t:
				return _t
		return None
	
	def _get_heirarchy(self):

		if len(self.n) == 0:
			return {'data':self.d}

		return {self.i: { _n.i: _n._get_heirarchy() for _n in self.n }}.update({'data': self.d})



