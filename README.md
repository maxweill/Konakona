## Anime Twitter Bot uwu
The 'bot' is really a simple script that runs every 30 minutes on my computer.
It randomly selects a lucky star episode file from my folder, randomly generates a timestamp for that video file,
and then generates a screenshot at that time, and uploads it to twitter.
There is no duplicate checking or anything else, it's all completely 100% random.
In more technical terms, it is a python script run by a cronjob every 30 minutes,
that uses ffmpeg, and the twitter dev apis to generate and upload a screenshot.
I didn't put a lot of work into the code or other solutions because this gets the job done, and I am lazy.
Please feel free to use it as you wish for your own bot.

### Setup

Get the requirements with:
`pip install -r requirements.txt`

To run the code every 30 minutes use cronjob. It should look something like this.\

**On Linux:**
`*/30 * * * * python3 run.py`