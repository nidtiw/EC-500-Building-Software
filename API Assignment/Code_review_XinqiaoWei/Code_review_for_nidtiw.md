Code review:
https://github.com/nidtiw/EC-500-Building-Software/tree/master/API%20Assignment

The flow for this program:
1. Get image url from tweepy api .
2. Download the image using wget in to a file called results.
3. Use FFMPEG to resize the image and saved in a file called resized.
4. Use Google cloud vision api to label the image and add text on top of the images and saved in the resized file as file_%

API Calls:
The API calls of twitter and google cloud vision works well under general situation. Twitter api uses tweepy which require extra library and left the developer’s personal accessing key in the program. For google cloud vision api, it need developers’ auth key.

Readability/Syntax Convention:
The syntax of the code is easy to understand. However, if the coder provide more comments on the google cloud vision api part would be great.


Error handling:
The coder doesn’t provide any personal error handle case only the default with the api.

It is quite hard to write a test program on the code. Hence I just try different error could happen on top of the original code.

1.Wrong twitter api key:
“tweepy.error.TweepError: [{'code': 32, 'message': 'Could not authenticate you.’}]” This is the default error by tweepy.

2.Twitter account without image I insert my own twitter account @AngelaBubble, the error I got is: “Traceback (most recent call last):
  File "vision_structured.py", line 47, in <module>
    last_id = tweets[-1].id
IndexError: list index out of range” 	which is still the default error message.
3. No google cloud vision auth key 	“    raise exceptions.DefaultCredentialsError(_HELP_MESSAGE)
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials. Please set GOOGLE_APPLICATION_CREDENTIALS or
explicitly create credential and re-run the application. For more
information, please see
https://developers.google.com/accounts/docs/application-default-credentials.”


Extra file:
It would be great if the coder provide “arial.ttf” in file, otherwise, it would shows: ”OSError: cannot open resource”


