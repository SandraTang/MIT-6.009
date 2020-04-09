# NO IMPORTS!

##################################################
### Problem 1: batch
##################################################

def batch(inp, size):
    """ Return a list of batches, per quiz specification """
    batches = []
    current = []
    for index in range(len(inp)):
    	num = inp[index]
    	current.append(num)
    	if sum(current) >= size or index == len(inp)-1:
    		batches.append(current)
    		current = []
    return batches


##################################################
### Problem 2: order
##################################################

def helper(inp, seen = set()):
	# seen = seen letters
	if inp == []:
		return []
	out = []
	new_inp = []
	letter = inp[0]
	letter = letter[0]
	for i in inp:
		if i[0] == letter:
			out.append(i)
		else:
			new_inp.append(i)
	return out + helper(new_inp, seen | set(letter))


def order(inp):
    """ Return an ordered list of string, per quiz specification """
    # recursive
    return helper(inp)


##################################################
### Problem 3: path_to_happiness
##################################################

def valid_positions(r, rows):
	pos = []
	if r - 1 >= 0:
		pos.append(r-1)
	pos.append(r)
	if r + 1 < rows:
		pos.append(r+1)
	return pos

def path_to_happiness(field):
	""" Return a path through field of smiles that maximizes happiness """

	f_temp = list(field["smiles"])

	rows = len(f_temp)
	cols = len(f_temp[0])

	# make copy of field
	b = []
	f = []
	for row_num in range(len(f_temp)):
		b.append([])
		f.append([])
		for col_num in range(len(f_temp[0])):
			b[row_num].append(f_temp[row_num][col_num])
			f[row_num].append(f_temp[row_num][col_num])

	# go row by row
	# backwards in col
	col_list = list(range(1, cols))
	col_list.reverse()

	# create map of numbers in b
	# higher number = better path
	for c in col_list:
		for r in range(rows):
			# column positions of possible options
			pos = valid_positions(r, rows)
			# values of possible options
			most = max(f[p][c-1] for p in pos)
			# r = row
			# p = new row
			# c = column
			# c-1 = new column
			# increase b accordingly
			for p in pos:
				if f[p][c-1] == most and f[r][c] + f[p][c-1] > b[p][c-1]:
					b[p][c-1] = f[r][c] + f[p][c-1]
		for r in range(rows):
			f[p][c-1] = b[p][c-1]
	
	# now use b
	# start index = index of row with max val, col = 0
	# next, go thru cols and find rows
	indexes = []
	max_val = 0
	i = 0
	for r in range(rows):
		if b[r][0] > max_val:
			max_val = b[r][0]
			i = r
	indexes.append(i)
	for c in range(1, cols):
		max_val = 0
		i = 0
		pos = valid_positions(indexes[-1], rows)
		for r in pos:
			if b[r][c] >= max_val:
				max_val = b[r][c]
				i = r
		indexes.append(i)
	return indexes