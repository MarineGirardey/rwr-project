#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 12:25:53 2021
@author: Marine Girardey
"""

# Library imports
import matplotlib.pyplot as plt
import networkx as nx
import random
from numpy.random import multinomial
import numpy as np
import os
import shutil


def create_graph(M, seed, rwr_walks, temporary_folder):
    """
    Function which create a graph for each step of the RWR and store it as images.
    ---------
    Arguments
        M : The probability transition matrix
        seed : The start node
        simple_w : A list with the nodes selected for the RWR
        temporary_folder : A temporary folder to store graph images in the tkinter window
    ---------
    Returns
        None
    """

    # Define an initialisation variable
    previous_node = 'initialisation'
    # Define a fixed graph took from a random choice
    pos = random.choice(range(0, 20))
    # Create a graph from the transition matrix (Graph or DiGraph)
    network = nx.from_numpy_matrix(M, create_using=nx.Graph)

    # Browse nodes and information about them in the graph and add the color information
    for u, v in network.nodes(data=True):
        v['color'] = 'lightgrey'

    # Define an iterator to create new pictures names iteratively for each graph
    i = 0
    # Browse each nodes from the RWR walk
    for chosen_node in rwr_walks:

        # Apply a new color to the chosen node to differentiate it
        color_nodes = color_chosen_nodes(network, chosen_node, 'pink')

        # If the node is not the first of the RWR walk and is different than the previous node chosen
        if previous_node != 'initialisation' and previous_node != chosen_node:
            # Than add a weight for the edge between the previous node and the chosen node to visualize the walk
            network[chosen_node][previous_node]['weight'] = 7

        # Store in a list the new weight set for each edges of the RWR
        weights = [network[u][v]['weight'] for u, v in network.edges]

        # Save the network created with the chosen node, the new edge between the new and the previous node
        save_network(network, pos, color_nodes, weights, i, temporary_folder)
        i += 1

        # Reset the network (reset colors to grey) to prepare the next node selection
        color_chosen_nodes(network, chosen_node, 'lightgrey')

        # Define the previous node variable
        previous_node = chosen_node

    # When the for loop has ended, create the last graph which is the return to the seed
    # Remove all weights
    for u, v, w in network.edges(data=True):
        w['weight'] = 0.6
    weights = [network[u][v]['weight'] for u, v in network.edges]
    # Set the color pink to the seed node
    color_nodes = color_chosen_nodes(network, seed, 'pink')
    # Save it
    save_network(network, pos, color_nodes, weights, i, temporary_folder)


def color_chosen_nodes(network, chosen_node, color):
    """
    Function which color a given node
    ---------
    Arguments
        network : The graph
        chosen_node : The chosen node
        color : The color to set
    ---------
    Returns
        color_nodes : A list with the new colored node
    """

    # Color the node selected randomly by RWR
    network.nodes[chosen_node]['color'] = color
    # Create a list with color for each node
    color_nodes = [network.nodes[node]['color'] for node in network.nodes]
    return color_nodes


def save_network(network, pos, color_nodes, weights, i, temporary_folder):
    """
    Function which plot and save a given network
    ---------
    Arguments
        network : The graph
        pos : The defined display of the graph
        color_nodes : The color applied to a chosen node
        weights : The list with weights representing the path of the RWR
        i : The iterator to save network in order with different names
        temporary_folder : The temporary folder to store images during the tkinter display
    ---------
    Returns
        None
    """

    # Plot a save the network without display it
    pos = nx.spring_layout(network, seed=pos, weight=7)
    plt.figure(1)
    plt.title('Random walk on a network')
    nx.draw(network, pos=pos, with_labels=True, node_color=color_nodes, width=weights)
    plt.savefig(temporary_folder + 'plotgraph' + str(i) + '.png', dpi=300, bbox_inches='tight')
    plt.close(1)


def random_walk_with_restart(M, c, i):
    """
    Function which executes a RWR
    ---------
    Arguments
        M : The probability transition matrix
        c : The probability to return to the seed
        i : The chosen node
    ---------
    Returns
        walk : A list with all the chosen nodes for one RWR
    """

    # Begin the RWR from node i (here the seed)
    walk = [i]

    # Repeat the loop while the function doesn't reached the return
    while True:
        # Select a random float between 0 and 1
        r = random.random()
        # If at least 1 walk from the seed
        if len(walk) > 1:
            # If r is <= than the probability to return to the seed then return to the seed and stop the RWR
            if r <= c:
                return walk

        # Store in a variable the line of the matrix corresponding to the node selected by RWR
        vector = M[i, :].tolist()[0]

        # Depending on transition probability from the actual node to another, do a multinomial experiment (Bernoulli
        # scheme with more than 2 results possible) and store the node selected
        # Choose a node randomly depending on probability RANDOM EXPERIMENT
        i = multinomial(1, vector, size=1).tolist()[0].index(1)  # CHANGE SEED

        # Add the node selected by the multinomial experiment to the walk list
        walk.append(i)


def take_max_rwr(rwr_walks):
    """
    Function which return the RWR with the highest number of nodes selected
    ---------
    Arguments
        rwr_walks : A list of RWR lists
    ---------
    Returns
        max_rwr : A list with the highest RWR
        image_numb : The length of the list with the highest RWR
    """
    max_rwr = []
    for rwr in rwr_walks:
        if len(rwr) > len(max_rwr):
            max_rwr = rwr
        else:
            pass
    image_numb = len(max_rwr)

    return max_rwr, image_numb


def compute_node_weight(walks):
    """
    Function which compute the node weight in each RWR
    ---------
    Arguments
        walks : A list of lists with the chosen nodes from the RWR
    ---------
    Returns
        sorted_values_list : A list with all nodes weights sorted in the ascending nodes order (from node 0 to n)
    """

    # Define a dict to count node occurrences
    count = {}
    # Float variable which will be the sum of all nodes
    sum = 0.0
    # The final list
    sorted_values_list = []

    # Browse each random walk realised
    for walk in walks:
        # Browse each node of a random walk
        for i in walk:
            # Do +1 if the node is already in dict
            if i in count.keys():
                count[i] = count[i] + 1.0
            # Insert nodes as key and 0 as the value it is not in dict
            else:
                count[i] = 0

    # Store the sum of all nodes values (number of time each node has been selected by the RWR) in the sum variable
    for val in count.values():
        sum = sum + val

    # Replace value of nodes by the ratio of the number of times a node has been selected to the total nodes selected
    for i in count:
        count[i] = count[i] / sum

    # Insert each node ratio in a list sorted by nodes (from 0 to n)
    for i in range(0, max(count.keys()) + 1):
        sorted_values_list.append(count[i])

    return sorted_values_list


def bar_plot(seed, node_list, count):
    """
    Function which draw a bar plot of the node weights for a giver graph after a RWR associated to a seed node
    ---------
    Arguments
        seed : The start node of the RWR
        node_list : The list of node names
        count : A dictionary with node weights for each nodes
    ---------
    Returns
        None
    """

    # Plot a the figure number 2
    plt.figure(2, figsize=(14, 14), dpi=80)
    # Put all colors in a list
    all_colors = list(plt.cm.colors.cnames.keys())

    color_list = []
    # For each node select a random color in the color list and put it in a list of color for each node
    for elem in node_list:
        c = random.choices(all_colors)[0]
        color_list.append(c)

    # Used for my report results (["lightcoral", "lightseagreen", "plum", "lightskyblue"])
    # Plot the bar plot
    plt.bar(node_list, count, color=color_list, width=.3)

    # Plot the text above the bar
    for i, val in enumerate(count):
        plt.text(i, val, float(round(val, 3)), horizontalalignment='center', verticalalignment='bottom',
                 fontdict={'fontweight': 500, 'size': 20})

    # Decoration
    plt.xticks(fontsize=20, rotation=60, horizontalalignment='right')
    plt.yticks(fontsize=20, rotation=60, horizontalalignment='right')
    plt.title("Weights of nodes with node " + str(seed) + " as the seed after a RWR simulation", fontsize=24)
    plt.ylabel('Node weights', fontsize=24)
    plt.xlabel('Nodes', fontsize=24)
    plt.ylim(0, max(count) + 0.05)


def convert_node_list(matrix_size, seed_node):
    """
    Function which convert the list of integer nodes in list of string nodes
    ---------
    Arguments
        matrix_size : The size of the matrix to iterate
        seed_node : The seed node to differentiate this node from the others
    ---------
    Returns
        node_list : The list of string nodes
    """

    node_list = []
    for i in range(0, matrix_size):
        if i == seed_node:
            node_list += ["Seed " + str(i)]
        else:
            node_list += ["Node " + str(i)]

    return node_list
