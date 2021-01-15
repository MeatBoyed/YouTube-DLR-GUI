from logging import error
import eel
from pytube import YouTube
from pytube import exceptions

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


# Download's the requested video. Accepts video's url, the selected video resolution, and the desired download location path
def DownloadVideo(url: str, resolution: str, filename: str, downloadLocation: str):
    # Make query to download the video with the correct parameters
    pass

# Download's the requested video in audio format. Accepts the video's url, the inputed filename, the desired download loaction,
# and inputed metadata about the file
def DownloadAudio(url: str, filename: str, downloadLocation: str, metadata: dict):
    # Make query to download the video with the correct download location and params
    # Edit .mp3 metadata with the inputed metadata fields
    pass


eel.start("index.html")