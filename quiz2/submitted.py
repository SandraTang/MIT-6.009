import doctest

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################


def genseq(f, a, b):
	"""
	>>> fibseq = genseq(lambda a, b: a + b, 0, 1)
	>>> [next(fibseq) for _ in range(10)]
	[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
	>>> altseq = genseq(lambda a, b: a, 7, 8)
	>>> [next(altseq) for _ in range(10)]
	[7, 8, 7, 8, 7, 8, 7, 8, 7, 8]
	"""
	yield a
	yield b
	new_a = a
	new_b = b
	result = f(new_a, new_b)
	yield result
	while True:
		new_a = new_b
		new_b = result
		result = f(new_a, new_b)
		yield result


##################################################
#  Problem 2
##################################################


def feed(people, food):
	"""
	People is dictionary mapping name to food person is willing to eat. 
	Food is dictionary mapping food item to quantity. 

	>>> out1 = {'alice': 'pickles', 'bob': 'ketchup'}
	>>> feed({'alice': ['pickles'], 'bob': ['ketchup']},
	...      {'pickles': 1, 'ketchup': 1}) == out1
	True

	>>> feed({'alice': ['pickles'], 'bob': ['pickles']},
	...      {'pickles': 1, 'ketchup': 1}) == None
	True

	>>> out2 = {'alice': 'pickles', 'bob': 'pickles'}
	>>> feed({'alice': ['pickles'], 'bob': ['pickles']},
	...      {'pickles': 2, 'ketchup': 1}) == out2
	True

	>>> people = {'alice': ['pickles', 'ketchup'], 'bob': ['chips', 'onions'],
	...           'candace': ['pie', 'broccoli'],  'dave': ['pickles'],
	...           'emery': ['onions'], 'fergus': ['pie']}
	>>> foods = {'pickles': 1, 'ketchup': 1, 'chips': 1, 'onions': 1,
	...          'pie': 1, 'broccoli': 1}
	>>> expected = {'alice': 'ketchup', 'bob': 'chips', 'candace': 'broccoli',
	...             'dave': 'pickles', 'emery': 'onions', 'fergus': 'pie'}
	>>> feed(people, foods) == expected
	True

	>>> people = {'alice': ['cake', 'cheese', 'pie', 'sandwiches'],
	...           'bob': ['cake', 'cheese', 'pie'],
	...           'candace': ['cake', 'cheese'],
	...           'dave': ['cake', 'cheese'],
	...           'emery': ['cake', 'cheese']}
	>>> foods = {'cake': 2, 'cheese': 1, 'pie': 1, 'sandwiches': 1}
	>>> res = feed(people, foods)
	>>> res['alice'], res['bob']
	('sandwiches', 'pie')
	>>> sorted((res['candace'], res['dave'], res['emery']))
	['cake', 'cake', 'cheese']
	"""
	# passing doc test but not real tests
	# problem with all test cases that contain res
	# assign the obvious
	def obvious(current, eaten):
		hungry = [person for person in people.keys() if person not in current.keys()]
		for name in hungry:
			available = [dish for dish in people[name] if dish in food.keys() and food[dish] - eaten[dish] > 0]
			if len(available) == 0:
				return None
			if len(available) == 1:
				dish = available[0]
				eaten[dish] += 1
				current[name] = dish
		return (current, eaten)
	# reduce logically until can't (need to guess)
	# setup
	assignments = {} # people : food
	food_eaten = {} # food : quantity eaten
	for item in food.keys():
		food_eaten[item] = 0
	prev = len(assignments)
	obvious(assignments, food_eaten)
	# while nothing new is assigned
	while prev != len(assignments):
		prev = len(assignments)
		result = obvious(assignments, food_eaten)
		if result == None:
			return None
	return assignments
	# guess
	# [{dict of current assignments}, {dict of food eaten : quantitiy eaten}]
	agenda = [[assignments, food_eaten]]
	while agenda:
		situation = agenda.pop()
		current = situation[0]
		eaten = situation[1]
		# base case
		if current.keys() == people.keys():
			return current #assignments
		# for each unassigned person, try new situation
		hungry = [person for person in people.keys() if person not in current.keys()]
		for name in hungry:
			# for each preferred and available dish
			available = [dish for dish in people[name] if dish in food.keys() and food[dish] - eaten[dish] > 0]
			for dish in available:
				# duplicate current
				new_current = {}
				for k, v in current.items():
					new_current[k] = v
				# duplicate eaten
				new_eaten = {}
				for k, v in eaten.items():
					new_eaten[k] = v
				# assign new current
				new_current[name] = dish
				# assign new eaten
				new_eaten[dish] += 1
				# add new situation to agenda
				agenda.append([new_current, new_eaten])

##################################################
#  Problem 3
##################################################


class Verbatim:
	"""
	Matches the given string, verbatim.
	"""
	def __init__(self, string):
		self.string = string

	def match(self, text, start_index=0):
		# return a tuple (start, end, matched_text)
		substr = text[start_index:]
		for i in range(len(self.string)):
			if i >= len(substr) or self.string[i] != substr[i]:
				return None
		return (start_index, start_index + len(self.string), self.string)


class Dot:
	"""
	Matches any single character in a piece of text.
	"""
	def match(self, text, start_index=0):
		if start_index >= len(text):
			return None
		return (start_index, start_index+1, text[start_index])


class CharFrom:
	"""
	Matches any single character from the given iterable object of characters.
	"""
	def __init__(self, chars):
		self.chars = chars

	def match(self, text, start_index=0):
		if start_index >= len(text):
			return None
		if text[start_index] in self.chars:
			return (start_index, start_index+1, text[start_index])
		return None


class CharNotFrom:
	"""
	Matches any single character _not_ contained in the given iterable object.
	"""
	def __init__(self, chars):
		self.chars = chars

	def match(self, text, start_index=0):
		if start_index >= len(text):
			return None
		if text[start_index] not in self.chars:
			return (start_index, start_index+1, text[start_index])
		return None


class Sequence:
	"""
	Matches only if the given patterns all occur in order.  Patterns is given
	as a list of instances of one of these classes.
	"""
	def __init__(self, patterns):
		self.patterns = patterns

	def match(self, text, start_index=0):
		result = None
		new_start = start_index
		# run each matching function
		for p in self.patterns:
			if result != None:
				end = result[1]
				new_start = end
			result = p.match(text, new_start)
		if result == None:
			return None
		else:
			# wasn't clear exactly what the function should return
			return (start_index, end+1, text[start_index:end+1])


class Alternatives:
	"""
	Matches if _any_ of the given patterns match, by trying them in the order
	they were given.
	"""
	def __init__(self, patterns):
		self.patterns = patterns

	def match(self, text, start_index=0):
		for p in self.patterns:
			result = p.match(text, start_index)
			if result != None:
				return result
		return None


class Repeat:
	"""
	Matches if the given pattern (given as an instance of one of these classes)
	exists repeated between n_min (inclusive) and n_max (inclusive) times.
	This matching should be greedy (i.e., it should match as many repetitions
	as possible up to `n_max` times).  It should not match if there are fewer
	than `n_min` repetitions.
	"""
	def __init__(self, pattern, n_min, n_max):
		self.p = pattern
		self.n = n_min
		self.m = n_max

	def match(self, text, start_index=0):
		result = self.p.match(text, start_index)
		num = 0
		while result != None and num < self.m:
			num += 1
			prev = result
			start = start_index + 1
			result = self.p.match(text, start)
		end = prev[1]
		if num < self.n:
			return None
		return (start_index, end, text[start_index:end])


class Star:
	"""
	Matches the given pattern (an instance of one of these classes) repeated an
	arbitrary number of times.  0 times (matching the empty string) is a valid
	match.
	"""
	def __init__(self, pattern):
		self.p = pattern

	def match(self, text, start_index=0):
		result = self.p.match(text, start_index)
		# while result != None:
		# 	prev = result
		# 	start = start_index + 1
		# 	result = self.p.match(text, start)
		# end = prev[1]
		# return (start_index, end, text[start_index:end])


if __name__ == "__main__":
	doctest.testmod()
