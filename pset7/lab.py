#!/usr/bin/env python3
"""6.009 Lab 7: carlae Interpreter"""

import doctest
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
	prod = 1
	for i in lis:
		prod *= i
	return prod

def div(lis):
	quo = lis[0]
	for i in lis[1:]:
		quo /= i
	return quo

carlae_builtins = {
	'+': sum,
	'-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
	'*': mult, 
	'/': div
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
		if len(pa) != len(self.params):
			raise EvaluationError
		e = Environments(self.parent)
		for i in range(len(pa)):
			e[self.params[i]] = pa[i]
		return evaluate(self.expr, e)

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

	# not list
	if not isinstance(tree, list):
		# handles variables
		if isinstance(tree, str):
			if tree in environment:
				return environment[tree]
			if tree in carlae_builtins:
				return carlae_builtins[tree]
			else:
				raise NameError
		# handles returning single numbers
		else:
			return tree
	# list (else)
	# is a defined function
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
	pass
	# uncommenting the following line will run doctests from above
	# doctest.testmod()
	# e = Environments(Carlae)
	# inp = ''
	# while (inp != 'QUIT'):
	#     inp = input("Input: ")
	#     print(">>>", inp)
	#     inp_new = parse(tokenize(inp))
	#     print("Output:", evaluate(inp_new, e))
	E = Environments()
	trees = ["(define (call x) (x))", "(call (lambda () 2))"]

	# (call (lambda () 2))
	# (define (spam) (call (lambda () 2)))
	# (call spam)
	# (call call)
	# (call)

	for t in trees:
		# print("T", t)
		t = tokenize(t)
		print("TOKEN", t)
		t = parse(t)
		# print("PARSE", t)
		print("EV", evaluate(t, E))
		print()
