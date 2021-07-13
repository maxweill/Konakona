## Twitter Screenshot Bot
This is a python script that runs as the back end of a twitter 'screenshot' bot. It works by first parsing through a directory and selecting a video. It then generates a screenshot at a random time from that video, and uploads it to twitter.

The bot also has the ability to parse through multiple directories, so you can give it a larger organized selection of videos to choose from. 

Take note that if you have a directory in the same hierarchical level as video files, it is significantly more likely that you will pull from the videos rather than parse the directory, since the bot stops parsing once it finds a video.

![Explanation](/help_diagram.png)

Additionally, rather than a screenshot, the bot can also generate videos from the source material.

### How To Use

First, get the requirements with:\
`pip install -r requirements.txt`

YouI personally run the bot as a cronjob on my home server. There are other solutions to do this, but I simply have the bot run every 30 minutes using the cronjob. It looks something like this.\

**On Linux:**
`*/30 * * * * python3 run.py`

**TODO:**
Windows/Mac

### Configuration
At the top of the **run.py** file are several lines of configuration. You will need to set these up in order for the bot to function.
#### Config Variables
*directory* - String. The path to your videos, or your folder of (folders of...) videos. Should end with a '/'.

*clip_length* - Integer. This is what the length of an outputted video clip will be, in seconds.

*video_chance* - Number. A number between 0 and 1, representing the percentage of the time the bot will produce a video instead of producing a screenshot. Set to 0 to never produce a video. Set to 1 to produce a video every time.

#### API Keys
There are also API keys that you must fill out. You will need to sign up for a twitter developer account in order to gain access to these. For more info, see Twitter's website. https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

 
