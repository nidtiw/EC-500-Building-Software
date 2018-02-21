import tweepy
from tweepy import OAuthHandler
import json
import wget

consumer_key = '************************'
consumer_secret = '******************************************'
access_token = '*************************************************'
access_secret = '******************************************************'

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

tweets = api.user_timeline(screen_name='Comey',
                           count=20, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id

while (True):
    more_tweets = api.user_timeline(screen_name='Comey',
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

for i, media_file in enumerate(media_files):
    wget.download(media_file, out= "%s/%d.jpg" % ('results', i))

subprocess.call("ffmpeg -i results/%d.jpg -vf scale=320:240 results/out_%d.jpg ", shell=True)
subprocess.call("ffmpeg -r 1 -i results/out_%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p results/test.mp4", shell=True)