# AudioManipulation
This repository tries to build up a training dataset from YouTube audio and 
transcripts, and use it to fine-tune an already trained text-to-speech 
model. 

## Initial set up!
### ffmpeg for audio processing
Installation: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z 
1. Unzip it and put the folder in the root directory--it actually doesn't 
   matter whether you put it in the root directory or not (I did it for 
   documentation)
2. Copy and paste `ffmpeg.exe`, `ffplay.exe`, and `ffprobe.exe` into a 
   directory in your computer's PATH, like 
   `C:\Users\louie\AppData\Local\GitHubDesktop\bin` 
   on my computer
3. Now `ffmpeg` should work normally 

### Audicity for labeling
Installation: https://github.com/audacity/audacity/releases/download/Audacity-3.2.1/audacity-win-3.2.1-64bit.exe 
* This is a free alternative for Adobe Audition 
* Download it and install it by the exe 

## Video/audio download 
**youtube_download.py** is used for this section. 

I like YouTube because it usually has closed captions with very high accuracy. 

`youtube_dl` is used for easy download of video. `ffmpeg` works with 
`youtube_dl` to convert the audio into a format that is accessible by 
`audicity`.

`youtube_dl` is also used to download transcripts from YouTube. 

**file_trim.py** is used here for some quick trim of the audio. You can 
also use `audicity` for this purpose, but using the `ffmpeg` commands is 
faster.

## Transcript/caption/subtitle download
**youtube_download.py** is used for this section. 

If you set inside the arguments that you want `'writesubtitles': True, 
'writeautomaticsub': True, 'allsubtitles': True`, in the returned ydl.
extract_info(url, download=False), you'll have `'requested_subtitles', 
'automatic_captions', and 'subtitles'`. 
* `'subtitles'` will be the one for manual captions and thus, they're usually
  fewer than `'automatic_captions'`.
  * Also, `'subtitles'` have better quality (more accurate texts and better 
    timestamp alignment) than `'automatic_captions'`, 
    so you 
    should download them first. 
* `'requested_subtitles'` is like a union of `'subtitles'` and 
  `'automatic_captions'`.

## Transcript/caption/subtitle processing
**transcript_processing.py** is used for this section. 

Downloaded transcripts can have different formats, so you need to double-check on the output file before you import it into audicity for labeling. 

The resulting output label txt is just a base and you can manually edit it 
before use it for labeling in audicity. 
* You can fuse some terms together to ensure a label is always a full 
  sentence. 
* For separating several sentences, you need to do it inside audicity. 

## Background noise (music) deduction 
**background_deduction.py** is used for this section. 

`Spleeter` (much quicker) vs `Demucs` (better performance): https://www.audiostrip.co.uk/#isolate 
* Both of them are machine learning model based 
* I'd recommend you trim a test sample from your audio 
  and run the test on this website, and then use the `background_deduction.
  py` to do the work
* Comparisons: **for best results, use Demucs** 
  * For me, I do feel Demucs performs a bit better than Spleeter for the 
  track I tested on.
    * Spleeter's vocal has some underwater effects compared to Demucs's
    * When work on a track has only vocals, Spleeter's non-vocal will pick 
      up on some "s" of higher pitches, while Demucs's non-vocal is pretty 
      much all silent
  * Spleeter has a wrapper while Demucs doesn't--both can be run by 
    subprocess 
    * Spleeter has some issues that after finishing the work, its separate 
      cannot stop properly <- this is another reason to use Demucs 
* Both Spleeter and Demucs are trained on vocal singing's, so the most 
challenging parts of separation are when the background music contains 
someone singing (both of them are bad on processing situations like that).  
  * A better model might be this https://github.com/darius522/dnr-utils that 
    was trained on narratives with music, which is more suitable for your 
    purpose, but the authors didn't release the pretrained models. 

## Audicity labeling
You need background-deducted vocal and the processed transcript to finish 
this step. 

Steps: reference: https://github.com/hollygrimm/voice-dataset-creation#-create-transcriptions-for-existing-voice-recordings
1. Load the vocal .wav in audicity. 
2. File -> Import -> Labels, and click the processed transcript .txt
3. You should see that labels are generated based on the time points you 
   provided and the text on labels are the transcript you provided. 
4. You play the audio and adjust the labels for the time and text on the 
   label. 
   * During labeling, try to avoid leading and trailing spaces in the label 
     texts. Also ensure the punctuations are correct.  
5. File -> Save project -> Save project, just in case if you want to make 
   changes later. 
6. File -> Export -> Export multiple. Set up as below and click Export 
   * Folder: ...\wavs_export and click Create
   * Format: WAV
   * Options: Signed 16-bit PCM
   * Split files based on: Labels
   * Name files: Using Label/Track Name
7. File -> Export -> Export labels, and save the file as labels.txt

## Speech to text (speech recognition)
This is only necessary if you don't have a transcript for the audio you're 
working on. 
* If the transcript for YouTube is manual (thus, very high accuracy and 
  time alignment), then you don't need to do this section.

This tool can be useful in the batch text to speech step as your job should 
be making small corrections on the transcription process rather than you do 
the transcription 