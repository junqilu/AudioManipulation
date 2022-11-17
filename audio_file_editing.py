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


def trim_files(init_direct_str, save_direct=None):
    files = select_files(init_direct_str)
    for file in files:  # Since I'm using a for loop here, it doesn't matter
        # whether the user really picked multiple files or just a single file

        # trim_by_end(file, save_direct, end_sec=30, start_sec=10)
        trim_by_duration(file, save_direct, duration_sec=50, start_sec=0)

    return 0


def concatenate_files(init_direct_str, save_direct):
    files = select_files(init_direct_str)

    if len(files) < 1:
        print('No file was selected.')
        return 0
    else:
        if save_direct is None:
            save_direct = os.path.dirname(files[0])
        in_file_format = pathlib.Path(files[0]).suffix
        output_direct = os.path.join(save_direct, 'combine result{}'.format(
            in_file_format))

        # The command that you want to create is something like 'ffmpeg -i "C:/Users/louie/Desktop/test/vocals1.wav" -i "C:/Users/louie/Desktop/test/vocals2.wav" -filter_complex "[0:0][1:0]concat=n=2:v=0:a=1[out]" -map "[out]" "C:/Users/louie/Desktop/test\\combine result.wav"'
        cmd_str = 'ffmpeg'
        for file in files:
            cmd_str += ' -i \"{}\"'.format(file)

        cmd_str += ' -filter_complex \"'
        for idx, file in enumerate(files):
            cmd_str += '[{}:0]'.format(idx)

        cmd_str += 'concat=n={}:v=0:a=1[out]\"'.format(len(files))

        cmd_str += ' -map \"[out]\" \"{}\"'.format(output_direct)
        sp.call(cmd_str, shell=True)
        return 0


def main():
    audio_direct = "./audio/2022_11_12 -China- Through the/-China- Through the Looking Glass-—Gallery Views.mp3"

    trim_by_end(audio_direct, None, 30, 10)
    # trim_by_duration(audio_direct, None, 50, 0)

    pass


if __name__ == '__main__':
    main()
