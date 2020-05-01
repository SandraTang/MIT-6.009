#!/usr/bin/env python3
"""6.009 Lab 7: carlae Interpreter"""

import doctest
import sys
# NO ADDITIONAL IMPORTS!

class EvaluationError(Exception):
	"""
	Exception to be raised if there is an error during evaluation other than a
	NameError.
	"""
	pass

def tokenize(source):
	"""
	Splits an input string into meaningful tokens (left parens, right parens,
	other whitespace-separated values).  Returns a list of strings.

	Arguments:
		source (str): a string containing the source code of a carlae
					  expression
	"""
	lines = source.splitlines()
	new = pre = ''
	chars = ('(', ')', ' ')
	for line in lines:
		new += ' '
		for c in line:
			if c == ';':
				break
			if c in chars:
				new += pre
				pre = ''
				new += ' ' + c + ' '
			else:
				pre += c
		new += pre
		pre = ''
	new += pre
	return new.split()

def parse(tokens):
	"""
	Parses a list of tokens, constructing a representation where:
		* symbols are represented as Python strings
		* numbers are represented as Python ints or floats
		* S-expressions are represented as Python lists

	Arguments:
		tokens (list): a list of strings representing tokens
	"""
	if tokens.count('(') != tokens.count(')'):
		raise SyntaxError
	def convert(thing):
		try:
			return int(thing)
		except:
			try:
				return float(thing)
			except:
				return thing
	def parse_expression(index):
		# if first item is not '(' then must be standalone int, float, or var
		if tokens[index] == ')':
			raise SyntaxError
		if tokens[index] != '(':
			return (convert(tokens[index]), index+1)
		else:
			result = []
			# start past first '('
			index += 1
			end = index
			while tokens[index] != ')':
				s, end = parse_expression(index)
				result.append(s)
				index = end
				if tokens[index] == ')':
					break
				if index >= len(tokens):
					raise SyntaxError
			return (result, end+1)
	exp, e = parse_expression(0)
	if e == len(tokens):
		return exp
	else:
		raise SyntaxError

def mult(lis):
	"""
	Given a list. 
	Multiplies numbers in list. 
	Returns product. 
	"""
	prod = 1
	for i in lis:
		prod *= i
	return prod

def div(lis):
	"""
	Given list. 
	Divides first number by subsequent numbers. 
	Returns quotient. 
	"""
	quo = lis[0]
	for i in lis[1:]:
		quo /= i
	return quo

def car(X):
	"""
	Given list containing Pair object. 
	Returns first number of Pair object. 
	Raises Evaluation Error if item is not a Pair object. 
	"""
	try:
		return X[0].car
	except:
		raise EvaluationError

def cdr(X):
	"""
	Given list containing Pair object. 
	Returns cdr of Pair object. 
	Raises Evaluation Error if item is not a Pair object. 
	"""
	try:
		return X[0].cdr
	except:
		raise EvaluationError

def cons(lis):
	"""
	Given a list of two values. 
	Returns a Pair object. 
	"""
	c1 = evaluate(lis[0])
	c2 = evaluate(lis[1])
	p = Pair(c1, c2)
	return p

def list_function(lis):
	"""
	Given a list of values. 
	Returns a linked list (Pair object) holding those values. 
	"""
	result = None
	lis.reverse()
	for item in lis:
		result = Pair(item, result)
	return result

def length(lis):
	"""
	Given list containing Pair object. 
	Returns length of linked list the Pair object represents. 
	"""
	try:
		count = 0
		thing = lis[0]
		while thing != None:
			count += 1
			thing = thing.cdr
		return count
	except: # not a linked list, not Pair
		raise EvaluationError

def element_at_index(inp):
	"""
	Given list contining Pair object and index. 
	Returns value at given index. 
	"""
	lis = inp[0]
	index = inp[1]
	i = 0
	middleman = lis
	while i < index:
		middleman = middleman.cdr
		i += 1
	return middleman.car

def copier(lis):
	"""
	Creates copies of lists. 
	"""
	if cdr([lis]) == None:
		return cons([car([lis]), cdr([lis])])
	return cons([car([lis]), copier(cdr([lis]))])

def concat(lists):
	"""
	Given list of Pair objects. 
	Returns one Pair object representing all values in given Pair objects. 
	"""
	# edge cases - no lists or all lists None
	if len(lists) == 0 or all(lis == None for lis in lists):
		return None
	# filter out None lists
	valid_lists = [lis for lis in lists if lis != None]
	# valid lists here on out
	copied_lists = [copier(lis) for lis in valid_lists]
	# concatenate
	lis_num = 0
	current = copied_lists[lis_num]
	while lis_num < len(copied_lists)-1:
		while cdr([current]) != None:
			current = cdr([current])
		# cdr = None
		lis_num += 1
		current.cdr = copied_lists[lis_num]
		current = current.cdr
	return copied_lists[0]

def map_function(items):
	"""
	Takes function and list. 
	Returns NEW list containing results of applying given function to each element of given list. 
	"""
	func = items[0]
	lis = items[1]
	if lis == None:
		return None
	copied_lis = copier(lis)
	current = copied_lis
	while current != None:
		current.car = func([current.car])
		current = cdr([current])
	return copied_lis

def filt(items):
	"""
	Takes function and list. 
	Returns NEW list containing only TRUE elements. 
	"""
	# not getting first num
	func = items[0]
	lis = items[1]
	if lis == None:
		return None
	copied_lis = copier(lis)
	current = copied_lis
	while copied_lis != None and not func(copied_lis.car):
		copied_lis = copied_lis.cdr
	while current != None:
		if current.cdr != None and not func(current.cdr.car):
			current.cdr = current.cdr.cdr
		else:
			current = cdr([current])
	return copied_lis

def reduc(items):
	"""
	Propogates function throughout list. 
	"""
	# print(items)
	func = items[0]
	lis = items[1]
	initval = items[2]
	if lis == None:
		return initval
	if cdr([lis]) == None:
		return func([initval, lis.car])
	return reduc([func, cdr([lis]), func([initval, lis.car])])

def begin(lis):
	"""
	Input: List of expressions. 
	Output: Reuslt of last expression. 
	"""
	return evaluate(lis[-1])

carlae_builtins = {
	'+': sum,
	'-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
	'*': mult, 
	'/': div, 
	'=?': lambda lis: all(item == lis[0] for item in lis), 
	'>': lambda lis: all(lis[i-1] > lis[i] for i in range(1, len(lis))), 
	'>=': lambda lis: all(lis[i-1] >= lis[i] for i in range(1, len(lis))),
	'<': lambda lis: all(lis[i-1] < lis[i] for i in range(1, len(lis))),
	'<=': lambda lis: all(lis[i-1] <= lis[i] for i in range(1, len(lis))),
	'not': lambda lis: not lis[0],
	'#t': True, 
	'#f': False, 
	'car': car,
	'cdr': cdr,
	'cons': cons,
	'nil': None, #is this ok? 
	'list': list_function,
	'length': length,
	'elt-at-index': element_at_index, 
	'concat': concat,
	'map': map_function,
	'filter': filt,
	'reduce': reduc,
	'begin': begin
}

class Environments:
	def __init__(self, parent = None, variables = None):
		self.parent = parent
		if variables == None:
			self.variables = {}
		else:
			self.variables = variables
	def __setitem__(self, key, value):
		self.variables[key] = value
	def __getitem__(self, key):
		if key in self.variables.keys():
			return self.variables[key]
		elif self.parent != None:
			# go to parent environment
			return self.parent[key]
		else: #parent == None
			raise NameError
	def __delitem__(self, key):
		del self.variables[key]
	def __contains__(self, key):
		if self.parent != None:
			return key in self.variables.keys() or key in self.parent
		else:
			return key in self.variables.keys()
	def in_which_environment(self, key):
		if key in self.variables.keys():
			return self
		else:
			return self.parent.in_which_environment(key)
	def __iter__(self):
		for key, value in self.variables.items():
			yield key, value

Carlae = Environments(None)
Carlae.variables = carlae_builtins

class Functions:
	def __init__(self, params, expr, parent = Carlae):
		self.params = params
		self.expr = expr
		self.parent = parent
	def __call__(self, pa):
		if not isinstance(pa, list):
			pa = [pa]
		if len(pa) != len(self.params):
			raise EvaluationError
		e = Environments(self.parent)
		for i in range(len(pa)):
			e[self.params[i]] = pa[i]
		return evaluate(self.expr, e)

class Pair: # aka cell
	def __init__(self, car, cdr):
		self.car = car
		self.cdr = cdr

def evaluate_file(file, environment = None):
	if environment is None:
		environment = Environments(Carlae)
	# read and split into lines
	f = open(file, 'r')
	t = f.read()
	f.close()
	# evaluate
	t = tokenize(t)
	t = parse(t)
	return evaluate(t, environment)

def evaluate(tree, environment = None):
	"""
	Evaluate the given syntax tree according to the rules of the carlae
	language.

	Arguments:
		tree (type varies): a fully parsed expression, as the output from the
							parse function
	"""
	# print("TREE", tree)
	# print(tree, environment, environment.variables)
	# default environment
	if environment is None:
		environment = Environments(Carlae)

	# not list, handles variables
	if not isinstance(tree, list):
		if isinstance(tree, str):
			if tree in environment:
				return environment[tree]
			if tree in carlae_builtins:
				return carlae_builtins[tree]
			else:
				raise NameError
		else: # handles returning single numbers
			return tree
	# list (else) is a defined function
	if tree[0] == 'define':
		if len(tree) != 3:
			raise EvaluationError
		if isinstance(tree[1], list):
			f = Functions(tree[1][1:], tree[2], environment)
			environment[tree[1][0]] = f
			return environment[tree[1][0]]
		else:
			environment[tree[1]] = evaluate(tree[2], environment)
			return environment[tree[1]]
	elif tree[0] == 'lambda':
		f = Functions(tree[1], tree[2], environment)
		return f
	elif tree[0] == 'if':
		cond = evaluate(tree[1], environment)
		if cond:
			return evaluate(tree[2], environment)
		else:
			return evaluate(tree[3], environment)
	elif tree[0] == 'and':
		for index, item in enumerate(tree[1:]):
			if evaluate(tree[index+1], environment) == False:
				return False
		return True
	elif tree[0] == 'or':
		for index, item in enumerate(tree[1:]):
			if evaluate(tree[index+1], environment) == True:
				return True
		return False
	elif tree[0] == 'let':
		# assignment
		params = [item[0] for item in tree[1]]
		values = [item[1] for item in tree[1]]
		body = tree[2]
		# evaluate values
		ev_vals = []
		for val in values:
			ev_vals.append(evaluate(val, environment))
		# create and use function
		f = Functions(params, body, environment)
		return f(ev_vals)
	elif tree[0] == 'set!':
		var = tree[1]
		exp = evaluate(tree[2], environment)
		if var not in environment:
			raise NameError
		e = environment.in_which_environment(var)
		e[var] = exp
		return exp
	else:
		try:
			new_tree = []
			for index, item in enumerate(tree[1:]):
				new_tree.append(evaluate(tree[index+1], environment))
			return evaluate(tree[0], environment)(new_tree)
		except NameError:
			raise NameError
		except:
			raise EvaluationError
	# return result

def result_and_env(tree, environment = None):
	if environment is None:
		environment = Environments(Carlae)
	return (evaluate(tree, environment), environment)

if __name__ == '__main__':
	# code in this block will only be executed if lab.py is the main file being
	# run (not when this module is imported)

	# data = tokenize(parse(sys.argv))
	# for d in data[1:]:
	# 	evaluate_file(d)

	# uncommenting the following line will run doctests from above
	# doctest.testmod()

	# e = Environments(Carlae)
	# inp = ''
	# while (inp != 'QUIT'):
	#     inp = input("Input: ")
	#     inp_new = parse(tokenize(inp))
	#     print("Output:", evaluate(inp_new, e))

	E = Environments()
	trees = [
	'(define y 10)', 
	'y', 
	'((lambda (z) (set! y (+ z y))) 9)', 
	'y', 
	'((lambda (z) (set! x (+ z y))) 9)', 
	'x'
	]
	for t in trees:
		# print("T", t)
		t = tokenize(t)
		# print("TOKEN", t)
		t = parse(t)
		# print("PARSE", t)
		thing = evaluate(t, E)
		print("EV", thing)
		try:
			while thing != None:
				print(thing.car)
				thing = thing.cdr
		except:
			print()
		print()
