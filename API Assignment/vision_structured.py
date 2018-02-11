import io
import os
import PIL
import glob
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
	file_name = []
	for filename in glob.glob('resources/*.jpg'): 
	    im=Image.open(filename)
	    file_name.append(im)

	
def label_images():
	print('Labels and Landmarks:')
	for i in length(file_name):
		with io.open(file_name[i], 'rb') as image_file:
		    content = image_file.read()
		image = types.Image(content=content)
		response1 = client.label_detection(image=image)
		labels = response1.label_annotations
		for label in labels:
    		print(label.description)
    		print(landmark.description)
    		draw = ImageDraw.Draw(im)
    		draw.text((0, 0),label.description,(255,255,0),font=font)
    		draw.text((0, 0),landmark.description,(255,255,0),font=font)
    		draw = ImageDraw.Draw(im1)
    		im1.save('%s.jpg' % (file_name + str(uuid.uuid4())))










