import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import json

class YoutubeAPI:

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    DEV_KEY = None

    def __init__(self):
        with open("./keys.json") as f:
            keys = json.load(f)
        YoutubeAPI.DEV_KEY = keys["DEV_KEY"]
        self.youtube_connector = googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=YoutubeAPI.DEV_KEY)

    def get_comments(self, video_id: str, max_results: int = 100):
        """
        Fetch comments from a YouTube video.

        :param video_id: The ID of the YouTube video.
        :param max_results: Maximum number of comments to fetch.
        :return: A list of comments.
        """
        request = self.youtube_connector.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results,
        )
        response = request.execute()
        # Print the video title for debugging
        print(f"Fetching comments for video ID: {video_id}")
        # Get the video title
        video_request = self.youtube_connector.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()
        video_title = None
        if video_response.get("items"):
            video_title = video_response["items"][0]["snippet"].get("title")
        print(f"Video title: {video_title}")
        comments = []
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            comments.append({"author": author, "text": text})
        return comments, video_title

# Test
if __name__ == "__main__":
    youtube_api = YoutubeAPI()
    video_id = "laay5hnpdUE"  # Replace with a valid YouTube video ID
    comments = youtube_api.get_comments(video_id, max_results=1)
