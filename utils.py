import eel
import youtube_dl

eel.init("web")
eel.start("index.html", size=("10", "550"))


# User has selected file format (mp4 or mp3). This set's off the respective function to collect the data about the video

# Collects all data needed about the YouTube video. The video's title and file size
def DataCollection(url: str):
    # Add a condition to check if mp4 (video) was selected, if true it will fetch and output all the available resolutions for the video
    pass

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

