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
import data
from data import Queue


def get_friend_path(graph: data.Graph, start: str, end: str) -> list[str]:
    """Returns the shortest path of mutuals between 2 people in the graph

    If there is no path, returns an empty list
    """
    # TODO: implement public get graph size method
    prev = get_parents(graph._vertices[start])

    return []


def get_parents(start: data._Vertex):
    # TODO: type annotations
    """Gets the path but backwards ig???
    """
    queue = Queue()
    queue.enqueue(start)

    visited = {start}
    parents = {}

    while not queue.is_empty():
        parent = queue.dequeue()

        for neighbour in parent.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.enqueue(neighbour)
                parents[neighbour] = parent

    return parents


def reconstructPath(start: data._Vertex, end:data._Vertex, parents):
    path = []
    current = end

    while current != end:
        if current not in parents:
            return []
        path.append(current)
        current = parents[current]

    path.append(start)
    path.reverse()

    return [person.item for person in path]
