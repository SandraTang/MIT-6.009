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


def feed(people, food, curren = None):
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
	# RESUBMISSION COMMENT - WHAT WAS WRONG WITH MY ORIGINAL SOLUTION
	# My original solution attempted to use DFS (Depth First Search)
	# instead of backtracking, the current solution, which is much
	# more efficient. Also, there were problems with dictionary keys
	# not existing. My new solution avoids that problem by creating
	# copies of current and food so that I can safely alter the data.

	if curren == None:
		current = {}
	else:
		current = curren.copy()
	# base case
	if current.keys() == people.keys():
		return current
	# copy food
	foo = food.copy()
	# simplify
	def obvious(curr):
		hungry = [person for person in people.keys() if person not in curr.keys()]
		for name in hungry:
			available = [dish for dish in people[name] if dish in foo and foo[dish] > 0]
			if len(available) == 0:
				return None
			if len(available) == 1:
				dish = available[0]
				foo[dish] -= 1
				curr[name] = dish
		return curr
	prev = len(current)
	current = obvious(current)
	while current != None and prev != len(current):
		prev = len(current)
		current = obvious(current)
	if current == None:
		return None
	# check base case again
	if current.keys() == people.keys():
		return current
	# choose someone to assume
	name = [person for person in people.keys() if person not in current.keys()][-1]
	temp = current.copy()
	# explore branches (multiple branches, not just left/right)
	available = [dish for dish in people[name] if dish in foo and foo[dish] > 0]
	for dish in available:
		temp[name] = dish
		new_food = foo.copy()
		new_food[dish] -= 1
		result = feed(people, new_food, temp)
		if result != None:
			temp.update(result)
			return temp
	return None

##################################################
#  Problem 3
##################################################


# RESUBMISSION COMMENT - WHAT WAS WRONG WITH MY ORIGINAL SOLUTION
# My original solution was incomplete. 
# FindAll was not implemented. 
# 


class FindAll:
	def find_all(self, text):
		if isinstance(self, Sequence) or isinstance(self, Alternatives) or isinstance(self, Repeat) or isinstance(self, Star):
			i = 0
			while i < len(text):
				result = self.match(text, i)
				if result != None:
					yield result
					i = result[1]
				else:
					i += 1
		else:
			a = Sequence(self)
			return fa(a, text)


class Verbatim(FindAll):
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


class Dot(FindAll):
	"""
	Matches any single character in a piece of text.
	"""
	def match(self, text, start_index=0):
		if start_index >= len(text):
			return None
		return (start_index, start_index+1, text[start_index])


class CharFrom(FindAll):
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


class CharNotFrom(FindAll):
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


class Sequence(FindAll):
	"""
	Matches only if the given patterns all occur in order.  Patterns is given
	as a list of instances of one of these classes.
	"""
	def __init__(self, patterns):
		self.patterns = patterns

	def match(self, text, start_index=0):
		start = start_index
		result = None
		for p in self.patterns:
			result = p.match(text, start)
			if result == None:
				return None
			end = result[1]
			start = end
		return (start_index, end, text[start_index:end])


class Alternatives(FindAll):
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


class Repeat(FindAll):
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
		count = 0
		start = start_index
		result = 'thing'
		while result != None and count < self.m:
			result = self.p.match(text, start)
			if result == None:
				break
			count += 1
			end = result[1]
			start = end
		if result == None and count < self.n:
				return None
		return (start_index, end, text[start_index:end])


class Star(FindAll):
	"""
	Matches the given pattern (an instance of one of these classes) repeated an
	arbitrary number of times.  0 times (matching the empty string) is a valid
	match.
	"""
	def __init__(self, pattern):
		self.p = pattern

	def match(self, text, start_index=0):
		start = start_index
		end = start
		result = 'thing'
		while result != None and start < len(text):
			result = self.p.match(text, start)
			if result == None:
				break
			end = result[1]
			start = end
		return (start_index, end, text[start_index:end])


if __name__ == "__main__":
	doctest.testmod()
