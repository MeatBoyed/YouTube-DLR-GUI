import os
import eel
import re
import time
import moviepy.editor as mp
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube, exceptions

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
    fileName = ""

    # Run PyTube validation checks
    try:
        # Create PyTube YouTube object instance
        video = YouTube(url)

        # Give DownloadVideo class the required YouTube class object
        DownloadVideo.videoInstance = video

        # Call DataFetching helper function
        fileName = DataFetch(video)

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
    except ConnectionError:
        errorMessage = "Connection Error. Check you internet connection or try again"
    except Exception as e:
        errorMessage = "An unexpected error occured while downloading the video: " + str(e)
    
    response = {
        "errorMessage": errorMessage,
        "fileName": fileName
    }

    return response


# Collects all data needed about the YouTube video. The video's title 
def DataFetch(youtubeVideoInstance):

    """
        :param youtubeVideoInstance:
            A PyTube YouTube() class instance, which will be used to collect data on
    """

    fileName = ""

    # Collect video's title for the file name
    title = youtubeVideoInstance.title

    # Clear special character that might exist in the video's title
    for sc in title.split("\n"):
        fileName = re.sub(r"[^a-zA-Z0-9]+", ' ', sc)

    response = fileName

    return response

# Download video class. Handles downloading Audio and video files, merging them into one and finally deleting all temp files
@eel.expose
class DownloadVideo():

    # Add all class variables here
    response = {}
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

        
        # Download the temp Video and Audio files
        tempVideo, tempAudio = self.DownloadFiles(resolution=resolution)

        # Merge files together
        result = self.MergeFiles(tempVideo=tempVideo, tempAudio=tempAudio, outputPath=self.outputpath, fileName=fileName)

        # Clean up files
        cleanUpResponse = self.CleanUp(tempVideoFile=tempVideo, tempAudioFile=tempAudio)
        
        self.response = {
            "finalResponse": result,
            "cleanUpResponse": cleanUpResponse 
        }

        return self.response


    def DownloadFiles(self, resolution: str):

        # Check if tempAudio file exists (has been downloaded previously)
        if os.path.exists("./temp/audio.webm"):
            tempAudio = os.path.realpath("./temp/audio.webm")
            print("exist webm")
        elif os.path.exists("./temp/audio.mp4"):
            tempAudio = os.path.realpath("./temp/audio.mp4")
            print("exists mp4")
        else:
            
            try:

                # Download audio
                tempAudio = self.videoInstance.streams.filter(only_audio=True).order_by("abr").desc().first().download(output_path="./temp", filename="audio")
                print("doesn't exist, downloading the tempAudio file")

            except ConnectionError:
                time.sleep(1)
                tempAudio = self.videoInstance.streams.filter(only_audio=True).order_by("abr").desc().first().download(output_path="./temp", filename="audio")
            

        try:
            # Download the tempuraty video and file needed to merge for final video. Will return audio file's path
            tempVideo = self.videoInstance.streams.filter(file_extension="mp4", only_video=True, resolution=resolution).desc().first().download(output_path="./temp", filename="video")
        except ConnectionError:
            time.sleep(1)
            tempVideo = self.videoInstance.streams.filter(file_extension="mp4", only_video=True, resolution=resolution).desc().first().download(output_path="./temp", filename="video")

        # Return tempVideo and tempAudio file paths
        return tempVideo, tempAudio

    
    # Use Moviepy to merge audio and video files
    def MergeFiles(self, tempVideo, tempAudio, outputPath, fileName):

        # Import video file as moviepy object
        try:
            video = mp.VideoFileClip(tempVideo)
        except Exception as e:
            self.response = "An error occured during getting Video file as an Moviepy object. " + str(e)


        # Import audio file as moviepy object
        try:
            audio = mp.AudioFileClip(tempAudio)
        except Exception as e:
            self.response = "An error occured during getting audio file as an Moviepy object. " + str(e)


        # Adding audio track to video file
        try:
            tempOutputVideo = video.set_audio(audio)
        except Exception as e:
            self.response = "An error occured during merging the files. " + str(e)
            print(self.response)

        
        try:
            # Write changes to new output file. Filename is (desired outputPath + desired fileName)
            tempOutputVideo.write_videofile(os.path.join(outputPath, (fileName + ".mp4")))
        except Exception as e:
            self.response = "An error occured during writing to video file. " + str(e)
            print("An error occured during write to video file. ", str(e))

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

        # Delete temp video and audio files
        try:
            os.remove(tempVideoFile)
            os.remove(tempAudioFile)
        except Exception as e:
            return "An error occured while deleteing temp files: " + str(e)


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