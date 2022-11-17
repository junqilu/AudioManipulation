import ffmpeg
import os
import pathlib
from tkinter import filedialog
import subprocess as sp


def select_files(init_direct_str):
    filetypes = (
        ('All audio files', '*.mp3 *.wav'),
        ('All files', '*.*')
    )

    filenames_tuple = filedialog.askopenfilenames(
        title='Select multiple files to process...',
        initialdir=init_direct_str,
        filetypes=filetypes,
    ) #filenames_tuple is a tuple of all the files' directories you selected.
    # If you only
    # select 1 file, filenames will be a tuple of length 1. I'll iterate
    # through this filenames_tuple, so you don't need to worry about whether
    # the user selected only 1 or multiple files

    return filenames_tuple



def trim_by_duration(in_file_direct, save_direct, duration_sec, start_sec=0):
    if save_direct is None:
        save_direct = os.path.dirname(in_file_direct)
    in_file_format = pathlib.Path(in_file_direct).suffix
    output_direct = os.path.join(save_direct, 'start from {}s with duration '
                                              'of {}s{}'.format(start_sec,
                                                                duration_sec,
                                                                in_file_format))

    audio_input = ffmpeg.input(in_file_direct)
    audio_cut = audio_input.audio.filter('atrim',
                                         start=start_sec,
                                         duration=duration_sec)
    audio_output = ffmpeg.output(audio_cut, output_direct)
    ffmpeg.run(audio_output)

    return output_direct


def trim_by_end(in_file_direct, save_direct, end_sec, start_sec=0):
    if save_direct is None:
        save_direct = os.path.dirname(in_file_direct)
    in_file_format = pathlib.Path(in_file_direct).suffix
    output_direct = os.path.join(save_direct, '{}s to {}s{}'.format(
        start_sec, end_sec, in_file_format))

    audio_input = ffmpeg.input(in_file_direct)
    audio_cut = audio_input.audio.filter('atrim', start=start_sec,
                                         end=end_sec)
    audio_output = ffmpeg.output(audio_cut, output_direct)
    ffmpeg.run(audio_output)

    return output_direct


def main():
    audio_direct = "./audio/2022_11_12 -China- Through the/-China- Through the Looking Glass-—Gallery Views.mp3"

    trim_by_end(audio_direct, None, 30, 10)
    # trim_by_duration(audio_direct, None, 50, 0)

    pass


if __name__ == '__main__':
    main()
