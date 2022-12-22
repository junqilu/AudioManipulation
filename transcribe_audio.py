import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pprint import pprint


def filename_extension_spliter(file_direct):
    # Split a file_direct to obtain the extension and the file_direct without
    # an extension

    filename, file_extension = os.path.splitext(file_direct)

    # filename will be the file_direct without extension, like "./audio_RA2/Zofia/SovietWar/RA2_csofu39"
    # file_extension is just the extension, like ".mp3"
    return filename, file_extension


def delete_file_by_direct(file_direct):
    # Delete a file by given file_direct
    os.remove(file_direct)
    return 0


def transcribe_audio(audio_file_direct):
    # Transcribe a mp3 audio file by the given audio_file_direct

    # Convert mp3 to wav as the format required by the speech recognition
    sound = AudioSegment.from_mp3(audio_file_direct)
    filename, file_extension = filename_extension_spliter(audio_file_direct)
    new_file_direct = filename + '.wav'
    sound.export(new_file_direct, format='wav')  # This wav file will be
    # deleted later

    recognizer = sr.Recognizer()
    with sr.AudioFile(new_file_direct) as source:
        # recognizer.adjust_for_ambient_noise(source) #Can be used to reduce
        # effects of background noise, but you'll lose 1 sec (by default) of
        # the audio for transcription
        audio = recognizer.record(
            source)  # Read the entire audio file into memory

    try:
        transcript = recognizer.recognize_google(audio, show_all=True)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print(
            'Could not request results from Google Speech Recognition '
            'service; {0}'.format(
                e))

    delete_file_by_direct(new_file_direct)  # Delete the wav file that was
    # generated from the beginning
    return transcript


def main():
    transcript = transcribe_audio(
        './audio_RA2/Zofia/SovietWar/RA2_csofu39.mp3')
    print(transcript)
    return 0


if __name__ == '__main__':
    main()
