#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:57:12 2021
@author: Marine Girardey
"""

# Library imports
import tkinter as tk
from PIL import ImageTk, Image

# Define an iterator i to display each images in the right order (0 is the default/first image)
i = 0


def tkinter_graph(folder, image_numb):
    """
    Function which display a tkinter window to visualize a RWR from graph images (sorted by names) with RWR steps
    ---------
    Arguments
        temporary_folder : The folder which contain graph images
        image_numb : An integer with the number of images to display
    ---------
    Returns
        None
    """

    # Create the tkinter window and set up it size
    racine = tk.Tk()
    racine.geometry("800x500")
    # Execute the change_i function with his arguments if the "Next Image" button is pressed
    next_img_but = tk.Button(racine, text="Next Image", fg="blue", command=lambda: change_i(racine, folder, label1, image_numb))
    # Create the first graph image object (here "plotgraph0.png") but you can change it into a modular variable
    img = Image.open(folder + "plotgraph0.png")
    # Redefine ing to resize the image
    img = img.resize((450, 350), Image.ANTIALIAS)
    # To prevent the image garbage collected
    racine.img = img
    # The image object is ready
    img = ImageTk.PhotoImage(img)

    # create a label object and attach the image to it
    label1 = tk.Label(image=img)
    label1.image = img
    # Display the widgets
    next_img_but.pack()
    label1.pack()
    # Repeat the tkinter window display while not closed
    racine.mainloop()


def change_i(racine, temporary_folder, label1, image_numb):
    """
    Function which change the value of the i variable
    ---------
    Arguments
        racine : Store the tkinter window
        temporary_folder : The folder which contain graph images
        label1 : The label which display images
        image_numb : An integer with the number of images to display
    ---------
    Returns
        None
    """
    # Define i as a global variable
    global i
    # Add +1 to i to display the next image
    i = i + 1
    # If i is equal to the number of images (means that the last image have to be displayed = seed return)
    if i == image_numb:
        seed_text = tk.Label(text="retrun to the seed")
        seed_text.pack()
    # If i is greater than the number of images to display, than do nothing (the end of the program)
    if i > image_numb:
        pass
    # In other cases, execute the function to display the next image (depending on the value of i)
    else:
        next_image(racine, temporary_folder, label1)


def next_image(racine, temporary_folder, label1):
    """
    Function which display the next image by changing the label configurations
    ---------
    Arguments
        racine : Store the tkinter window
        temporary_folder : The folder which contain graph images
        label1 : The label which display images
    ---------
    Returns
        None
    """

    # Get the image corresponding to the value of i
    img = Image.open(temporary_folder + "plotgraph" + str(i) + ".png")
    # Repeat the procedure made for the first display
    img = img.resize((450, 350), Image.ANTIALIAS)
    racine.img = img
    img = ImageTk.PhotoImage(img)
    # Configure the label1 with the new img and display the widget
    label1.configure(image=img)
    label1.image = img
    label1.pack()
