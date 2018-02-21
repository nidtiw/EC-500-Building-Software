import tweepy
from tweepy import OAuthHandler
import json
import wget
import subprocess
import io
import os
import PIL
import glob
# import uuid
# import cv2
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name='ugh_7',
                           count=20, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id
 
while (True):
    more_tweets = api.user_timeline(screen_name='ugh_7',
                                count=20,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)
# There are no more tweets
    if (len(more_tweets) == 0):
        break
    else:
        last_id = more_tweets[-1].id-1
        tweets = tweets + more_tweets

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])

# for media_file in media_files:
#     wget.download(media_file)

subprocess.call("mkdir results", shell=True)
subprocess.call("mkdir resized", shell=True)

for i, media_file in enumerate(media_files):
    wget.download(media_file, out= "%s/%d.jpg" % ('results', i))

subprocess.call("ffmpeg -i results/%d.jpg -vf scale=1000:1000 resized/out_%d.jpg ", shell=True)

# Using vision API to annotate the images:
font = ImageFont.truetype("arial.ttf", 16, encoding="unic")

# Instantiates a client
client = vision.ImageAnnotatorClient()


def get_images():
    # file_name = []
    for i, filename in enumerate(glob.glob('resized/*.jpg')): 
        print(i, filename)
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
            # print(label.description)
            label_list.append(label.description)
        label_string = '| '.join(label_list)
        print(label_string)
        draw = ImageDraw.Draw(im)
        draw.text((0, 25),label_string,(255,255,255,255),font=font)
        for landmark in landmarks:
            # print(landmark.description)
            landmark_list.append(landmark.description)
        landmark_string = '| '.join(landmark_list)
        print(landmark_string)
        draw.text((0, 50),landmark_string,(255,255,255,255),font=font)
        draw = ImageDraw.Draw(im)
        im.save('%s/file_%d.jpg' % ('resized', i))

        # name_of_file = "results/file_%d.jpg" %d
        # cv2.imwrite(name_of_file, im)
        # im.save('results/ann_%d.jpg' %d )




# if "__init__" == "__main__":
get_images()
# subprocess.call("ffmpeg -r 1 -i results/ann_%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p results/test.mp4", shell=True)
subprocess.call("ffmpeg -r 1 -i resized/file_%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p resized/test.mp4", shell=True)

