"""CSC111 Winter 2024 Project 2: Run Program (Part 4)

Instructions (READ THIS FIRST!)
===============================

This Python module contains classes responsible for running the entire program.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from data import load_friend_network
from visualize import visualize_graph


def run() -> None:
    """Run the program to find matching friend"""

    is_weighted = input("Use weighted graph? (y/n): ")

    if is_weighted == "y":
        is_weighted = True
    else:
        is_weighted = False

    my_graph = load_friend_network('data/first-names.txt', 'data/edges.txt')

    graph_vertices = my_graph[0].get_vertices()

    user = input("Enter your name: ")

    while user not in graph_vertices:
        print("User not found!")
        user = input("Enter your name: ")

    target = input("Enter target: ")

    while target not in graph_vertices:
        print("Target not found!")
        target = input("Enter target: ")

    visualize_graph(my_graph, user, target, is_weighted)

    print("\n")
    exit("Program finished.")


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random', 'networkx', 'data', 'plotly.graph_objs', 'visualize'],
        'allowed-io': ['run'],
        'max-line-length': 120
    })

    run()
