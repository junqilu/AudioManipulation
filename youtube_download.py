from datetime import datetime
import pytz
import youtube_dl
import os
import requests
import re


def get_title(url):
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:  # 'quiet': True
        # forbids printing any messages to the output
        info_dict = ydl.extract_info(url, download=False)
        youtube_title = info_dict.get('title', None)
        return youtube_title


def str_clean(in_str, replace_char='-',
              delete_char_list=('<', '>', ':', '"', '\\', '/', '|', '?',
                                '*')):
    # delete_char_list contains all the chars that aren't allowed in Windows
    # file names

    print('Before cleaning, video title is {}'.format(in_str))
    for char in delete_char_list:
        in_str = in_str.replace(char, replace_char)
    print('After cleaning, video title is {}'.format(in_str))
    return in_str


def file_direct_remove_exist(file_direct):
    # Since youtube_dl will check if the file already exists, if you changed the url, you need to delete the original raw file you previously downloaded. Otherwise, nothing will be downloaded, and you'll be using the old file
    if os.path.exists(file_direct):
        print(
            'File {} already exists. It will be deleted to allow youtube_dl to overwrite.'.format(
                file_direct))
        os.remove(file_direct)
    return 0


def current_datetime_str():
    time_zone = pytz.timezone(
        'US/Eastern')  # To see all time zones, iterate pytz.all_timezones
    datetime_str = datetime.now(time_zone).strftime('%Y_%m_%d')
    return datetime_str


def download_audio(url, save_parent_direct='audio', audio_format='mp3'):
    audio_title = get_title(url)
    audio_title = str_clean(audio_title)

    audio_title_first_three_words = ' '.join(
        audio_title.split(' ')[:3])
    save_parent_direct = os.path.join(save_parent_direct,
                                      current_datetime_str() + ' ' +
                                      audio_title_first_three_words)

    audio_direct = os.path.join(save_parent_direct, audio_title +
                                '.webm')
    # .webm is the
    # original format. You can't directly download as mp3 but use ffmpeg to
    # convert it into mp3. Otherwise, you can't open the mp3 in Audicity
    file_direct_remove_exist(audio_direct)  # Remove the already existing
    # audio file to force youtube_dl to download

    ydl_args = {
        'format': 'bestaudio/best',  # This forces to download audio only
        'outtmpl': audio_direct,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192'
        }],
        # Lines below are pretty important to ensure the audio file can be
        # opened in Audicity

        # 'ffmpeg-location': r'\ffmpeg',  # This is where you
        # put ffmpeg.exe. This line doesn't really work. You need to move
        # the ffmpeg.exe, ffplay.exe, and ffprobe.exe into the root directory
        'prefer_ffmpeg': True,
        'keepvideo': False  # False to automatically remove the original file
        # after post-processing
    }  # Other options: https://github.com/ytdl-org/youtube-dl/blob
    # /3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312

    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        ydl.download([url])

    return 0


def video_format_list(url):
    # List out all the available format of a video. It'll tell you in the
    # note section which format that the package think is the best
    ydl_args = {
        # 'quiet': True, #If this is True, you won't see the formatl ist
        'listformats': True,
        'skip_download': True  # Skip the actual download of the video file
    }
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        ydl.download([url])
    return 0


def download_video(url, save_parent_direct='video'):
    video_title = get_title(url)
    video_title = str_clean(video_title)

    video_title_first_three_words = ' '.join(
        video_title.split(' ')[:3])
    save_parent_direct = os.path.join(save_parent_direct, current_datetime_str(

    ) + ' ' + video_title_first_three_words)

    video_direct = os.path.join(save_parent_direct, video_title + '.webm')  #
    # .webm is
    # the
    # original format. You can't directly download as mp3 but use ffmpeg to
    # convert it into mp3. Otherwise, you can't open the mp3 in Audicity
    file_direct_remove_exist(video_direct)  # Remove the already existing
    # video file to force youtube_dl to download

    ydl_args = {
        'format': 'best',
        'outtmpl': video_direct
    }  # Other options: https://github.com/ytdl-org/youtube-dl/blob
    # /3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312

    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        ydl.download([url])

    return 0


def make_direct_if_not_exist(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return 0


def download_caption(url, save_parent_direct='audio'):
    title = get_title(url)
    title = str_clean(title)

    title_first_three_words = ' '.join(
        title.split(' ')[:3])
    save_parent_direct = os.path.join(save_parent_direct,
                                      current_datetime_str() + ' ' +
                                      title_first_three_words)

    caption_direct = os.path.join(save_parent_direct, title +
                                  '.txt')

    ydl_args = {
        'writesubtitles': True,
        "writeautomaticsub": True,
        'allsubtitles': True,

        'skip_download': True,  # Skip the actual download of the video file
        'subtitleslangs': ['en'],  # Only want English
        # 'postprocessors': [{
        #     'key': 'FFmpegSubtitlesConvertor',
        #     'format': 'srt',
        # }]
    }

    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        res = ydl.extract_info(url, download=False)
        if res['requested_subtitles']:  # Youtube source has captions
            if res['requested_subtitles']['en']:  # Youtube source has
                # English captions
                if len(res['subtitles']) > 0:
                    print('YouTube source has manual captions.')
                else:
                    print('YouTube source has automatic_captions')
                response = requests.get(
                    res['requested_subtitles']['en']['url'],
                    stream=True)
                if response.ok:
                    make_direct_if_not_exist(save_parent_direct)  # Create the
                    # parent save directory so you can write in the txt file
                    with open(caption_direct, 'w') as file:
                        text_str = response.text
                        text_str = re.sub(r"^([0-9]{1,})(\n\r|\n|\r)",
                                          r"\1 |-| ", text_str, 0,
                                          re.MULTILINE)
                        text_str = re.sub(r"((\n\r|\n|\r){2}.*)(\n\r|\n|\r)",
                                          r"\1 +++ ", text_str, 0,
                                          re.MULTILINE)
                        text_str = re.sub(r"(\+{3} .*)(\n\r|\n|\r)", r"\1 ",
                                          text_str, 0,
                                          re.MULTILINE)
                        text_str = re.sub(r"(\n\r|\n|\r){2}", r"\n", text_str,
                                          0,
                                          re.MULTILINE)
                        file.write(text_str)
            else:
                print("Youtube source doesn't have English captions")
        else:
            print("Youtube source doesn't have captions")

    return 0


def main():
    url = 'https://www.youtube.com/watch?v=60yGE64Xzs4&ab_channel=TheMet'

    # video_format_list(url) #Tells you all the format if you want to have a look
    # download_video(url, save_parent_direct='video')

    download_audio(url, save_parent_direct='audio', audio_format='mp3')
    # download_caption(url, save_parent_direct='audio')
    return 0


if __name__ == '__main__':
    main()
