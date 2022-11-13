# AudioManipulation
## Initial set up!
### ffmpeg for audio processing
Installation: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z 
1. Unzip it and put the folder in the root directory--it actually doesn't 
   matter whether you put it in the root directory or not (I did it for 
   documentation)
2. Copy and paste `ffmpeg.exe`, `ffplay.exe`, and `ffprobe.exe` into a 
   directory in PATH, like `C:\Users\louie\AppData\Local\GitHubDesktop\bin` 
   on my computer
3. Now ffmpeg should work normally 

### Audicity for labeling
Installation: https://github.com/audacity/audacity/releases/download/Audacity-3.2.1/audacity-win-3.2.1-64bit.exe 
* This is free 

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

## Speech to text (speech recognition)
This tool can be useful in the batch text to speech step as your job should 
be making small corrections on the transcription process rather than you do 
the transcription 