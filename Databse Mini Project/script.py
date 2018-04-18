import tweepy
from tweepy import OAuthHandler
import json
import wget
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
import glob
from google.cloud import vision
from google.cloud.vision import types
import io
import os

consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET_KEY'
access_token = 'YOUR_ACCESS_TOKEN'
access_secret = 'YOUR_SECRET_ACCESS_TOKEN'

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

username = sys.argv[1]
count = sys.argv[2]
#print(username)

tweets = api.user_timeline(screen_name=username,
                           count=count, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id
 
media_files = set()
mediaURLs = []
imageCount = 0
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])
        mediaURLs.append(media[0]['media_url'])
        imageCount += 1
    elif(len(media) == 0):
        print("no media files found")

subprocess.call("mkdir results", shell=True)
subprocess.call("mkdir resized", shell=True)

for i, media_file in enumerate(media_files):
    wget.download(media_file, out= "%s/%d.jpg" % ('results', i))

subprocess.call("ffmpeg -i 'results/%d.jpg' -vf scale=320:240 'resized/out_%d.jpg' ", shell=True)


font = ImageFont.load_default()
#ImageFont.truetype("")


# Instantiates a client
client = vision.ImageAnnotatorClient()

from collections import defaultdict
labels_dict = defaultdict(lambda: " ")
def get_images():
    for i, filename in enumerate(glob.glob('resized/*.jpg')): 
        #print(i, filename)
        parsedFilename = filename.split(".")
        key = parsedFilename[0]
        im=Image.open(filename)
        # file_name.append(im)
        label_list = []
        landmark_list = []
        texts_list = []
        # print('Labels:')
        # for i in len(file_name):
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        
        response1 = client.label_detection(image=image)
        labels = response1.label_annotations
        response2 = client.landmark_detection(image=image)
        landmarks = response2.landmark_annotations
        response3 = client.text_detection(image=image)
        texts = response3.text_annotations
        
        for text in texts:
            # print(landmark.description)
            texts_list.append(text.description)
        text_string = '**'.join(texts_list)
       
        draw = ImageDraw.Draw(im)
        draw.text((0, 75),text_string,(255,255,255,255),font=font)
        for label in labels:
            # print(label.description)
            label_list.append(label.description)
        label_string = ' ** ' .join(label_list)
        
        labels_dict[key] = label_string
        #print('Labels:')
        #print(label_string)
        #print('\n')
        draw = ImageDraw.Draw(im)
        draw.text((0, 25),label_string,(255,255,255,255),font=font)
        for landmark in landmarks:
            # print(landmark.description)
            landmark_list.append(landmark.description)
        landmark_string = '**'.join(landmark_list)
        print('Landmarks:')
        print(landmark_string)
        #print('\n')
        draw = ImageDraw.Draw(im)
        draw.text((0, 50),landmark_string,(255,255,255,255),font=font)
        im.save('%s/file_%d.jpg' % ('resized', i))

get_images()
subprocess.call("ffmpeg -r 1 -i 'resized/file_%d.jpg' -vcodec libx264 -crf 25  -pix_fmt yuv420p 'results/test.mp4'", shell=True)

########################################################################################################################
from pymongo import MongoClient
import json
from pprint import pprint

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.twitter_data
posts = db.posts

#file = open("airports.json","r")
#airports_data = json.load(file)
data = {
    "twitter handle": username,
    "tweets count": count,
    "downloaded media list": mediaURLs,
    "total images": imageCount,
    "labels dictionary": labels_dict

}
posts.insert_one(data)

