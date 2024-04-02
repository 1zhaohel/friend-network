"""CSC111 Winter 2024 Project 2: Reading Data and Constructing Graphs (Part 1)

Instructions (READ THIS FIRST!)
===============================

This Python module contains classes and functions responsible for reading data from our dataset
and creating an unweighted and weighted graph.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from __future__ import annotations
from typing import Any
import random
from queue import PriorityQueue
import math

import networkx as nx


class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.

    >>> q = Queue()
    >>> q.is_empty()
    True
    >>> q.enqueue('hello')
    >>> q.is_empty()
    False
    >>> q.enqueue('goodbye')
    >>> q.dequeue()
    'hello'
    >>> q.dequeue()
    'goodbye'
    >>> q.is_empty()
    True
    """
    # Private Instance Attributes:
    #   - _items: The items stored in this queue. The front of the list represents
    #             the front of the queue.
    _items: list

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.
        """
        return self._items == []

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the item at the front of this queue.

        Raise an EmptyQueueError if this queue is empty.
        """
        if self.is_empty():
            raise ValueError
        else:
            return self._items.pop(0)


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def conv_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph to a networkx graph, limiting it to max_vertices."""
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def get_friend_path(self, start: str, end: str) -> list[_Vertex]:
        """Returns the shortest path of mutuals between 2 people in the graph

        If there is no path, returns an empty list
        """
        start_vertex = self._vertices[start]
        end_vertex = self._vertices[end]

        parents = self._get_parents(start_vertex)
        reconstructed_path = self._reconstruct_path(start_vertex, end_vertex, parents)

        return self.path_to_edges(reconstructed_path)

    def _get_parents(self, start: _Vertex) -> dict[_Vertex, _Vertex]:
        """Returns a dictionary containing vertices (keys) which link back to their
        "parent nodes" (values) from bfs graph traversal
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

    def _reconstruct_path(self, start: _Vertex, end: _Vertex, parents: dict[_Vertex, _Vertex]) -> list[_Vertex]:
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

        return path

    def path_to_edges(self, path: list[_Vertex]) -> list[tuple:_Vertex]:
        """Takes a path between vertices and converts it into a corresponding list of edges

        >>> g = Graph()
        >>> v1 = _Vertex('a', set())
        >>> v2 = _Vertex('b', set())
        >>> v3 = _Vertex('c', set())
        >>> v4 = _Vertex('d', set())
        >>> a_path = [v1, v2, v3, v4]
        >>> edges = g.path_to_edges(a_path)
        >>> edges == [(v1, v2), (v2, v3), (v3, v4)]
        True
        """
        return [(path[i], path[i + 1]) for i in range(len(path)-1)]


class _WeightedVertex(_Vertex):
    """A vertex in a weighted graph.

    Same documentation as _Vertex, except now neighbours is a dictionary mapping
    a neighbour vertex to the weight of the edge to from self to that neighbour.
    Note that for this project, the weights will be integers between 1 and 5 indicating
    the vertex's closeness to their neighbours.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_WeightedVertex, int]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        super().__init__(item, set())
        self.neighbours = {}


class WeightedGraph(Graph):
    """A weighted graph used to represent a friend network with weights representing their closeness.

    Note that this is a subclass of the Graph class, and so inherits any methods
    from that class that aren't overridden here.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        Graph.__init__(self)

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item)

    def add_edge(self, item1: Any, item2: Any, weight: int = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> int:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def get_friend_path(self, start: str, end: str) -> list[_Vertex | _WeightedVertex]:
        """Returns the shortest path of mutuals between 2 people in the graph

        If there is no path, returns an empty list
        """
        start_vertex = self._vertices[start]
        end_vertex = self._vertices[end]

        parents = self._parents_weighted(start_vertex, end_vertex)

        reconstructed_path = self._reconstruct_path(start_vertex, end_vertex, parents)
        return self.path_to_edges(reconstructed_path)

    def _parents_weighted(self, start: _WeightedVertex, end: _WeightedVertex) -> dict[_WeightedVertex, _WeightedVertex]:
        """Uses Djikstra's algorithm to return a dictionary containing vertices (keys) which link back to their
        "parent nodes" (values).
        """
        visited = set()
        distances = {start: 0}
        prev = {}
        priority_queue = PriorityQueue()
        priority_queue.put((0, id(start), start))

        while not priority_queue.empty():
            distance, _, vertex = priority_queue.get()
            visited.add(vertex)
            if distances[vertex] < distance:
                continue

            for neighbour in vertex.neighbours:
                if neighbour in visited:
                    continue

                new_distance = distances[vertex] + vertex.neighbours[neighbour]
                if neighbour not in distances:
                    distances[neighbour] = math.inf

                if new_distance < distances[neighbour]:
                    prev[neighbour] = vertex
                    distances[neighbour] = new_distance
                    priority_queue.put((new_distance, id(neighbour), neighbour))

            if vertex == end:
                return prev

        return prev


def load_friend_network(names_file: str, edges_file: str) -> tuple[Graph, WeightedGraph]:
    """Return a friend network graph corresponding to the given datasets.

    Preconditions:
        - names_file is the path to a txt file corresponding to a list of first names
        - edges_file is the path to a txt file corresponding to the edges of the friend network
    """
    people = {}
    unweighted_network = Graph()
    weighted_network = WeightedGraph()
    random.seed(1)

    # add the ego
    unweighted_network.add_vertex('raven')
    weighted_network.add_vertex('raven')

    with open(names_file) as f1, open(edges_file) as f2:
        names = f1.readlines()
        i = random.randint(0, len(names) - 1)

        for line in f2:
            split_line = line.strip().split()
            user1, user2 = split_line[0], split_line[1]

            # map new user to name, add user to graph, create edge between user and ego (raven)
            if user1 not in people:
                people[user1] = names[i].strip()
                names.pop(i)
                i = random.randint(0, len(names) - 1)

                unweighted_network.add_vertex(people[user1])
                unweighted_network.add_edge(people[user1], 'raven')

                weighted_network.add_vertex(people[user1])
                weighted_network.add_edge(people[user1], 'raven', random.randint(1, 5))

            if user2 not in people:
                people[user2] = names[i].strip()
                names.pop(i)
                i = random.randint(0, len(names) - 1)

                unweighted_network.add_vertex(people[user2])
                unweighted_network.add_edge(people[user2], 'raven')

                weighted_network.add_vertex(people[user2])
                weighted_network.add_edge(people[user2], 'raven', random.randint(1, 5))

            unweighted_network.add_edge(people[user1], people[user2])
            weighted_network.add_edge(people[user1], people[user2], random.randint(1, 5))

    return (unweighted_network, weighted_network)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['random'],  # the names (strs) of imported modules
    #     'allowed-io': ['load_friend_network'],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
