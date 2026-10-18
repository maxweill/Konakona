import os
import random
import shutil
import datetime
import subprocess
import time
import requests
import yaml
import tweepy
from requests_oauthlib import OAuth1Session

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # KONAKONA_CONFIG lets a deployment point at a private config (relative paths resolve against this script's directory)
    config_path = os.path.join(script_dir, os.environ.get('KONAKONA_CONFIG', 'config.yaml'))

    with open(config_path, 'r') as stream:
        data = yaml.safe_load(stream)

    settings = {
        'consumer_key': data['twitter']['consumerKey'],
        'consumer_secret': data['twitter']['consumerSecret'],
        'token': data['twitter']['token'],
        'token_secret': data['twitter']['tokenSecret'],

        'directory': data['directory'],
        'video_directory': data['altVidDirectory'],
        'file_ending': data['fileEnding'],

        'save': data['save'],
        'save_images': data['saveDirectory']['images'],
        'save_clips': data['saveDirectory']['clips'],

        'image_count': data['screenshot']['imageCount'],
        'image_seconds_apart': data['screenshot']['secondsApart'],

        'clip_count': data['clip']['clipCount'],
        'clip_seconds_apart': data['clip']['secondsApart'],
        'clip_length': data['clip']['clipLength'],
        'clip_subtitles':data['clip']['forceSubTrack'],
        'chance_clip': data['chance']['clip'],
        'chance_sub': data['chance']['subtitle']
    }

    return settings


def get_random_filepath(directory, file_ending):
    items = os.listdir(directory)
    #gather the list of valid files to work on, subdirectories and files of the correct filetype.
    matching_files = list(filter(lambda x: os.path.isfile(os.path.join(directory, x)) and x.endswith(file_ending), items))
    subdirectories = list(filter(lambda x: os.path.isdir(os.path.join(directory, x)), items))

    #pull one at random from the combined list    
    validchoices = matching_files+subdirectories
    random_selection = random.choice(validchoices)
    
    # if we picked a directory, then we should recursively traverse the tree
    if os.path.isdir(os.path.join(directory, random_selection)):
        random_file=get_random_filepath(os.path.join(directory, random_selection),file_ending)
    #otherwise, lets use the file
    elif os.path.isfile(os.path.join(directory, random_selection)):
        random_file=random_selection
    #finally, if there was no valid selection in our list, then quit out. if we were smarter we could probably make this
    #into a DFS, but i think for now we can say it's user error if there is a dead-end subdirectory.
    else:
        return ""
    
    random_filepath = os.path.join(directory, random_file)
    return random_filepath


def get_file_length(filepath):
    script = [
        'ffprobe',
        '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=%s' % 'p=0'
    ]

    duration = subprocess.check_output(script)

    return float(duration)


def generate_screenshot_local(filepath, duration, image_count, seconds_apart, use_subtitles):
    if image_count >= 5:
        image_count = random.randint(1, 4)

    random_time = random.uniform(0.00, duration - seconds_apart * image_count)

    output_name_list = []
    for i in range(image_count):
        output_name = f"out_{i}.png"
        output_name_list.append(output_name)
    
    if use_subtitles:
        # Fix: Properly escape filepath for ffmpeg subtitles filter on Windows
        # Replace backslashes with forward slashes and escape colons and special chars
        escaped_filepath = filepath.replace('\\', '/').replace(':', '\\:').replace('[', '\\[').replace(']', '\\]')
        vfString = f"subtitles='{escaped_filepath}',scale=min(1920\\,iw):-2:flags=lanczos"
    else:
        vfString = "scale=min(1920\\,iw):-2:flags=lanczos"
    for i in range(image_count):
        script = [
            'ffmpeg', '-y',
            '-ss', str(random_time),
            '-copyts',
            '-i', filepath,
            '-ss', str(random_time),
            '-vframes', '1',
            '-vf', vfString,
            '-q:v', '1',
            '-qmin', '1',
            output_name_list[i]
        ]

        random_time += seconds_apart
        
        print(f"FFmpeg command: {' '.join(script)}")
        result = subprocess.call(script)
        if result != 0:
            raise RuntimeError(f"FFmpeg failed with return code {result} for {output_name_list[i]}")
        print(f"Successfully created: {output_name_list[i]}")
    return output_name_list


def generate_clip_local(filepath, duration, clip_count, seconds_apart, clip_length,use_subtitles):
    if clip_count >= 5:
        clip_count = random.randint(1, 4)

    calc = seconds_apart * clip_count + float(clip_length) * clip_count
    random_time = random.uniform(0.00, duration - calc)

    output_video_list = []
    for i in range(clip_count):
        output_name = f"out_{i}.mp4"
        output_video_list.append(output_name)
    
    if use_subtitles:
        # Fix: Properly escape filepath for ffmpeg subtitles filter on Windows
        # Replace backslashes with forward slashes and escape colons and special chars
        escaped_filepath = filepath.replace('\\', '/').replace(':', '\\:').replace('[', '\\[').replace(']', '\\]')
        vfString = f"subtitles='{escaped_filepath}',scale=min(1920\\,iw):-2:flags=lanczos"
    else:
        vfString = "scale=min(1920\\,iw):-2:flags=lanczos"
    for i in range(clip_count):
        script = [
            'ffmpeg', '-y',
            '-ss', str(random_time),
            '-copyts',
            '-i', filepath,
            '-ss', str(random_time),
            '-t', str(clip_length),
            '-ac', '2',
            '-sn',
            '-map_chapters', '-1',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-vf', vfString,
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-avoid_negative_ts', 'make_zero',
            output_video_list[i]
        ]

        print(f"FFmpeg command: {' '.join(script)}")
        result = subprocess.call(script)
        if result != 0:
            raise RuntimeError(f"FFmpeg failed with return code {result} for {output_video_list[i]}")
        print(f"Successfully created: {output_video_list[i]}")

        random_time += clip_length + seconds_apart

    return output_video_list


def check_generate(chance_clip):
    r = random.random()
    if r <= chance_clip:
        return True
    else:
        return False


_MEDIA_UPLOAD_URL = 'https://api.x.com/2/media/upload'
_MEDIA_UPLOAD_INIT_URL = 'https://api.x.com/2/media/upload/initialize'
_CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB per chunk


def _get_oauth_session():
    return OAuth1Session(
        config['consumer_key'],
        client_secret=config['consumer_secret'],
        resource_owner_key=config['token'],
        resource_owner_secret=config['token_secret']
    )


def _compress_png_to_limit(filepath, max_bytes=5 * 1024 * 1024):
    """Scale down a PNG using ffmpeg in 10% steps until it fits within max_bytes."""
    if os.path.getsize(filepath) <= max_bytes:
        return
    # Get current dimensions via ffprobe
    probe = subprocess.check_output([
        'ffprobe', '-v', 'quiet',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        filepath
    ]).decode().strip().split(',')
    w, h = int(probe[0]), int(probe[1])
    tmp = filepath + '.tmp.png'
    while os.path.getsize(filepath) > max_bytes and w >= 400:
        w = int(w * 0.9)
        subprocess.call([
            'ffmpeg', '-y', '-i', filepath,
            '-vf', f'scale={w}:-2:flags=lanczos',
            tmp
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.replace(tmp, filepath)
    if os.path.exists(tmp):
        os.remove(tmp)


def _upload_image(oauth, filepath):
    """Compress PNG to <5MB then upload via POST /2/media/upload."""
    _compress_png_to_limit(filepath)
    with open(filepath, 'rb') as f:
        resp = oauth.post(
            _MEDIA_UPLOAD_URL,
            files={'media': ('media', f, 'image/png')},
            data={'media_category': 'tweet_image'}
        )
    if not resp.ok:
        print(f"[IMAGE UPLOAD] HTTP {resp.status_code}: {resp.text}")
        resp.raise_for_status()
    return resp.json()['data']['id']


def _upload_video(oauth, filepath):
    """Upload a video via the v2 chunked upload flow."""
    file_size = os.path.getsize(filepath)

    def _check(resp, step):
        if not resp.ok:
            print(f"[{step}] HTTP {resp.status_code}: {resp.text}")
            resp.raise_for_status()

    # INIT
    resp = oauth.post(_MEDIA_UPLOAD_INIT_URL, json={
        'media_type': 'video/mp4',
        'total_bytes': file_size,
        'media_category': 'tweet_video',
    })
    _check(resp, 'INIT')
    media_id = resp.json()['data']['id']

    # APPEND — POST /2/media/upload/{id}/append
    append_url = f'{_MEDIA_UPLOAD_URL}/{media_id}/append'
    with open(filepath, 'rb') as f:
        segment_index = 0
        while True:
            chunk = f.read(_CHUNK_SIZE)
            if not chunk:
                break
            resp = oauth.post(append_url, files={
                'media': ('chunk', chunk, 'application/octet-stream'),
                'segment_index': (None, str(segment_index)),
            })
            _check(resp, f'APPEND segment {segment_index}')
            segment_index += 1

    # FINALIZE — POST /2/media/upload/{id}/finalize
    resp = oauth.post(f'{_MEDIA_UPLOAD_URL}/{media_id}/finalize')
    _check(resp, 'FINALIZE')

    # Poll STATUS until async video processing completes
    processing_info = resp.json().get('data', {}).get('processing_info')
    while processing_info:
        state = processing_info.get('state')
        if state == 'succeeded':
            break
        if state == 'failed':
            raise RuntimeError(f"X media processing failed for {filepath}")
        wait = processing_info.get('check_after_secs', 5)
        time.sleep(wait)
        resp = oauth.get(_MEDIA_UPLOAD_URL, params={'media_id': media_id})
        _check(resp, 'STATUS')
        processing_info = resp.json().get('data', {}).get('processing_info')

    return media_id


def post_update(upload):
    oauth = _get_oauth_session()
    media_ids = []
    for item in upload:
        if item.lower().endswith('.mp4'):
            media_id = _upload_video(oauth, item)
        else:
            media_id = _upload_image(oauth, item)
        media_ids.append(media_id)

    client = tweepy.Client(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token=config['token'],
        access_token_secret=config['token_secret'],
        return_type=requests.Response
    )
    try:
        update = client.create_tweet(text="", media_ids=media_ids)
    except tweepy.errors.HTTPException as e:
        print(e.response.headers)
        print(f"Tweet failed: {e}")
        raise
    else:
        print(update.headers)



def save_files(clip, output):
    output_path = config['save_clips'] if clip else config['save_images']
    # Fix: Remove colons from timestamp - invalid character in Windows filenames
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    
    # Fix: Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    for item in output:
        # Use os.path.join for proper path handling
        destination = os.path.join(output_path, f"{timestamp}_{item}")
        try:
            shutil.move(item, destination)
        except FileNotFoundError as e:
            print(f"Error moving file {item} to {destination}: {e}")
        except OSError as e:
            print(f"OS Error moving file {item} to {destination}: {e}")


if __name__ == '__main__':
    config = load_config()

    generateClip=check_generate(config['chance_clip'])
    directory = config['video_directory'] if generateClip else config['directory']
    if not directory: 
        directory=config['directory']
    filepath = get_random_filepath(directory, config['file_ending'])
    duration = get_file_length(filepath)
    useSubtitles = check_generate(config['chance_sub'])

    if generateClip:
        if config['clip_subtitles']: useSubtitles=True 
        output = generate_clip_local(filepath, duration, config['clip_count'], config['clip_seconds_apart'],
                                     config['clip_length'],useSubtitles)
    else:
        output = generate_screenshot_local(filepath, duration, config['image_count'], config['image_seconds_apart'],useSubtitles)

    post_update(output)

    if config['save']:
        save_files(generateClip, output)  # Fix: Use generateClip instead of calling check_generate again
