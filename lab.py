#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url

# NO ADDITIONAL IMPORTS!


ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}

# THIS IS OLD
# def build_auxiliary_structures(nodes_filename, ways_filename):
#     """
#     Create any auxiliary structures you are interested in, by reading the data
#     from the given filenames (using read_osm_data)
#     """
#     nodes = {}
#     possible_nodes = set()
#     locs = {}
#     for way in read_osm_data(ways_filename):
#         # key - way ID
#         # value - dict of nodes list and tags dictionary
#         # {id: [node, node], id: [node, node], id: [node, node]}
#         if 'highway' in way['tags'] and way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
#             path = way['nodes']
#             for i in range(len(path)-1):
#                 if not 'oneway' in way['tags'] or not way['tags']['oneway'] == 'yes':
#                     nodes.setdefault(path[i+1], set()).add(path[i])
#                 nodes.setdefault(path[i], set()).add(path[i+1])
#                 possible_nodes.add(path[i])
#             # add last node manually since for loop skips it
#             possible_nodes.add(path[len(path)-1])
#             # this may be right idk
#             nodes.setdefault(path[len(path)-1], set())

#     for node in read_osm_data(nodes_filename):
#         # key - node ID
#         # value - tuple of location (lat, lon)
#         # {id: (lat, lon), id: (lat, lon), id: (lat, lon)}
#         if node['id'] in possible_nodes:
#             locs[node['id']] = (node['lat'], node['lon'])           
#     return nodes, locs

def dist_btw(structure, id1, id2):
    """
    Helper Function (Sandra Tang)
    Finds distance in miles between two locations. 
    Provided - dataset, two node id's
    Returns - distance (miles)
    """
    nodes, locs = structure
    lat1, lon1 = locs[id1]
    lat2, lon2 = locs[id2]
    # print(great_circle_distance((lat1, lon1), (lat2, lon2)))
    return great_circle_distance((lat1, lon1), (lat2, lon2))

def follow_node(dataset, id):
    """
    Helper Function (Sandra Tang)
    Follows way from beginning node to ending node. 
    Provided - dataset, way's id
    Returns - miles travelled from beginning to end node
    """
    way = None
    for possible_way in read_osm_data('resources/'+dataset+'.ways'):
        if possible_way['id'] == id:
            way = possible_way
    nodes = way['nodes']
    miles = 0
    for node in nodes:
        if not node == nodes[0]:
            miles += distance_between(dataset, node, node_before)
        node_before = node
    return miles

def follow_path(structure, path):
    nodes, locs = structure
    distance = 0
    # ignore first element because it is the distance
    for i in range(1, len(path)-1):
        distance += dist_btw(structure, path[i], path[i+1])
    return distance

def cost(structure, path, goal):
    nodes, locs = structure
    cost = path[0]
    # path is a list of node IDs [n, n, n]
    one = path[len(path)-2] # node ID 1
    two = path[len(path)-1] # node ID 2
    # additional distance
    cost += dist_btw(structure, one, two)
    # heuristic
    # cost += dist_btw(structure, two, goal)
    return cost

def cost_heuristic(structure, path, goal):
    nodes, locs = structure
    cost = path[0]
    # path is a list of node IDs [n, n, n]
    one = path[len(path)-2] # node ID 1
    two = path[len(path)-1] # node ID 2
    # additional distance
    # heuristic
    cost += dist_btw(structure, two, goal)
    return cost

def nearest_node(structure, loc):
    """
    Helper Function (Sandra Tang)
    Finds node nearest to provided location. 
    Provided - location
    Returns - nearest node
    """
    nodes, locs = structure
    min_dist = None
    nearest = None
    for key, value in locs.items():
        node = key
        n_loc = (value[0], value[1])
        dist = great_circle_distance(loc, n_loc)
        if min_dist == None:
            min_dist = great_circle_distance(loc, n_loc)
            nearest = node
        dist = great_circle_distance(loc, n_loc)
        if dist < min_dist:
            min_dist = dist
            nearest = node
    return nearest

def find_short_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """
    return find_path(aux_structures, loc1, loc2, cost, cost_heuristic)

# NEW ONE
def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    """
    nodes = {}
    possible_nodes = set()
    locs = {}
    for way in read_osm_data(ways_filename):
        # key - way ID
        # value - dict of nodes list and tags dictionary
        # {id: [(node, speed_lim), (node, speed_lim)]}
        if 'highway' in way['tags'] and way['tags']['highway'] in ALLOWED_HIGHWAY_TYPES:
            path = way['nodes']
            # if way has maxspeed_mph tag
            if 'maxspeed_mph' in way['tags']:
                speed = way['tags']['maxspeed_mph']
            # if tag doesn't exist, look up highway speed
            else:
                speed = DEFAULT_SPEED_LIMIT_MPH[way['tags']['highway']]
            for i in range(len(path)-1):
                if not 'oneway' in way['tags'] or not way['tags']['oneway'] == 'yes':
                    # dictionary of dictionaries
                    # {n: {n:s, n:s, n:s}, n: {n:s, n:s, n:s}, n: {n:s, n:s, n:s}}
                    nodes.setdefault(path[i+1], {})
                    if path[i] not in nodes[path[i+1]] or nodes[path[i+1]][path[i]] < speed:
                        # if path[i] in nodes[path[i+1]] and nodes[path[i+1]][path[i]] < speed:
                            # print("CHANGED")
                        nodes[path[i+1]][path[i]] = speed
                nodes.setdefault(path[i], {})
                if path[i+1] not in nodes[path[i]] or nodes[path[i]][path[i+1]] < speed:
                        # if path[i+1] in nodes[path[i]] and nodes[path[i]][path[i+1]] < speed:
                            # print("CHANGED")
                        nodes[path[i]][path[i+1]] = speed
                possible_nodes.add(path[i])
            # add last node manually since for loop skips it
            possible_nodes.add(path[len(path)-1])
            nodes.setdefault(path[len(path)-1], {})

    for node in read_osm_data(nodes_filename):
        # key - node ID
        # value - tuple of location (lat, lon)
        # {id: (lat, lon), id: (lat, lon), id: (lat, lon)}
        if node['id'] in possible_nodes:
            locs[node['id']] = (node['lat'], node['lon'])       
    # print(nodes)
    # print()
    # print(locs)    
    return nodes, locs

def time(structure, path, goal):
    nodes, locs = structure
    time = path[0]
    # path is a list of node IDs [n, n, n]
    one = path[len(path)-2] # node ID 1
    two = path[len(path)-1] # node ID 2
    speed = nodes[one][two] # yield speed
    # additional distance
    time += dist_btw(structure, one, two) / speed
    # heuristic (distance, strictly, though)
    # time += dist_btw(structure, path[len(path)-1], goal)
    return time

def time_heuristic(structure, path, goal):
    nodes, locs = structure
    time = path[0]
    # path is a list of node IDs [n, n, n]
    one = path[len(path)-2] # node ID 1
    two = path[len(path)-1] # node ID 2
    speed = nodes[one][two] # yield speed
    # additional distance
    # time += dist_btw(structure, one, two) / speed
    # heuristic (distance, strictly, though)
    # time += dist_btw(structure, path[len(path)-1], goal)
    time = 0
    return time

def find_fast_path(aux_structures, loc1, loc2):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    return find_path(aux_structures, loc1, loc2, time, time_heuristic)

def find_path(aux_structures, loc1, loc2, func, heuristic):
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """
    # find neares nodes
    node1 = nearest_node(aux_structures, loc1)
    node2 = nearest_node(aux_structures, loc2)
    # unpack structure
    nodes, locs = aux_structures
    # agenda with first path to consider
    agenda = [[0, 0, node1]]
    # visit nodes
    visited = set()
    # visited.add(node1)
    # loop through data
    while agenda:
        # print(agenda)
        min_cost_path = agenda[0]
        for p in agenda:
            if p[1] < min_cost_path[1]:
                min_cost_path = p
        index = agenda.index(min_cost_path)
        # remove min cost path, assign it to path
        path = agenda.pop(index)
        path_last_node = path[len(path)-1]
        # if already visited path
        if path_last_node in visited:
            continue
        if path_last_node == node2:
            # print(path[1:])
            loc_path = []
            for n in path[2:]:
                loc_path.append(locs[n])
            # print(loc_path)
            return loc_path
        # if the node doesn't connect to anything and isn't goal
        if path_last_node not in nodes.keys():
            continue
        connections = nodes[path_last_node].keys()
        for node in connections:
            if node not in visited:
                new_path = path.copy()
                new_path.append(node)
                new_path[0] = func(aux_structures, new_path, node2)
                new_path[1] = new_path[0] + heuristic(aux_structures, new_path, node2)
                # print(new_path)
                agenda.append(new_path)
        visited.add(path_last_node)
    return None

if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # structure = build_auxiliary_structures('resources/midwest.nodes', 'resources/midwest.ways')
    # nodes, locs = structure
    # print(nodes, locs)
    # for way in read_osm_data('resources/mit.ways'):
    #     print(way)
    # print(find_short_path(structure, (42.3612, -71.092), (42.3612, -71.092)))
    # ALL NODES 44809
    # NODE CONNECTED BY VALID HIGHWAY 8339
    # 788 VALID RELEVANT WAYS
    # node = nearest_node(structure, (41.4452463, -89.3161394))
    # print(node)
    # nodes, ways = structure
    # print(ways)
    # print(ways[233883323])
    # structure = build_auxiliary_structures('resources/mit.nodes', 'resources/mit.ways')
    # print(structure)
    # node = nearest_node(structure, (42.355, -71.1009))
    # print(node)
    # {'id': 1, 'lat': 42.3575, 'lon': -71.0952, 'tags': {'name': 'Kresge'}}
    # {'id': 2, 'lat': 42.355, 'lon': -71.1009, 'tags': {'name': 'New House'}}
    # {'id': 3, 'lat': 42.3575, 'lon': -71.0927, 'tags': {'name': 'South Maseeh'}}
    # {'id': 5, 'lat': 42.3592, 'lon': -71.0932, 'tags': {'name': 'Lobby 7'}}
    # {'id': 6, 'lat': 42.36, 'lon': -71.0907, 'tags': {'name': 'Building 26'}}
    # {'id': 7, 'lat': 42.3601, 'lon': -71.0952, 'tags': {'name': 'Building 35'}}
    # {'id': 8, 'lat': 42.3612, 'lon': -71.092, 'tags': {'name': '009 OH'}}
    # {'id': 9, 'lat': 42.3605, 'lon': -71.091, 'tags': {'name': 'The Fountain of Youth'}}
    # {'id': 10, 'lat': 42.3582, 'lon': -71.0931, 'tags': {'name': 'North Maseeh'}}
    # {'id': 11, 'lat': 42.3575, 'lon': -71.0956, 'tags': {'name': 'Parking Lot'}}
    # structure = build_auxiliary_structures('resources/cambridge.nodes', 'resources/cambridge.ways')
    # print(find_short_path(structure, (42.3858, -71.0783), (42.5465, -71.1787)))
    # with heuristic 47609
    # without heuristic ):
    # Location 1: (42.3858, -71.0783)
    # Location 2: (42.5465, -71.1787)
    
    pass
