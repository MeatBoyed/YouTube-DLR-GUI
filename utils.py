import os
import eel
from pytube import YouTube
from pytube import exceptions
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp

eel.init("web")

# User has selected file format (mp4 or mp3). This set's off the respective function to collect the data about the video

# Validate input video's url, if successful will run DataFetching function
@eel.expose
def ValidateURL(url: str):

    """
    Runs validation checks to ensure the inputed url is valid for downloading with PyTube.
    Returns Boolean value, with respective error message to display to user.

        :param url:
            Inputed YouTube video url
    """

    errorMessage = ""
    data = {}

    # Run PyTube validation checks
    try:
        # Create PyTube YouTube object instance
        video = YouTube(url)
        DownloadVideo.videoInstance = video

        # Call DataFetching helper function
        data = DataFetch(video)

        # Reset's response for output
        errorMessage = ""

    # Exceptions handle all possible Errors that may be caused and saves it in errorMessage variable to be out putted to user as an understandble error message
    except exceptions.RegexMatchError or exceptions.ExtractError or exceptions.HTMLParseError:
        errorMessage = "Entered URL is invalid. Try again."
    except exceptions.VideoUnavailable:
        errorMessage = "Video is Unavailable."
    except exceptions.VideoPrivate:
        errorMessage = "Video is Private."
    except exceptions.VideoRegionBlocked:
        errorMessage = "Video is Region Blocked."
    except exceptions.RecordingUnavailable:
        errorMessage = "Video Recording is Unavailable."
    except exceptions.MembersOnly:
        errorMessage = "Video is assessable by Memebers Only."
    except exceptions.LiveStreamError:
        errorMessage = "Video is currently being Live Streamed."
    except Exception as e:
        errorMessage = "An unexpected error occured while downloading the video: " + str(e)
    
    response = {
        "errorMessage": errorMessage,
        "videoData": data
    }

    return response


# Collects all data needed about the YouTube video. The video's title 
def DataFetch(youtubeVideoInstance):

    """
        :param str url:
            A valid YouTube video url
        :param youtubeVideoInstance:
            A PyTube YouTube() class instance, which will be used to collect data on
    """

    availabelResolutions = []

    # Get list of availabel streams, filterig out DASH streams
    streams = youtubeVideoInstance.streams.filter(progressive=True)

    # Collect video's title for the file name
    fileName = youtubeVideoInstance.title

    # Iterating through all streams to collect availabel resolutions
    for stream in streams:
        availabelResolutions.append(stream.resolution)

    response = {
        "fileName": fileName,
        "resolutions": availabelResolutions,
    }

    return response

# Download video class. Handles downloading Audio and video files, merging them into one and finally deleting all temp files
@eel.expose
class DownloadVideo():

    # Add all class variables here
    response = ""
    outputpath = ""
    videoInstance = None

    # Add class init function to run other things
    def __init__(self, resolution: str, fileName: str):

        """
            :param resolution:
                Desired video resolution of video to download
            :param filename:
                Desired inputted filename of outputed video
        """

        print("Download has begun")

        # Download the tempuraty video and audio files needed to merge for final video. Will return audio file's path
        tempVideo = self.videoInstance.streams.filter(file_extension="mp4", only_video=True, resolution=resolution).desc().first().download(output_path="./temp", filename="video")
        tempAudio = self.videoInstance.streams.filter(only_audio=True).order_by("abr").desc().first().download(output_path="./temp", filename="audio")

        # Merge files together
        result = self.MergeFiles(tempVideo=tempVideo, tempAudio=tempAudio, outputPath=self.outputpath, fileName=fileName)

        # Clean up files
        self.CleanUp(tempVideoFile=tempVideo, tempAudioFile=tempAudio)
        
        self.response = result
    
    # Use Moviepy to merge audio and video files
    def MergeFiles(self, tempVideo, tempAudio, outputPath, fileName):

        # Import video and audio files as moviepy objects
        video = mp.VideoFileClip(tempVideo)
        audio = mp.AudioFileClip(tempAudio)

        # Adding audio track to video file
        tempOutputVideo = video.set_audio(audio)

        # Write changes to new output file. Filename is (desired outputPath + desired fileName)
        tempOutputVideo.write_videofile(os.path.join(outputPath, (fileName + ".mp4")))

        print("Merge completeed")

        self.response = "Download Successful"

        
    # Use OS to delete all temp files and folders
    def CleanUp(self, tempVideoFile, tempAudioFile):

        """
            :param tempVideoFile:
                Path to temp video file
            :param tempAudioFile:
                Path to temp audio file
        """

        os.remove(tempVideoFile)
        os.remove(tempAudioFile)



# Download's the requested video in audio format. Accepts the video's url, the inputed filename, the desired download loaction,
# and inputed metadata about the file
def DownloadAudio(url: str, filename: str, downloadLocation: str, metadata: dict):
    # Make query to download the video with the correct download location and params
    # Edit .mp3 metadata with the inputed metadata fields
    pass

@eel.expose
def selectFolder():
    print("Here")
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()
    print(directory_path)

    DownloadVideo.outputpath = os.path.join(directory_path)

    return directory_path

eel.start("index.html")