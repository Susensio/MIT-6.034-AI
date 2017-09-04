# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

# Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.


def bfs(graph, start, goal):
    agenda = [[start]]
    extended = set()
    while True:
        path = agenda[0]
        if path[-1] == goal:
            return path
        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path and node not in extended]
        paths_extended = [path + [node] for node in nodes_valid]
        extended.add(path[-1])
        agenda = agenda + paths_extended
        agenda.remove(path)


# Once you have completed the breadth-first search,
# this part should be very simple to complete.


def dfs(graph, start, goal):
    agenda = [[start]]
    extended = set()
    while True:
        path = agenda[0]
        if path[-1] == goal:
            return path
        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path and node not in extended]
        paths_extended = [path + [node] for node in nodes_valid]
        extended.add(path[-1])
        agenda = paths_extended + agenda
        agenda.remove(path)


# Now we're going to add some heuristics into the search.
# Remember that hill-climbing is a modified version of depth-first search.
# Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    agenda = [[start]]
    while True:
        path = agenda[0]
        if path[-1] == goal:
            return path
        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path]
        paths_extended = [path + [node] for node in nodes_valid]
        paths_extended.sort(key=lambda nodes: graph.get_heuristic(nodes[-1], goal))
        agenda = paths_extended + agenda
        agenda.remove(path)


# Now we're going to implement beam search, a variation on BFS
# that caps the amount of memory used to store paths.  Remember,
# we maintain only k candidate paths of length n in our agenda at any time.
# The k top candidates are to be determined using the
# graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    agenda = [[[start]], []]
    depth = 0
    while True:
        # If there are no paths left, return empty path
        try:
            path = agenda[depth][0]
        except IndexError:
            return []

        if path[-1] == goal:
            return path

        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path]
        paths_extended = [path + [node] for node in nodes_valid]
        agenda[depth + 1].extend(paths_extended)
        agenda[depth + 1].sort(key=lambda nodes: graph.get_heuristic(nodes[-1], goal))
        agenda[depth + 1] = agenda[depth + 1][:beam_width]

        agenda[depth].remove(path)
        if len(agenda[depth]) == 0:
            depth += 1
            agenda.append([])

# Now we're going to try optimal search.  The previous searches haven't
# used edge distances in the calculation.

# This function takes in a graph and a list of node names, and returns
# the sum of edge lengths along the path -- the total distance in the path.


def path_length(graph, node_names):
    edges = [graph.get_edge(node_names[index - 1], node) for index, node in enumerate(node_names) if index > 0]
    return sum([edge.length for edge in edges])


def branch_and_bound(graph, start, goal):
    agenda = [[start]]
    while True:
        path = agenda[0]
        if path[-1] == goal:
            return path
        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path]
        paths_extended = [path + [node] for node in nodes_valid]
        agenda = paths_extended + agenda
        agenda.remove(path)
        agenda.sort(key=lambda nodes: path_length(graph, nodes))


def a_star(graph, start, goal):
    agenda = [[start]]
    extended = set()
    while True:
        path = agenda[0]
        if path[-1] == goal:
            return path
        nodes_connected = graph.get_connected_nodes(path[-1])
        nodes_valid = [node for node in nodes_connected if node not in path and node not in extended]
        paths_extended = [path + [node] for node in nodes_valid]
        agenda = paths_extended + agenda
        extended.add(path[-1])
        agenda.remove(path)
        agenda.sort(key=lambda nodes: path_length(graph, nodes) + graph.get_heuristic(nodes[-1], goal))


# It's useful to determine if a graph has a consistent and admissible
# heuristic.  You've seen graphs with heuristics that are
# admissible, but not consistent.  Have you seen any graphs that are
# consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        length = path_length(graph, branch_and_bound(graph, node, goal))
        heuristic = graph.get_heuristic(node, goal)
        if heuristic > length:
            return False
    return True


def is_consistent(graph, goal):
    for start in graph.nodes:
        for end in graph.nodes:
            length = path_length(graph, branch_and_bound(graph, start, end))
            heuristic = abs(graph.get_heuristic(start, goal) - graph.get_heuristic(end, goal))
            if heuristic > length:
                return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '5'
WHAT_I_FOUND_INTERESTING = 'Little implementation differences between algorithms lead to big behaviour differences'
WHAT_I_FOUND_BORING = 'Nothing at all'
