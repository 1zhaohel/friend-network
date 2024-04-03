"""CSC111 Winter 2024 Project 2: Run Program (Part 3)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the function responsible for running the entire program.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2024 CSC111 Friend Network
"""
from data import load_friend_network
from visualize import visualize_graph


def run() -> None:
    """Run the program to find the shortest path through mutuals to contact a potential friend"""

    is_weighted = input("\nUse weighted graph? (y/n): ")

    if is_weighted == "y":
        is_weighted = True
    else:
        is_weighted = False

    # Loads an unweighted and weighted graph
    my_graph = load_friend_network('data/first-names.txt', 'data/edges.txt')
    graph_vertices = my_graph[0].get_vertices()

    # User and target should be in the friend network
    user = input("\nEnter 'help' to see the people in the network. \nEnter your name: ")
    while user not in graph_vertices:
        if user == "help":
            print("People in the Network: ")
            for name in graph_vertices:
                print(f'- {name}')
        else:
            print("User not found!")
        user = input("Enter your name: ")

    target = input("\nEnter 'help' to see the people in the network. \nEnter target friend: ")
    while target not in graph_vertices:
        if target == "help":
            print("People in the Network: ")
            for name in graph_vertices:
                print(f'- {name}')
        else:
            print("Target not found!")
        target = input("Enter target friend: ")

    visualize_graph(my_graph, user, target, is_weighted)

    choice_to_continue = input("\nDo you wish to find the path with another user? (y/n): ")
    if choice_to_continue == "y":
        run()
    else:
        exit("Thank you for using Friend Network!")


if __name__ == '__main__':
    run()
