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

    response = ""

    # Run PyTube validation checks
    try:
        # Create PyTube YouTube object instance
        YouTube(url)

        # Reset's response for output
        response = ""

    # Exceptions handle all possible Errors that may be caused and saves it in response variable to be out putted to user as an understandble error message
    except exceptions.RegexMatchError or exceptions.ExtractError or exceptions.HTMLParseError:
        response = "Entered URL is invalid. Try again."
    except exceptions.VideoUnavailable:
        response = "Video is Unavailable."
    except exceptions.VideoPrivate:
        resoltion = "Video is Private."
    except exceptions.VideoRegionBlocked:
        response = "Video is Region Blocked."
    except exceptions.RecordingUnavailable:
        response = "Video Recording is Unavailable."
    except exceptions.MembersOnly:
        response = "Video is assessable by Memebers Only."
    except exceptions.LiveStreamError:
        response = "Video is currently being Live Streamed."
    except Exception as e:
        response = "An unexpected error occured while downloading the video: " + str(e)
    
    print(response)
    return response


# Collects all data needed about the YouTube video. The video's title 
def DataFetch(url: str, youtubeVideoInstance):

    """
        :param str url:
            A valid YouTube video url
        :param youtubeVideoInstance:
            A PyTube YouTube() class instance, which will be used to collect data on
    """

    # Collect video's title for the file name
    fileName = youtubeVideoInstance.title

    # Collect all the available resolutions for the video
    



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