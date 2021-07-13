import os
import random
import subprocess

import twitter


# settings
directory = '/PATH/TO/VIDEO/FOLDER/'
clip_length = '5'
video_chance = 0.5

# twitter keys
CONSUMER_KEY_INPUT = 'ENTER_CONSUMER_KEY_INPUT'
CONSUMER_SECRET_INPUT = 'ENTER_CONSUMER_SECRET_INPUT'
ACCESS_TOKEN_KEY_INPUT = 'ENTER_ACCESS_TOKEN_KEY_INPUT'
ACCESS_TOKEN_SECRET_INPUT = 'ENTER_ACCESS_TOKEN_SECRET_INPUT'

# etc.
tmpfile_img = 'out.jpg'
tmpfile_vid = 'out.mp4'


# randomly select an mkv video from input directory
# look at help diagram to understand which use cases are supported
def get_random_video_filepath(directory):
    outdir = ''
    direc = directory
    while os.path.isdir(direc):
        outdir += random.choice(os.listdir(direc))
        if outdir.endswith('mkv'):
            break
        else:
            outdir += '/'
            direc += outdir
    return outdir


# use ffmpeg to generate screenshot at timestamp
def generate_random_screenshot_locally(filepath):
    random_time = random.uniform(0.00, get_length(filepath))
    command_img = [
        'ffmpeg', '-y',
        '-ss', str(random_time),
        '-i', filepath,
        '-vframes', '1',
        '-vf', 'scale=1920:-1',
        '-q:v', '1',
        '-qmin', '1',
        tmpfile_img
    ]
    subprocess.call(command_img)
    return tmpfile_img

# use ffmpeg to generate 5 sec clip at timestamp
def generate_random_clip_locally(filepath):
    random_time = random.uniform(0.00, get_length(filepath) - float(clip_length))
    command_vid = [
        'ffmpeg', '-y',
        '-ss', str(random_time),
        '-i', filepath,
        '-t', str(clip_length),
        '-ac', '2',
        '-sn',
        '-map_chapters', '-1',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-vf', 'scale=1280:-1',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        tmpfile_vid
    ]
    subprocess.call(command_vid)
    return tmpfile_vid

# use ffprobe to get the length of the mkv
def get_length(filepath):
    command_info = [
        'ffprobe',
        '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=%s' % 'p=0'
    ]
    duration = subprocess.check_output(command_info)
    return float(duration)


# uploads the screenshot/clip to twitter
def post_update(tmpfile):
    api = twitter.Api(consumer_key=CONSUMER_KEY_INPUT,
                      consumer_secret=CONSUMER_SECRET_INPUT,
                      access_token_key=ACCESS_TOKEN_KEY_INPUT,
                      access_token_secret=ACCESS_TOKEN_SECRET_INPUT)
    return api.PostUpdate('', tmpfile)


# checks if we should generate a screenshot or clip
def check_video():
    r = random.random()
    if r <= video_chance:
        return True
    else:
        return False
        

if __name__ == '__main__':
	# find our random video by parsing directory
    filepath = directory + get_random_video_filepath(directory)
    
    #determine if we should generate a video or screenshot
    shouldGenerateVideo = check_video()
    
    #generate output file
    if shouldGenerateVideo:
        output=generate_random_clip_locally(filepath)
    else:
        output=generate_random_screenshot_locally(filepath)
    
    #post to twitter.
    post_update(output)
