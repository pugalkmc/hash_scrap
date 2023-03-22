# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # Set up YouTube API client
# API_KEY = "AIzaSyBw-VWCD-28ighChu3aSrryaxL8F1GIcIo"
# youtube = build("youtube", "v3", developerKey=API_KEY)

# # Define the hashtag to search for
# hashtag = "pulsechain"

# # Set the number of results to retrieve per page
# max_results = 1000

# # Call the search.list method to retrieve videos that match the search term
# next_page_token = None
# video_links = []
# while True:
#     search_response = youtube.search().list(
#         q=hashtag,
#         type="video",
#         part="id,snippet",
#         maxResults=max_results,
#         pageToken=next_page_token,
#         fields="items(id(videoId),snippet(title,description))"
#     ).execute()

#     # Loop through each search result and extract the video link
#     for search_result in search_response.get("items", []):
#         video_id = search_result["id"]["videoId"]
#         video_title = search_result["snippet"]["title"]
#         video_description = search_result["snippet"]["description"]

#         # Check if the hashtag is in the video title or description
#         if hashtag.lower() in video_title.lower() or hashtag.lower() in video_description.lower():
#             video_link = f"https://www.youtube.com/watch?v={video_id}"
#             video_links.append(video_link)

#     # Check if there are more pages of results to retrieve
#     next_page_token = search_response.get("nextPageToken")
#     if not next_page_token:
#         break

# # Print the video links
# print("Video links:")
# for video_link in video_links:
#     print(video_link)


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set the API key and YouTube API service name
API_KEY = 'AIzaSyBw-VWCD-28ighChu3aSrryaxL8F1GIcIo'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Set the search query (hash tag) and the maximum number of results to retrieve
QUERY = 'pulsechain'
MAX_RESULTS = 1000

# Create a YouTube API client
try:
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
except HttpError as e:
    print(f'An error occurred while creating the YouTube API client: {e}')
    exit()

# Retrieve the videos that match the search query
video_links = []
next_page_token = None
while len(video_links) < MAX_RESULTS:
    try:
        search_response = youtube.search().list(
            q=QUERY,
            type='video',
            part='id,snippet',
            maxResults=min(MAX_RESULTS - len(video_links), 50),
            pageToken=next_page_token
        ).execute()

        video_ids = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]
        video_links.extend(['https://www.youtube.com/watch?v=' + video_id for video_id in video_ids])
        next_page_token = search_response.get('nextPageToken')

        if next_page_token is None:
            break

    except HttpError as e:
        print(f'An error occurred while retrieving the videos: {e}')
        exit()

# Print the retrieved video links
for video_link in video_links:
    print(video_link)
