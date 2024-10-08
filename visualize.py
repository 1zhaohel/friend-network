"""CSC111 Winter 2024 Project 2: Visualize Data (Part 2)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the function responsible for displaying the shortest path
in the graph.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2024 CSC111 Friend Network
"""
import networkx as nx
from plotly.graph_objs import Figure, Scatter
import plotly

import data

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
BOOK_COLOUR = 'rgb(89, 205, 105)'
USER_COLOUR = 'rgb(105, 89, 205)'


def visualize_graph(graph_tuple: tuple[data.Graph, data.WeightedGraph],
                    start: str, end: str, weighted: bool) -> None:
    """Use plotly and networkx to visualize the given graph.
    """
    if weighted:
        graph = graph_tuple[1]
    else:
        graph = graph_tuple[0]

    pos = getattr(nx, 'spring_layout')(graph.conv_networkx(5000))
    nx.set_node_attributes(graph.conv_networkx(5000), pos, 'pos')

    x_values = [pos[k][0] for k in graph.conv_networkx(5000).nodes]
    y_values = [pos[k][1] for k in graph.conv_networkx(5000).nodes]

    x_edges = []
    y_edges = []

    # Output path from user to target in console
    print("\nPath to Target: ", end='')
    for i in range(len(graph.get_friend_path(start, end))):
        if i == 0:
            print(f'{graph.get_friend_path(start, end)[i][0]}, {graph.get_friend_path(start, end)[i][1]}', end='')
        else:
            print(f', {graph.get_friend_path(start, end)[i][1]}', end='')

    x_highlight_edges = []
    y_highlight_edges = []

    for edge in graph.conv_networkx(5000).edges:
        if edge in graph.get_friend_path(start, end) or (edge[1], edge[0]) in graph.get_friend_path(start, end):
            x_highlight_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_highlight_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
        else:
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    fig = Figure(data=[Scatter(x=x_edges,
                               y=y_edges,
                               mode='lines',
                               name='edges',
                               line={"color": 'rgb(144,238,144)', "width": 0.5},
                               hoverinfo='none',
                               ), Scatter(x=x_values,
                                          y=y_values,
                                          mode='markers',
                                          name='nodes',
                                          marker={"symbol": 'circle-dot', "size": 5, "color": 'rgb(0,0,128)',
                                                  "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
                                          text=list(graph.conv_networkx(5000).nodes),
                                          hovertemplate='%{text}',
                                          hoverlabel={'namelength': 0}
                                          ), Scatter(x=x_highlight_edges,
                                                     y=y_highlight_edges,
                                                     mode='lines',
                                                     name='edges',
                                                     line={"color": 'rgb(0,0,0)', "width": 2},
                                                     hoverinfo='none',
                                                     )])
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    # fig.show()
    plotly.offline.plot(fig)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'data', 'plotly.graph_objs', 'plotly'],
        'allowed-io': ['visualize_graph'],
        'max-line-length': 120
    })
