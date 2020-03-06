#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for lab 2 will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).

KEVIN_BACON_ID = 4724

def ID_to_name(arr):
    """
    Takes in an array of IDs. 
    Returns modified array with names. 
    """
    # arr is an array
    # get file data
    filename = 'resources/names.pickle'
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    # replace IDs with names
    for key, value in data.items():
        if value in arr:
            for i in range(len(arr)):
                if arr[i] == value:
                    arr[i] = key
    return arr

def ID_to_movie(arr):
    """
    Takes in an array of IDs. 
    Returns modified array with movies. 
    """
    # arr is an array
    # get file data
    filename = 'resources/movies.pickle'
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    # replace IDs with movie name
    for key, value in data.items():
        if value in arr:
            for i in range(len(arr)):
                if arr[i] == value:
                    arr[i] = key
    return arr

def acted_together(data, actor_id_1, actor_id_2):
    """
    Takes in data and two actors. Returns if they acted together. 
    """
    # loop through all tuples in the data
    for tup in data:
        # if actors are in same tuple
        if (actor_id_1 == tup[0] and actor_id_2 == tup[1]) or (actor_id_1 == tup[0] and actor_id_2 == tup[1]):
            return True
    return False


def actors_with_bacon_number(data, n):
    """
    # Takes database and desired Bacon number.
    # Returns set containing ID numbers of actors with desired Bacon number.
    # """
    # # Kevin Bacon's actor ID is 4724

    # # FINDING BACON NUMBER 0
    # # Kevin Bacon is the only person with a Bacon number of 0. 
    # if n == 0:
    #     return {4724}

    # # FINDING BACON NUMBER 1
    # # Iterate through tuples and check if Kevin Bacon's number is in either
    # # Index [0] OR [1] in the tuple
    # # Check that the number is not Kevin Bacon's

    # # dictionary
    # actor_BNs = build_graph(data)

    # # return the people with a certain bacon number
    # queue = set()
    # queue.add(KEVIN_BACON_ID)
    # next_queue = set()
    # seen = set()
    # seen.add(KEVIN_BACON_ID)

    # # get queue
    # for _ in range(n):
    #     for ID in queue:
    #         for actor in actor_BNs[ID]:
    #             if not actor in seen:
    #                 next_queue.add(actor)
    #         seen |= set(actor_BNs[ID])
    #     queue = next_queue.copy()
    #     next_queue = set()
    # return queue

    # ONE LINER
    # return {key for key, value in actor_BNs.items() if value == n}

    # make graph
    actor_graph = build_graph(data)
    seen = set()
    current_layer = {4724}
    layer_count = 0

    # split bacon numbers into layers
    while len(current_layer)>0:
        if layer_count == n:
            return current_layer

        # add people to current layer (current bacon #)
        seen |= current_layer
        neighbors = set()
        for node in current_layer:
            neighbors |= actor_graph[node]

        current_layer = neighbors - seen
        layer_count += 1

    # if nobody, return empty set just in case
    return set()

def build_graph(data):
    actor_BNs = {}

    # go through O(n), loop through data
    for tup in data:
        ACTOR_1 = tup[0]
        ACTOR_2 = tup[1]
        # add actor info OR
        # if actor not already in dictionary, 
        # add actor and their info
        actor_BNs.setdefault(ACTOR_1, set()).add(ACTOR_2)
        actor_BNs.setdefault(ACTOR_2, set()).add(ACTOR_1)

    #return dict with connections
    return actor_BNs

def bacon_path(data, actor_id):
    """
    Takes in data and ID of an actor you are looking for. Returns kevin bacon, actors to the goal, and the goal. 
    """
    return actor_to_actor_path(data, 4724, actor_id)



def actor_to_actor_path(data, actor_id_1, actor_id_2):
    """
    Takes in data and two actors. 
    Returns shortest path from the first to the second actor. 
    """
    actor_graph = build_graph(data)
    # builds path
    parents = {actor_id_2: None}
    seen = {actor_id_1}
    queue = [actor_id_1]
    index = 0

    # implement BFS
    while index < len(queue):
        # pop first node from the queue
        curr_node = queue[index]
        if curr_node == actor_id_2:
            break

        # remove actors already seen from neighbors
        curr_neighbors = actor_graph[curr_node] - seen 

        # For each new unseen node in neighbors, set parent, add to queue, and mark it seen
        for neighbor in curr_neighbors:
            parents[neighbor] = curr_node
            # to be dealt with 
            queue.append(neighbor)
            # seen list, for efficiency
            seen.add(neighbor)

        # move to next
        index+=1

    if parents[actor_id_2] is None:
        return None
    else:
        path = [actor_id_2]
        prev = parents[actor_id_2]
        # load off actors to create path
        while prev is not actor_id_1:
            path.append(prev)
            prev = parents[prev]

        path.append(actor_id_1)
        path.reverse()
        return path

def actor_path(data, actor_id_1, goal_test_function):
    """
    Takes data, actor ID, and function. 
    Function takes actor ID, returns T/F if actor is valid ending for path. 
    Actor_path returns list of actor IDs, shortest path from actor_id_1 to satisfy function. 
    """
    if goal_test_function(actor_id_1):
        return [actor_id_1]

    actor_graph = build_graph(data)
    # builds path
    goal_actor = None
    parents = {}
    seen = set()
    queue = [actor_id_1]
    index = 0

    # implement BFS
    while index < len(queue):
        # pop first node from the queue
        curr_node = queue[index]
        if goal_test_function(curr_node):
            goal_actor = curr_node
            break

        # remove actors already seen from neighbors
        curr_neighbors = actor_graph[curr_node] - seen 

        # For each new unseen node in neighbors, set parent, add to queue, and mark it seen
        for neighbor in curr_neighbors:
            parents[neighbor] = curr_node
            # to be dealt with 
            queue.append(neighbor)
            # seen list, for efficiency
            seen.add(neighbor)

        # move to next
        index+=1

    if goal_actor is None:
        return None
    else:
        path = [goal_actor]
        prev = parents[goal_actor]
        # load off actors to create path
        while prev is not actor_id_1:
            path.append(prev)
            prev = parents[prev]

        path.append(actor_id_1)
        path.reverse()
        return path


# WERE WE SUPPOSED TO MAKE OUR OWN FUNC OR IMPLEMENT INTO PRE-EXISTING THING
def get_movie_path(data, actor_1, actor_2):
    """
    Iterate through every two actors, 
    find the correct movie, and add it to a list.
    """
    # get path from actor 1 to actor 2 
    actor_path = actor_to_actor_path(data, actor_1, actor_2)
    path = []
    # loop through path
    for i in range(len(actor_path)-1):
        # loop through tuples in data
        for film in data:
            # add film to list of movies if actors both in it
            if actor_path[i] in film and actor_path[i+1] in film:
                path.append(film[2])
    return path

# helper function
def actors_in_film(data, goal_film):
    actors = set()
    # loop through tuple
    for tup in data:
        # get data
        actor_1 = tup[0]
        actor_2 = tup[1]
        film = tup[2]
        # if actors are in the film, add to set
        if film == goal_film:
            actors.add(actor_1)
            actors.add(actor_2)
    return actors

def actors_connecting_films(data, film1, film2):
    # shortest possible list of actor ID numbers (in order) that connect those two films
    # find actors tht acted in film 1
    # find actors that acted in film 2
    # find shortest path from an actor in film 1 to an actor in film 2
    # this doens't take that long
    # film1_actors = actors_in_film(data, film1)
    # film2_actors = actors_in_film(data, film2)
    # intersects = film1_actors.intersection(film2_actors)
    # # cut down on run time by returning actor in common IF exists
    # if intersects:
    #     return [intersects[0]]

    # # def valid(actor_id):
    # #     return actor_id in film2_actors

    # # REALLY BAD RUN TIME
    # # film1_actors and film2_actors have none in common
    # paths = []
    # # find all paths
    # for actor_1 in film1_actors:
    #     for actor_2 in film2_actors:
    #         paths.append(actor_to_actor_path(data, actor_1, actor_2))
    # best_path = paths[0]
    # # find best path out of all paths
    # for path in paths:
    #     if len(best_path) > len(path):
    #         best_path = path
    # return None

    # NEW OPTIMIZED FUNCTION

    actor_graph = build_graph(data)
    actors_in_film1 = actors_in_film(data, film1)
    actors_in_film2 = actors_in_film(data, film2)

    # goal test function
    def in_film_2(actor):
        return actor in actors_in_film2

    possible_paths = []

    for actor in actors_in_film1:
        # data, actor_id_1, goal_test_function
        possible_paths.append(actor_path(data, actor, in_film_2))

    # choose the best path out of them all
    best_path = possible_paths[0]
    for paths in possible_paths:
        if len(paths) < len(best_path):
            best_path = paths

    return best_path

    # # builds path
    # actor_id_2 = "Dummy Variable"
    # parents = {actor_id_2: None}
    # seen = {actor_id_1}
    # queue = [actors_in_film1]
    # index = 0

    # # implement BFS
    # while index < len(queue):
    #     # pop first node from the queue
    #     curr_node = queue[index]
    #     if curr_node in actors_in_film2:
    #         break

    #     # remove actors already seen from neighbors
    #     curr_neighbors = actor_graph[curr_node] - seen 

    #     # For each new unseen node in neighbors, set parent, add to queue, and mark it seen
    #     for neighbor in curr_neighbors:
    #         parents[neighbor] = curr_node
    #         # to be dealt with 
    #         queue.append(neighbor)
    #         # seen list, for efficiency
    #         seen.add(neighbor)

    #     # move to next
    #     index+=1

    # if parents[actor_id_2] is None:
    #     return None
    # else:
    #     path = [actor_id_2]
    #     prev = parents[actor_id_2]
    #     # load off actors to create path
    #     while prev is not actor_id_1:
    #         path.append(prev)
    #         prev = parents[prev]

    #     path.append(actor_id_1)
    #     path.reverse()
    #     return path




if __name__ == '__main__':
    filename = 'resources/tiny.pickle'
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(actor_to_actor_path(data, 2876, 1640))
    # pass