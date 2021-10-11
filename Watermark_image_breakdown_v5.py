#!/usr/bin/env python
# coding: utf-8

# <H2> Code Breakdown </H2>
# "C:/Users/nnour/Desktop/!dev/threading/images/test.jpg"
# infile_path = "928.jpg"
# input("Enter the image file path : ")
# hello
# Constants
# INPUT_IMAGE_FILE = infile_path
# OUTPUT_IMAGE_FILE = infile_path + ".convert23ed.png"
import time

import os
from PIL import Image, ImageDraw, ImageFont
# directory = r'C:\Users\nnour\Desktop\!dev\watermark\watermark\IMAGES2'
import PySimpleGUI as sg


FONT_LOCATION = "calibrib.ttf"
FONT_SIZE = 80
H_SPACING = 70
V_SPACING = 90
FONT_OPACITY = 75
WATERMARK_TEXT = " COPYRIGHT @ TNB 2020 "

# Importing essential packages from PIL


# opening image
def watermarking(img_path, file_name, font_opacity, font_size, watermark_text):
    #output_result = img_path
    img_path2 = img_path + "/result" #os.path.join(img_path, "/result")
    if not os.path.exists(img_path2):
        os.makedirs(img_path2)
    OUTPUT_IMAGE_FILE = os.path.join(img_path2, file_name) + ".watermark.jpg"
    FONT_LOCATION = "calibrib.ttf"
    FONT_SIZE = int(font_size)  # 80
    H_SPACING = 70
    V_SPACING = 90
    FONT_OPACITY = int(font_opacity)  # 75
    WATERMARK_TEXT = watermark_text  # " COPYRIGHT @ TNB 2020 "

    INPUT_IMAGE_FILE =  os.path.join(img_path, file_name) #img_path
    im = Image.open(INPUT_IMAGE_FILE)
    font = ImageFont.truetype(FONT_LOCATION, FONT_SIZE)
    watermark_text = WATERMARK_TEXT
    im_width, im_height = im.size  # gathering parent image size

    # Creating editable image
    drawing = ImageDraw.Draw(im)
    text_width, text_height = drawing.textsize(watermark_text, font)  # gathering size of the text

    # Initializing text watermark sub image
    im_text = Image.new('RGBA', (text_width, text_height),
                        (255, 255, 255, 0))  # creating new transparent sub image for watermark text
    drawing = ImageDraw.Draw(im_text)
    drawing.text((0, 0), watermark_text, fill=(255, 255, 255, FONT_OPACITY),
                 font=font)  # adding the text to the new sub-image

    current_width = im_width
    current_height = im_height

    up_down = +1  # for interesting tiling pattern ( up down position difference )

    # Looping for additional watermarks
    new_position = (current_width - text_width) - H_SPACING, current_height + (up_down * (V_SPACING // 2))
    # top ling
    im.paste(im_text, (0, 0), im_text)  # pasting the watermark on the parent image
    im.paste(im_text, (1600, 0), im_text)
    im.paste(im_text, (3200, 0), im_text)
    im.paste(im_text, (4800, 0), im_text)
    im.paste(im_text, (6400, 0), im_text)

    # middle line
    im.paste(im_text, (0, 2000), im_text)  # pasting the watermark on the parent image
    im.paste(im_text, (1600, 2000), im_text)
    im.paste(im_text, (3200, 2000), im_text)
    im.paste(im_text, (4800, 2000), im_text)
    im.paste(im_text, (6400, 2000), im_text)

    print("values insaide the funcation are")
    print(font_opacity, font_size, watermark_text)
    im.save(OUTPUT_IMAGE_FILE, 'JPEG')


# bottom horizontal watermark line repeat
# while current_width > text_width + H_SPACING:
#     new_position = (current_width - text_width) - H_SPACING, current_height + (up_down * (V_SPACING // 2))
#     im.paste(im_text, new_position, im_text)  # pasting the watermark on the parent image
#     current_width, current_height = new_position
#
#     # Creating vertical repeat for each horizontal one in the bottom line
#
#     repeat_current_width, repeat_current_height = new_position
#
#     while repeat_current_height > text_height + V_SPACING:
#         repeat_new_position = repeat_current_width, (repeat_current_height - text_height - V_SPACING)
#         im.paste(im_text, repeat_new_position, im_text)  # pasting the watermark on the parent image
#         repeat_current_width, repeat_current_height = repeat_new_position
#
#     up_down *= -1

# saving output to outfile


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="Folder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(20, 10), key="File List"
        )
    ],
]

image_viewer_column = [
    [sg.Text("Watermark Software")], [sg.Button("start"), sg.Button("Exit")],
]

image_edit_values = [
    [sg.Text("Font opacity      "), sg.InputText(size=(20, 10), key="font_opacity", default_text=75)], [sg.Text("Font Size          ")
        , sg.InputText(size=20, key="font_size", default_text=80)],
    [sg.Text("Water Mark Text"), sg.InputText(size=20, key="watermark_text", default_text='Copyright © TNB 2020')]
]

layout = [
    [
        # sg.Text("Hello this watermark software")], [sg.Button("start")], [sg.Button("Exit")],
        sg.Column(file_list_column), sg.VSeperator(), sg.Column(image_edit_values),
        sg.VSeperator(), sg.Column(image_viewer_column),

    ]
]
folder = ""
# Create the window
window = sg.Window("Watermark By Nour", layout)
#i = 0
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    value_font_opacity = values['font_opacity']
    value_font_size = values['font_size']
    value_watermark_text = values['watermark_text']

    if event == "Folder":

        folder = values["Folder"]
        print(folder)
        try:
            file_list = os.listdir(folder)
            print(file_list)
        except:
            file_list = []

    if event == "start":  # or event == sg.WIN_CLOSED:
        # break
        if folder:
            directory = folder
            print(directory)
        else:
            directory = r'C:\Users\nnour\Desktop\!dev\watermark\watermark\IMAGES3'

        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # path = os.path.join(directory, filename)
                #directory = directory + "/result"
                print(os.path.join(directory, filename))
                #os.path.join(directory, filename)
                watermarking(directory, filename, value_font_opacity, value_font_size, value_watermark_text)
                named_tuple = time.localtime()
                time_string = time.strftime("Time: %H:%M:%S", named_tuple)
                done = ["Finised " + time_string]
                window["File List"].update(done)
               # i += 1
            # else:

            # else:
            # continue

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
