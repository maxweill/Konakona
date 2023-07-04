## Konakona - An Automated Twitter Screenshot/Video Bot
Konakona is a generic twitter screenshot / video posting bot written in Python. This project was originally developed for [@LuckyStarPicBot](https://twitter.com/LuckyStarPicBot).

### What is this?
This bot was written in order to generate a constant stream of content for a Twitter bot that avoids the overhead of manual uploads or pre-clipping images and video files.

It works by first parsing through a directory and selecting a video. It then uses ffmpeg to generate a screenshot at a random time from that video, then uploads it to twitter.

The bot also has the ability to parse through multiple directories, so you can give it a larger organized selection of videos to choose from. 

Take note that if you have a directory in the same hierarchical level as video files, it is significantly more likely that you will pull from the videos rather than parse the directory, since the bot stops parsing once it finds a video.

![Explanation](/konakona/data/help_diagram.png)

Additionally, rather than a screenshot, the bot can also generate videos from the source material.

Currently, the bot is capable of finding and parsing MKV, MP4, and AVI video files. 

Other file types can be manually added in the function **get_random_video_filepath** at your own risk.

### How To Use

#### Linux

**First**, you will need FFMPEG. This is tested with version n4.4, but will probably work fine with older versions.

**Second**, get the python requirements with:

```
pip install -r requirements.txt
```

**Third**, you will need a method of running the script at your specified intervals. 
I personally run the bot as a cronjob on my home server. My job config is set to run at 30 minute intervals and looks something like this:

```
*/30 * * * * python3 konakona.py
```

**Finally**, set up the configuration file.

#### Configuration
In the same directory as the konakona.py script is a configuration file, **settings.cfg**. You will need to modify this file in order for the bot to function.
##### Config Variables
The settings.cfg file contains a JSON-like structure of variables. Of these variables, please note:

| 'general' tree  | data-type | description                                                  |
| --------------- | --------- | ------------------------------------------------------------ |
| directory       | String    | The path to your videos, or your folder of (folders of...) videos. **Should end with a '/'.** |
| save            | Boolean   | Choose whether images/clips should be saved or not. Output files get renamed and moved to the media folder. The format of the filename is %Y%m%d-%H%M%S(year,month,day-hour,minute,second). |
| image.directory | String    | An alternate image tree. It works like the base tree, but, if filled out, will be the source folder for all videos. Useful for pre-generated images, for instance. **Leave empty if not used.** |
| multi.chance    | Integer   | A number between 0 and 1, representing the percentage of the time the bot will produce multiple images. Set to 0 to never produce multiple images. Set to 1 to produce multiple images every time. |
| multi.img_num   | Integer   | Goes from 2 to 4 images. Insert 1 for random number. Generates multiple images that get posted as one tweet. Not working with videos. |
| multi.sec_apart | Integer   | Chooses how many seconds apart the multiple generated images should be. |
| video.chance    | Integer   | A number between 0 and 1, representing the percentage of the time the bot will produce a video instead of producing a screenshot. Set to 0 to never produce a video. Set to 1 to produce a video every time. |
| video.length    | Integer   | This is what the length of an outputted video clip will be, in seconds. |
| video.directory | String    | An alternate video tree. It works like the base tree, but, if filled out, will be the source folder for all videos. Useful for guaranteeing that videos have subtitles, for instance.  **Leave empty if not used.** |

##### API Keys
There are also API keys that you must fill out. You will need to sign up for a Twitter developer account in order to gain access to these. For more info, see Twitter's website. https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

These keys & secrets should be placed in the corresponding variables in the 'keys.consumer' and 'keys.access' trees.

| 'keys' tree     | data-type | description |
| --------------- | --------- | ----------- |
| consumer.key    | String    |             |
| consumer.secret | String    |             |
| access.key      | String    |             |
| access.secret   | String    |             |

##### Etc.

Here you can change the output file of the image, video clip and the place where saved images should go. It is not recommended to change anything unless you know what you are doing.

| 'etc' tree      | data-type | description                                                  |
| --------------- | --------- | ------------------------------------------------------------ |
| tmpfile.img     | String    | The normal output file is 'out.jpg', but you could change the extension to 'out.png'. |
| tmpfile.vid     | String    | The normal output file is 'out.mp4', but you could change it to 'out.mkv' or 'out.avi'. There is no guarantee that the bot will work with those file perfectly. 'out.gif' and 'out.webm' are currently not working. |
| tmpfile_alt.img | String    | Path where your images are getting stored. Currently inside the konakona folder. Should end with a '/'. |
| tmpfile_alt.vid | String    | Path where your video clips are getting stored. Currently inside the konakona folder. Should end with a '/'. |

### Future Enhancements
* Burn in subtitles. (Currently soft-subtitles are not supported).
* GUI setup tool.
* Konakona OC ＼(^o^)／

### Licensing
This software is free and open-source software, licensed under the GPLv3. For more information, see the LICENSE file in the repository, or check out https://www.fsf.org/

### Thanks
Mevon, for his help with development and ability organize my pastebins and discord messages of ffmpeg commands. Check out his instance of this bot: [@MonogatariBotto](https://twitter.com/MonogatariBotto).

Ophelia, for recommending that I pick Lucky Star as the source anime for the original bot.
