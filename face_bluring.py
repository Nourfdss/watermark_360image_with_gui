from facenet_pytorch import MTCNN
import torch
import numpy as np
import mmcv, cv2
from PIL import Image, ImageDraw
from IPython import display
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import PySimpleGUI as sg
# Function for bluring purpose
import time

def make_ellipse_mask(size, x0, y0, x1, y1, blur_radius):
    img = Image.new("L", size, color=0)
    draw = ImageDraw.Draw(img)
    draw.ellipse((x0, y0, x1, y1), fill=255)
    return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

# TO get the value different between the our image and developer image


def scale_cords_scalefill(scaled_img_shape, coords, org_img_shape):
    hr = scaled_img_shape[0] / org_img_shape[1]
    wr = scaled_img_shape[1] / org_img_shape[0]

    print('hr ' + str(hr))
    print('wr ' + str(wr))

    # coords[:, [0, 1]] /= wr
    # coords[:, [1, 0]] /=hr
    # , coords[1][0]
    # , coords[1][1]
    coords[0][1] /= wr  # ymin
    coords[1][1] /= wr  # ymax

    coords[0][0] /= hr  # xmin
    coords[1][0] /= hr  # xmax
    return coords


#
# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# print('Running on device: {}'.format(device))
#
# mtcnn = MTCNN(keep_all=True, device=device)
#
# # video = mmcv.VideoReader('video.mp4')
# # frames_tracked = []
# # frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]
# # img = mmcv.imread('test.bmp') # 1232*1024
# name = '871.jpg'
# img = mmcv.imread(name)
#
# # img = mmcv.imrotate(img, 90)
# # print(img.show())
# # mmcv.imresize_like(img, frames[0], return_scale=False)
# # print(img)
# img = mmcv.imresize(img, (1920, 1080))
# # mmcv.imresize(img, (1920, 1080), return_scale=False)
# # print(img)
# img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#
# # print(img)
# # print(frames[0])
# boxes, _ = mtcnn.detect(img)
# print(boxes[0][0])
#
# # display.Video('video.mp4', width=640)
# frame_draw = img.copy()
# draw = ImageDraw.Draw(frame_draw)
# # box2 = []
# for box in boxes:
#     # draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
#     # draw.ellipse((box[0], box[1], box[2], box[3]), fill=0)
#     print(box)
#     img2 = mmcv.imread(name)
#     box2 = np.array(box)
#     box2 = box2.reshape(2, 2)
#     print(box2)
#     print(img2.shape)
#     print(frame_draw.size)
#     cropped_image = frame_draw.crop((box[0], box[1], box[2], box[3]))
#     blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(radius=20))
#     # draw.filter(ImageFilter.GaussianBlur(radius=5))
#     # frame_draw = make_ellipse_mask(frame_draw.size, box[0], box[1], box[2], box[3], 5)
#     # print(box[0])
#     # draw.filter(ImageFilter.BoxBlur(5))
#
# # Add to frame list
# # frames_tracked.append(frame_draw.resize((640, 360), Image.BILINEAR))
# # d = display.display(frames_tracked[0], display_id=True)
# print(cropped_image.show())
# cropped_image.show()
# d = display.display(cropped_image, display_id=True)
# d = display.display(blurred_image, display_id=True)
# # print(frames_tracked[0].show())
# # frame_draw.show()
# # img = mmcv.imresize(frame_draw, (640, 360))
#
# values = scale_cords_scalefill(frame_draw.size, box2, img2.shape)
# print("the values are" + str(values))
# img4 = Image.open(name)
# # d = display.display(img4, display_id=True)
# # img4.show()
# img4.size
# # 3581.3015 5069.2354 3611.5146 5189.422
# img3 = img4.crop((int(values[0][0]), int(values[0][1]), int(values[1][0]), int(values[1][1])))
# # img3 = img4.crop((7134, 2505, 7257, 2614))
# img5 = img4.crop((int(values[0][0]), int(values[0][1]), int(values[1][0]), int(values[1][1])))
# print(values[0][0], values[0][1], values[1][0], values[1][1])
# # d = display.display(img3, display_id=True)
# d = display.display(img5, display_id=True)
# blurrred_image = img3.filter(ImageFilter.GaussianBlur(radius=20))
# d = display.display(blurrred_image, display_id=True)
# img4.paste(blurrred_image,
#            (int(values[0][0]), int(values[0][1]), int(values[1][0]), int(values[1][1])))  # (7134, 2505, 7257, 2614)
# d = display.display(img4, display_id=True)
# # img3.show()
# img4.save("new_ImageDraw_blurred.jpg")
# print('done')
# image_name = '871.jpg'

# Detecting the faces and blur them for privacy purpose

# TODO: create a saveing file location
def face_detection_bluring(img_path, name):
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('Running on device: {}'.format(device))

    mtcnn = MTCNN(keep_all=True, device=device)

    face_detected = img_path + "/face_detected" #os.path.join(img_path, "/result")
    face_not_detected = img_path + "/face_not_detected"
    if not os.path.exists(face_detected):
        os.makedirs(face_detected)
    if not os.path.exists(face_not_detected):
        os.makedirs(face_not_detected)
    OUTPUT_IMAGE_FILE = os.path.join(face_detected, name) + ".blured.jpg"
    OUTPUT_IMAGE_FILE2 = os.path.join(face_not_detected, name) + ".not_blured.jpg"

    # name = '871.jpg'
    img_ogr = mmcv.imread(os.path.join(img_path, name))
    img = mmcv.imresize(img_ogr, (1920, 1080))
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    boxes, _ = mtcnn.detect(img)
    # print(boxes[0][0])
    frame_draw = img.copy()
    draw = ImageDraw.Draw(frame_draw)
    # box2 = []
    name = os.path.join(img_path, name)
    if boxes is None:
        img_orgi = Image.open(os.path.join(img_path, name))
        img_orgi.save(OUTPUT_IMAGE_FILE2)
        pass
    else:
        for box in boxes:
            img2 = mmcv.imread(name)
            box2 = np.array(box)
            box2 = box2.reshape(2, 2)
            # print(box2)
            # print(img2.shape)
            # print(frame_draw.size)
            cropped_image = frame_draw.crop((box[0], box[1], box[2], box[3]))
            blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(radius=20))
            values = scale_cords_scalefill(frame_draw.size, box2, img2.shape)
            # print("the values are" + str(values))
            img4 = Image.open(name)
            img3 = img4.crop((int(values[0][0]), int(values[0][1]), int(values[1][0]), int(values[1][1])))
            img5 = img4.crop((int(values[0][0]), int(values[0][1]), int(values[1][0]), int(values[1][1])))
            print(values[0][0], values[0][1], values[1][0], values[1][1])
            # d = display.display(img5, display_id=True)
            blurrred_image = img3.filter(ImageFilter.GaussianBlur(radius=20))
            # d = display.display(blurrred_image, display_id=True)
            img4.paste(blurrred_image,
                       (int(values[0][0]), int(values[0][1]), int(values[1][0]),
                        int(values[1][1])))  # (7134, 2505, 7257, 2614)
            # d = display.display(img4, display_id=True)
            # img3.show()
            img4.save(OUTPUT_IMAGE_FILE)
            print('done')

    #cropped_image.show()
    #d = display.display(cropped_image, display_id=True)
    #d = display.display(blurred_image, display_id=True)


file_list_column = [
    [
        sg.Text("Input Image Folder"),
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
    [sg.Text("Face Bluring Software")], [sg.Button("start"), sg.Button("Exit")],
]

image_edit_values = [
    [sg.Text("Font Opacity      "), sg.InputText(size=(20, 10), key="font_opacity", default_text=75)],
    [sg.Text("Font Size          ")
        , sg.InputText(size=20, key="font_size", default_text=80)],
    [sg.Text("Water Mark Text"), sg.InputText(size=20, key="watermark_text", default_text='Copyright © TNB 2020')]
]

layout = [
    [
        # sg.Text("Hello this watermark software")], [sg.Button("start")], [sg.Button("Exit")],
        sg.Column(file_list_column), sg.VSeperator(), sg.Column(image_viewer_column),   # sg.VSeperator(), sg.Column(image_edit_values),

    ]
]

window = sg.Window("FaceBluring By Nour", layout)

def main():
    folder = ""

    while True:

        event, values = window.read()

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
                directory = r'C:\Users\nnour\Desktop\!dev\watermark\facebluring\test'

            directory = r'C:\Users\nnour\Desktop\!dev\watermark\facebluring\test'

            for filename in os.listdir(directory):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    # path = os.path.join(directory, filename)
                    # directory = directory + "/result"
                    print(os.path.join(directory, filename))
                    face_detection_bluring(directory, filename)
                    named_tuple = time.localtime()
                    time_string = time.strftime("Time: %H:%M:%S", named_tuple)
                    done = ["Finised " + time_string]
                    window["File List"].update(done)
        #
    # directory = r'C:\Users\nnour\Desktop\!dev\watermark\facebluring\test'
    #
    # for filename in os.listdir(directory):
    #     if filename.endswith(".jpg") or filename.endswith(".png"):
    #         # path = os.path.join(directory, filename)
    #         # directory = directory + "/result"
    #         print(os.path.join(directory, filename))
    #         face_detection_bluring(directory, filename)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

if __name__ == "__main__":
    main()
