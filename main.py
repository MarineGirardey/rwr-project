#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 12:24:43 2021
@author: Marine Girardey
"""
from rwr_functions import *
from tkinter_window_network import *


def main():
    """
    Main function which run the full program
    ----------

    Returns
    ----------
    """

    # ------ PROBABILITY TRANSITION MATRIX ------
    # matrix of a complete directed weighted graph
    matrix_1 = np.matrix([[0, 0.6, 0.2, 0.2],
                          [0.6, 0, 0.3, 0.1],
                          [0.2, 0.6, 0, 0.2],
                          [0.1, 0.6, 0.3, 0]])

    # matrix of a complete undirected weighted graph
    matrix_2 = np.matrix([[0, 0.5, 0.3, 0.2],
                          [0.5, 0, 0.2, 0.3],
                          [0.3, 0.2, 0, 0.5],
                          [0.2, 0.3, 0.5, 0]])

    # matrix of an incomplete directed weighted graph
    matrix_3 = np.matrix([[0, 5/6, 1/6, 0, 0, 0],
                            [1/2, 0, 1/2, 0, 0, 0],
                            [1/6, 2/3, 0, 0, 1/6, 0],
                            [0, 0, 0, 0, 1/6, 5/6],
                            [0, 0, 1/6, 1/6, 0, 2/3],
                            [0, 0, 0, 1/2, 1/2, 0],
                            ])

    # matrix of an incomplete undirected weighted graph
    matrix_4 = np.matrix([[0, 4/7, 3/7, 0, 0, 0],
                            [4/7, 0, 3/7, 0, 0, 0],
                            [3/7, 3/7, 0, 0, 1/7, 0],
                            [0, 0, 0, 0, 3/7, 4/7],
                            [0, 0, 1/7, 3/7, 0, 3/7],
                            [0, 0, 0, 4/7, 3/7, 0],
                            ])

    # Store the matrix size
    matrix_size = len(matrix_3)

    # ------ RWR PARAMETERS ------
    seed_node = 0
    c = 0.25
    number_of_rwr = 1000

    # Do k time a RWR with the specified matrix
    rwr_walks = [random_walk_with_restart(matrix_3, c, seed_node) for k in range(0, number_of_rwr)]

    # ------ FOR TKINTER ------
    # Select the RWR with the highest number of nodes reached
    max_rwr = take_max_rwr(rwr_walks)[0]
    image_numb = take_max_rwr(rwr_walks)[1]

    # Default temporary_folder
    temporary_folder = None
    # Try to create a folder except os error
    try:
        # Create the folder that will contain all network images for the rwr visualisation
        path = os.getcwd()
        temporary_folder = path + "/temporary_folder/"
        os.mkdir(temporary_folder)

        # Create the network with the visualisation of the RWR
        create_graph(matrix_3, seed_node, max_rwr, temporary_folder)

        # ------ FOR THE BAR PLOTS ------
        # Remove the seed from the RWR to not introduce a bias in the results
        for rwr in rwr_walks:
            rwr.pop(0)

        # Execute the function to count the weight of each node
        weight_count = compute_node_weight(rwr_walks)

        # Convert the integer node list into a list of strings
        node_list = convert_node_list(matrix_size, seed_node)

        # Plot the bar plot
        bar_plot(seed_node, node_list, weight_count)

    except OSError:
        print("folder creation error")
        pass

    return temporary_folder, image_numb


if __name__ == '__main__':

    # Run the main function
    my_main = main()

    # Name of the temporary folder
    temp_folder = my_main[0]
    # Number of images to display for the tkinter window
    img_numb = my_main[1]

    # Show the plotted figures
    plt.show()

    # Open the tkinter window
    print("A tkinter window has been opened.")
    tkinter_graph(temp_folder, img_numb)
    print("Tkinter window closed.")

    # Delete the temporary folder (only if the window is closed with the red cross button)
    shutil.rmtree(temp_folder)
