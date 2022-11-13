import file_trim
import os
from spleeter.separator import Separator



def music_split(in_file_direct, save_direct):
    if save_direct is None:
        save_direct = os.path.dirname(in_file_direct)

    separator = Separator('spleeter:2stems')
    separator.separate_to_file(in_file_direct, save_direct,
                               filename_format='spletter_export/{instrument}.{'
                                               'codec}')

    return 0

def main():
    audio_direct = "./audio/2022_11_12 Alexander McQueen's extreme/Alexander McQueen's extreme fashion that bridges art and fashion - Art, Explained.mp3"

    output_direct = file_trim.trim_by_duration(audio_direct, None, 50, 0)
    music_split(output_direct, None)

    return 0

if __name__=='__main__':
    main()