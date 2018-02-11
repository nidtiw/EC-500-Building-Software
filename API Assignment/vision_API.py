import io
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

font = ImageFont.truetype("arial.ttf", 28, encoding="unic")


# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'resources/Angkor-wat-cambodia.jpg')

im1=Image.open(file_name)

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)


# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

label_list = []

response = client.landmark_detection(image=image)
landmarks = response.landmark_annotations

print('Labels:')
for label in labels:
    print(label.description)
    label_list.append(label.description)
label_string = ' '.join(label_list)
draw = ImageDraw.Draw(im1)
draw.text((0, 0),label_string,(255,255,0),font=font)
draw = ImageDraw.Draw(im1)

im1.save("marked_image.jpg")

print('Landmarks:')

for landmark in landmarks:
	print(landmark.description)
	for location in landmark.locations:
		lat_lng = location.lat_lng
		print('Latitude'.format(lat_lng.latitude))
		print('Longitude'.format(lat_lng.longitude))



