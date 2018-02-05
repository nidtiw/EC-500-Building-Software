import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'resources/lombardy_SF.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

response = client.landmark_detection(image=image)
landmarks = response.landmark_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)

print('Landmarks:')

for landmark in landmarks:
	print(landmark.description)
	for location in landmark.locations:
		lat_lng = location.lat_lng
		print('Latitude'.format(lat_lng.latitude))
		print('Longitude'.format(lat_lng.longitude))

		
