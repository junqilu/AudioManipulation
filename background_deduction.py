import file_trim
import os
import subprocess as sp
from spleeter.separator import Separator
import numpy

import demucs


def music_demucs_split(in_file_direct, save_direct):
    if save_direct is None:
        save_direct = os.path.dirname(in_file_direct)

    # As long as your directories contain spaces, you need to use double
    # quotes to embrace it to run in cmd
    save_direct = '"' + save_direct + '/demucs_export' + '"'
    explicit_in_file_direct = '"' + in_file_direct + '"'

    # See all options in https://github.com/facebookresearch/demucs/blob/main/demucs/separate.py
    cmd_str = 'python -m demucs.separate ' + explicit_in_file_direct + ' -o ' + save_direct + ' --two-stems vocals ' + '--jobs 3'
    # Use ' --two-stems vocals'
    # can be faster since I'm only interested in the vocals. Without this
    # argument, you'll have 4 different tracks, 1 for vocal and 3 for
    # others--of course it'll take longer time. I didn't detect any
    # difference of vocal from 2 stems vs. 4 stems separation

    # Use '--jobs 3' to use 3 cores. Your laptop has 4 cores anyway. This
    # will increase the memory usage but also speeds up the process
    sp.call(cmd_str, shell=True)
    return 0


def music_spleeter_split(in_file_direct, save_direct):
    # An potential issue with spleeter is that spleeter was trained to split
    # vocals from music (aka, human is singing), so it might not be the best
    # to split vocal narratives from background music. A better model might
    # be this https://github.com/darius522/dnr-utils but the authors didn't
    # release the pretrained models. But it's still better than nothing

    # From running this, I also found that spleeter separator seems to stuck
    # in some loop after finishing the work. This is another point of not
    # using it
    if save_direct is None:
        save_direct = os.path.dirname(in_file_direct)

    separator = Separator('spleeter:2stems')
    separator.separate_to_file(in_file_direct, save_direct,
                               filename_format='spletter_export/{instrument}.{'
                                               'codec}', synchronous=True)

    return 0


def main():
    audio_direct = "./audio/2022_11_12 -China- Through the/-China- Through " \
                   "the Looking Glass-—Gallery Views.mp3"

    # output_direct = file_trim.trim_by_duration(audio_direct, None, 30, 0) #For generating a testing file

    # music_spleeter_split(output_direct, None) #I like demucs more since it
    # performs a bit better

    for root, dirs, files in os.walk('./audio'):  # Iterate all .mp3 in this
        # folder's sub folders
        for name in files:
            in_file_direct = os.path.join(root, name)  # This is the directory
            # to the input audio file, like './audio/2022_11_12 -China- Through the/start from 0s with duration of 30s.mp3'

            music_demucs_split(in_file_direct, None)  # Split the audio file.
            # The format of output has been set up inside music_demucs_split()
    return 0


if __name__ == '__main__':
    main()
