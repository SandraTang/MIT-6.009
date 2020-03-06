#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)

def check_surrounding(num_rows, num_cols, board, func, item = None, mask = None):
    """
    check surrounding squares
    """
    surrounding = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
    for row in range(num_rows):
        for col in range(num_cols):
            # figuring out number of bombs in 8 squares around
            if not board[row][col] == item:
                for pos in surrounding:
                    # if in bounds
                    if not(row+pos[0] < 0 or col+pos[1] < 0 or row+pos[0] > num_rows-1 or col+pos[1] > num_cols-1):
                        func(board, row, col, pos[0], pos[1], mask)

# 2-D IMPLEMENTATION

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    # N-D IMPLEMENTATION ONCE I GET IT TO WORK
    return new_game_nd((num_rows, num_cols), bombs)

    # BUILDING BOARD AND MASK (added mask for efficiency)
    # board = []
    # mask = []
    # # build structure
    # for _ in range(num_rows):
    #     board.append([0]*num_cols)
    #     mask.append([False]*num_cols)
    # # add bombs
    # for tup in bombs:
    #     board[tup[0]][tup[1]] = '.'

    # # ADD NUMBERS TO BOARD
    # def check_bombs(board, row, col, pos0, pos1, mask = None):
    #     if board[row+pos0][col+pos1] == '.':
    #         board[row][col] += 1
    # check_surrounding(num_rows, num_cols, board, check_bombs, '.')


    # REMOVED OLD CODE BECAUSE INEFFICIENT
    # for r in range(num_rows):
    #     row = []
    #     for c in range(num_cols):
    #         if [r,c] in bombs or (r,c) in bombs:
    #             row.append('.')
    #         else:
    #             row.append(0)
    #     board.append(row)

    # DIMENSIONS ARE MADE AT THE END
    # no processing required

    # BUILD MASK
    # CODE MOVED TO TOP TO REDUCE NUMBER OF LOOPS
    # mask = []

    # OLD CODE REMOVED BECAUSE HARD TO READ
    # for r in range(num_rows):
    #     row = []
    #     for c in range(num_cols):
    #         row.append(False)
    #     mask.append(row)
    # for r in range(num_rows):
    #     for c in range(num_cols):
    #         if board[r][c] == 0:
    #             neighbor_bombs = 0
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r-1][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r+1][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r-1][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r+1][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r-1][c+1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r][c+1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r+1][c+1] == '.':
    #                         neighbor_bombs += 1
    #             board[r][c] = neighbor_bombs
    # return {
    #     'dimensions': (num_rows, num_cols),
    #     'board' : board,
    #     'mask' : mask,
    #     'state': 'ongoing'}

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    # N-D IMPLEMENTATION ONCE I GET IT TO WORK
    return dig_nd(game, (row, col))

    # if game['state'] == 'defeat' or game['state'] == 'victory':
    #     # REMOVED BECAUSE REDUNDANT
    #     # game['state'] = game['state']  # keep the state the same
    #     return 0

    # # BOMB IS UNCOVERED
    # if game['board'][row][col] == '.':
    #     game['mask'][row][col] = True
    #     game['state'] = 'defeat'
    #     return 1

    # bombs = 0
    # covered_squares = 0
    # for r in range(game['dimensions'][0]):
    #     for c in range(game['dimensions'][1]):
    #         if game['board'][r][c] == '.':
    #             if  game['mask'][r][c] == True:
    #                 bombs += 1
    #         elif game['mask'][r][c] == False:
    #             covered_squares += 1
    # REMOVED DEFEATED PORTION BECAUSE IT WOULD'VE BEEN CAUGHT EARLIER
    # if bombs != 0:
    #     # if bombs is not equal to zero, set the game state to defeat and
    #     # return 0
    #     game['state'] = 'defeat'
    #     return 0
    # if covered_squares == 0:
    #     game['state'] = 'victory'
    #     return 0

    # if game['mask'][row][col] != True:
    #     game['mask'][row][col] = True
    #     revealed = 1
    # else:
    #     return 0

    # def clear_space(board, row, col, pos0, pos1, mask):
    #     if game['mask'][row+pos0][col+pos1] == False:
    #         revealed += dig_2d(game, row+pos0, col+pos1)

    # num_rows = game['dimensions'][0]
    # num_cols = game['dimensions'][1]
    # if game['board'][row][col] == 0:
    #     # revealed = 0
    #     # check_surrounding(game['dimensions'][0], game['dimensions'][1], game['board'], clear_space, '.', game['mask'])
    #     surrounding = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
    #     # figuring out number of bombs in 8 squares around
    #     if not game['board'][row][col] == '.':
    #         for pos in surrounding:
    #             if not(row+pos[0] < 0 or col+pos[1] < 0 or row+pos[0] > num_rows-1 or col+pos[1] > num_cols-1):
    #                 if game['mask'][row+pos[0]][col+pos[1]] == False:
    #                     revealed += dig_2d(game, row+pos[0], col+pos[1])

                        # if in bounds
        # REMOVED CODE BELOW BECAUSE REPETITIVE, HARD TO READ
        # num_rows, num_cols = game['dimensions']
        # if 0 <= row-1 < num_rows:
        #     if 0 <= col-1 < num_cols:
        #         if game['board'][row-1][col-1] != '.':
        #             if game['mask'][row-1][col-1] == False:
        #                 revealed += dig_2d(game, row-1, col-1)
        # if 0 <= row < num_rows:
        #     if 0 <= col-1 < num_cols:
        #         if game['board'][row][col-1] != '.':
        #             if game['mask'][row][col-1] == False:
        #                 revealed += dig_2d(game, row, col-1)
        # if 0 <= row+1 < num_rows:
        #     if 0 <= col-1 < num_cols:
        #         if game['board'][row+1][col-1] != '.':
        #             if game['mask'][row+1][col-1] == False:
        #                 revealed += dig_2d(game, row+1, col-1)
        # if 0 <= row-1 < num_rows:
        #     if 0 <= col < num_cols:
        #         if game['board'][row-1][col] != '.':
        #             if game['mask'][row-1][col] == False:
        #                 revealed += dig_2d(game, row-1, col)
        # if 0 <= row < num_rows:
        #     if 0 <= col < num_cols:
        #         if game['board'][row][col] != '.':
        #             if game['mask'][row][col] == False:
        #                 revealed += dig_2d(game, row, col)
        # if 0 <= row+1 < num_rows:
        #     if 0 <= col < num_cols:
        #         if game['board'][row+1][col] != '.':
        #             if game['mask'][row+1][col] == False:
        #                 revealed += dig_2d(game, row+1, col)
        # if 0 <= row-1 < num_rows:
        #     if 0 <= col+1 < num_cols:
        #         if game['board'][row-1][col+1] != '.':
        #             if game['mask'][row-1][col+1] == False:
        #                 revealed += dig_2d(game, row-1, col+1)
        # if 0 <= row < num_rows:
        #     if 0 <= col+1 < num_cols:
        #         if game['board'][row][col+1] != '.':
        #             if game['mask'][row][col+1] == False:
        #                 revealed += dig_2d(game, row, col+1)
        # if 0 <= row+1 < num_rows:
        #     if 0 <= col+1 < num_cols:
        #         if game['board'][row+1][col+1] != '.':
        #             if game['mask'][row+1][col+1] == False:
        #                 revealed += dig_2d(game, row+1, col+1)

    # bombs = 0  # set number of bombs to 0
    # covered_squares = 0
    # for r in range(game['dimensions'][0]):
    #     # for each r,
    #     for c in range(game['dimensions'][1]):
    #         # for each c,
    #         if game['board'][r][c] == '.':
    #             if  game['mask'][r][c] == True:
    #                 # if the game mask is True, and the board is '.', add 1 to
    #                 # bombs
    #                 bombs += 1
    #         elif game['mask'][r][c] == False:
    #             covered_squares += 1
    # bad_squares = bombs + covered_squares
    # if bad_squares > 0:
    #     game['state'] = 'ongoing'
    #     return revealed
    # else:
    #     game['state'] = 'victory'
    #     return revealed

def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    # N-D IMPLEMENTATION ONCE I GET IT TO WORK
    return render_nd(game, xray)

    # display = game['board'].copy()
    # rows = game['dimensions'][0]
    # cols = game['dimensions'][1]
    # # loop through 2D arrays
    # for row in range(rows):
    #     for col in range(cols):
    #         # if SHOW ALL or mask TRUE
    #         if xray or game['mask'][row][col]:
    #             if display[row][col] == 0:
    #                 display[row][col] = ' '
    #             else:
    #                 display[row][col] = str(game['board'][row][col])
    #         else:
    #             display[row][col] = '_'
    # return display

def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """

    string = ''
    rows = game['dimensions'][0]
    cols = game['dimensions'][1]
    # loop through 2D arrays
    for row in range(rows):
        for col in range(cols):
            # if SHOW ALL or mask TRUE
            if xray or game['mask'][row][col]:
                if game['board'][row][col] == 0:
                    string = string + ' '
                else:
                    string = string + str(game['board'][row][col])
            else:
                string = string + '_'
        string = string + "\n"
    return string[:-1]

# N-D IMPLEMENTATION

# HELPER FUNCTIONS

def get_spot(array, tup):
    """
    Get the value stored in the array at 
    coordinate tup. 
    """
    # if not a list (thus is int, bool, etc.)
    # if not isinstance(array, list):

    if not isinstance(array, list):
        # is a number
        return array
    else:
        new_array = array[tup[0]]
        return get_spot(new_array, tup[1::])

def set_spot(array, tup, change):
    """
    Sets the index specified by tup in the array
    to the value passed in as 'change'. 
    """
    if len(tup) == 1:
        array[tup[0]] = change
    # if the next item is a value, not a list
    # if not isinstance(new_array, list):
    if not isinstance(array[tup[0]], list):
        array[tup[0]] = change
    else:
        new_array = array[tup[0]]
        return set_spot(new_array, tup[1::], change)

def create_blank(dimensions, value):
    """
    Create a blank new multi-dimensional array with all
    elements set to the value of "value". 
    """
    if len(dimensions) == 0:
        return value
    else:
        blank = []
        for _ in range(dimensions[0]):
            blank.append(create_blank(dimensions[1::], value))
        return blank
        # return [create_blank(dimensions[1::], value)]*dimensions[0]

def victory(game):
    """
    Check if there is a victory. 
    """
    coords = get_all_coords(game['dimensions'])
    for c in coords:
        if get_spot(game['board'], c) != '.' and get_spot(game['mask'], c) == False:
            return False
    return True

def neighbors(coordinates):
    """
    Gets coordinates. 
    Returns coordinates of neighbors. 
    """
    # base case
    if len(coordinates) == 1:
        return [[coordinates[0]-1], [coordinates[0]], [coordinates[0]+1]]
    else:
        n_list = []
        for i in neighbors(coordinates[1::]):
            n_list.append([coordinates[0]-1] + i)
            n_list.append([coordinates[0]] + i)
            n_list.append([coordinates[0]+1] + i)
        return(n_list)

def get_all_coords(dimensions):
    """
    Returns all possible coordinates. 
    """
    if len(dimensions) == 1:
        l = []
        for i in range(dimensions[len(dimensions)-1]):
            l.append([i])
        return l
    else:
        coords = []
        for i in get_all_coords(dimensions[:len(dimensions)-1:]):
            for i2 in range(dimensions[len(dimensions)-1]):
                coords.append(i+[i2] )
    return coords

def in_board(dimensions, coordinate):
    """
    Check if the coordinate is a valid board coordinate
    or if it goes out of bounds. 
    """
    for i in range(len(dimensions)):
        c = coordinate[i]
        d = dimensions[i]
        if c < 0 or c >= d:
            return False
    return True

# LAB FUNCTIONS

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    # initialize board and mask
    board = create_blank(dimensions, 0)
    mask = create_blank(dimensions, False)

    # add bombs
    for location in bombs:
        set_spot(board, location, '.')
        all_neighbors = neighbors(location)
        for n in all_neighbors:
            if in_board(dimensions, n) and not get_spot(board, n) == ".":
                set_spot(board, n, get_spot(board, n)+1)

    # add appropriate numbers to board
    # all_coords = get_all_coords(dimensions)
    # for coord in all_coords:
    #     neighboring = neighbors(coord)
    #     value = 0
    #     for n in neighboring:
    #         if in_board(dimensions, n) and get_spot(board, n) == '.':
    #             value += 1
    #     set_spot(board, coord, value)

    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}

def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coords (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> game1 = {'dimensions': (3),
    ...         'board': [0, 1, '.'],
    ...          'mask': [False, False, False],
    ...          'state': 'ongoing'}

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """

    # check if game already ended
    # if game['state'] == 'defeat' or game['state'] == 'victory':
    #     return 0

    # # if bomb is uncovered, defeat
    # if get_spot(game['board'], coordinates) == '.':
    #     set_spot(game['mask'], coordinates, True)
    #     game['state'] = 'defeat'
    #     return 1

    # if get_spot(game['mask'], coordinates) != True:
    #     set_spot(game['mask'], coordinates, True)
    #     revealed = 1
    # else:
    #     return 0

    # if you proceed past this point, revealed is initialized to 1

    # if it is 0
    # check all surrounding blocks
    # if they aren't bombs, then
    # if they are in range and undiscovered, 
    # check if they are 0

    def dig_recursive(game, coordinates):
        if game['state'] == 'defeat' or game['state'] == 'victory':
            return 0

        # if bomb is uncovered, defeat
        if get_spot(game['board'], coordinates) == '.':
            set_spot(game['mask'], coordinates, True)
            game['state'] = 'defeat'
            return 1

        if get_spot(game['mask'], coordinates) != True:
            set_spot(game['mask'], coordinates, True)
            revealed = 1
        else:
            return 0

        if get_spot(game['board'], coordinates) == 0:
            neighboring = neighbors(coordinates)
            for n in neighboring:
                if in_board(game['dimensions'], n):
                    if get_spot(game['mask'], n) == False:
                        revealed += dig_recursive(game, n)
        return revealed

    revealed_spaces = dig_recursive(game, coordinates)

    # determine if victory AT THE END
    if victory(game):
        game['state'] = 'victory'

    return revealed_spaces

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    display = create_blank(game['dimensions'], 0)
    all_coords = get_all_coords(game['dimensions'])
    for coord in all_coords:
        if xray or get_spot(game['mask'], coord):
            if get_spot(game['board'], coord) == 0:
                set_spot(display, coord, ' ')
            else:
                set_spot(display, coord, str(get_spot(game['board'], coord)))
        else:
            set_spot(display, coord, '_')
    return display

if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
