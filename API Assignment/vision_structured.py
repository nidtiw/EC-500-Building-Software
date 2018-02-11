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
	for i in length(file_name):
		with io.open(file_name, 'rb') as image_file:
		    content = image_file.read()



