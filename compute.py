"""CSC111 Winter 2024 Project 2: Compute on Data (Part 2)

Instructions (READ THIS FIRST!)
===============================

This Python module contains classes responsible for computing on the data.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import networkx as nx

import data
from data import Queue

# TODO: add these functions as methods in Graph class


def get_friend_path(graph: data.Graph, start: str, end: str) -> list[str]:
    """Returns the shortest path of mutuals between 2 people in the graph

    If there is no path, returns an empty list
    """
    start_vertex = graph._vertices[start]
    end_vertex = graph._vertices[end]
    parents = get_parents(start_vertex)

    return reconstruct_path(start_vertex, end_vertex, parents)


def get_parents(start: data._Vertex) -> dict[_Vertex, _Vertex]:
    """Returns a dictionary containing vertices (keys) which link back to their
    "parent nodes" (values) from bfs graph traversal
    """
    queue = Queue()
    queue.enqueue(start)

    visited = {start}
    parents = {}
    parents_with_str = {}

    while not queue.is_empty():
        parent = queue.dequeue()

        for neighbour in parent.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.enqueue(neighbour)
                parents[neighbour] = parent
                parents_with_str[neighbour.item] = parent.item

    return parents


def reconstruct_path(start: data._Vertex, end: data._Vertex, parents) -> list[str]:
    """Reconstructs the shortest path between start to end by going backwards in the parents
    dictionary starting from the end vertex.

    The path is a list containing the items of the vertices

    If there is no path between start and end, returns an empty list
    """
    path = []
    current = end

    while current != start:
        if current not in parents:
            return []
        path.append(current)
        current = parents[current]

    path.append(start)
    path.reverse()

    return [person.item for person in path]


# FUNCTION FOR TESTING PURPOSES
def test_graph():
    g = data.Graph()
    # names = ['a', 'b', 'c', 'd', 'e']
    # edges = [['a', 'b'], ['a', 'c'], ['a', 'e'], ['b', 'c'], ['c', 'd'], ['c', 'e']]

    names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    edges = [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'f'], ['b', 'c'], ['f', 'g'], ['c', 'g'], ['c', 'h'], ['d', 'h'], ['h', 'i']]

    for name in names:
        g.add_vertex(name)
    for edge in edges:
        g.add_edge(edge[0], edge[1])

    print(get_friend_path(g, 'a', 'e'))


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
