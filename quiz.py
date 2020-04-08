# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def vals_at_depth(tree, depth):
    """
    Takes in tree (nested list) and depth (int). 
    """
    if depth == 0:
        return [tree[0]]
    current = tree
    for _ in range(depth-1):
        answer = []
        for x in current:
            if isinstance(x, list):
                for e in x:
                    answer.append(e)
        current = answer
    answer = []
    for x in current:
        if isinstance(x, list):
            answer.append(x[0])
    return answer

##################################################
##  Problem 2
##################################################

def weave(list1, list2):
    """
    Creates a list with no duplicates
    of alternating elements from 
    list1 and list2 until items have
    been exhausted. 
    """
    # indexes of list 1 and 2
    i = 0
    j = 0
    weave = []
    prev = None
    current = None
    while i < len(list1) or j < len(list2):
        if i < len(list1):
            current = list1[i]
            while current == prev:
                i += 1
                if i >= len(list1):
                    break
                current = list1[i]
            if i >= len(list1):
                continue
            prev = list1[i]
            weave.append(prev)
            i += 1
        if j < len(list2):
            current = list2[j]
            while current == prev:
                j += 1
                if j >= len(list2):
                    break
                current = list2[j]
            if j >= len(list2):
                continue
            prev = list2[j]
            weave.append(prev)
            j += 1
    return weave

##################################################
##  Problem 3
##################################################

def all_blobs(world):
    """
    Takes in dictionary with rows, cols,
    and a list representation of a world
    with blobs. 
    """
    rows = world["nrows"]
    cols = world["ncols"]
    grid = world["grid"]
    seen = set()
    blobs = []

    def valid_locs(pos):
        row = pos[0]
        col = pos[1]
        valid = []
        if row-1 >= 0 and (row-1, col) not in seen:
            valid.append((row-1, col))
        if row+1 < rows and (row+1, col) not in seen:
            valid.append((row+1, col))
        if col-1 >= 0 and (row, col-1) not in seen:
            valid.append((row, col-1))
        if col+1 < cols and (row, col+1) not in seen:
            valid.append((row, col+1))
        return valid

    def expand(pos, letter):
        blob_locs = set()
        blob_locs.add(pos)
        # find adjacent positions to given position
        adjacent = valid_locs(pos)
        # see if contain blob letter and expand
        for loc in adjacent:
            if grid[loc[0]][loc[1]] == letter:
                # loc is tuple
                seen.add((loc[0], loc[1]))
                # expand returns set of tuples
                blob_locs |= expand(loc, letter)
        return blob_locs

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in seen:
                if grid[row][col] == None:
                    seen.add((row, col))
                else:
                    # recursive call
                    blob = [grid[row][col], expand((row, col), grid[row][col])]
                    blobs.append(blob)

    return blobs

if __name__ == "__main__":
    pass
