import io
import os
import PIL
import glob
import uuid
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

font = ImageFont.truetype("arial.ttf", 28, encoding="unic")

# Instantiates a client
client = vision.ImageAnnotatorClient()


def get_images():
    # file_name = []
    for filename in glob.glob('resources/*.jpg'): 
        im=Image.open(filename)
        # file_name.append(im)
        label_list = []
        landmark_list = []
        print('Labels and Landmarks:')
        # for i in len(file_name):
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response1 = client.label_detection(image=image)
        labels = response1.label_annotations
        response2 = client.landmark_detection(image=image)
        landmarks = response2.landmark_annotations
        for label in labels:
            print(label.description)
            label_list.append(label.description)
        label_string = '| '.join(label_list)
        draw = ImageDraw.Draw(im)
        draw.text((0, 25),label_string,(255,255,255,255),font=font)
        for landmark in landmarks:
            print(landmark.description)
            landmark_list.append(landmark.description)
        landmark_string = '| '.join(landmark_list)
        draw.text((0, 45),landmark_string,(255,255,255,255),font=font)
        draw = ImageDraw.Draw(im)
        im.save('%s.jpg' % (filename + str(uuid.uuid4())))

get_images()










