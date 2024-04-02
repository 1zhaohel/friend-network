"""CSC111 Winter 2024 Project 2: Visualize Data (Part 3)

Instructions (READ THIS FIRST!)
===============================

This Python module contains classes responsible for displaying the results
of the computations.

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
from plotly.graph_objs import Figure, Scatter

import data

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
BOOK_COLOUR = 'rgb(89, 205, 105)'
USER_COLOUR = 'rgb(105, 89, 205)'


def visualize_graph(graph_tuple: tuple[data.Graph, data.WeightedGraph],
                    start: str, end: str,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '', weighted: bool = False) -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    if weighted:
        graph = graph_tuple[1]
    else:
        graph = graph_tuple[0]

    graph_nx = graph.conv_networkx(max_vertices)
    pos = getattr(nx, layout)(graph_nx)
    nx.set_node_attributes(graph_nx, pos, 'pos')

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    x_edges = []
    y_edges = []
    path = graph.get_friend_path(start, end)  # TODO check if returns list of edges (tuples of items)
    x_highlight_edges = []
    y_highlight_edges = []

    for edge in graph_nx.edges:
        if edge in path:
            x_highlight_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_highlight_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
        else:
            x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
            y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace_highlight = Scatter(x=x_highlight_edges,
                              y=y_highlight_edges,
                              mode='lines',
                              name='edges',
                              line=dict(color='rgb(255,0,0)', width=1),
                              hoverinfo='none',
                              )

    trace_edges = Scatter(x=x_edges,
                          y=y_edges,
                          mode='lines',
                          name='edges',
                          line=dict(color='rgb(255,185,185)', width=1),
                          hoverinfo='none',
                          )

    trace_nodes = Scatter(x=x_values,
                          y=y_values,
                          mode='markers',
                          name='nodes',
                          marker=dict(symbol='circle-dot',
                                      size=5,
                                      color='rgb(0,0,128)',
                                      line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                      ),
                          text=labels,
                          hovertemplate='%{text}',
                          hoverlabel={'namelength': 0}
                          )

    data1 = [trace_highlight, trace_edges, trace_nodes]

    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)
