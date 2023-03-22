from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up YouTube API client
API_KEY = "YOUR_API_KEY"
youtube = build("youtube", "v3", developerKey=API_KEY)

# Define the hashtag to search for
hashtag = "YOUR_HASHTAG"

# Set the number of results to retrieve per page
max_results = 1000

# Call the search.list method to retrieve videos that match the search term
next_page_token = None
video_links = []
while True:
    search_response = youtube.search().list(
        q=hashtag,
        type="video",
        part="id,snippet",
        maxResults=max_results,
        pageToken=next_page_token,
        fields="items(id(videoId),snippet(title,description))"
    ).execute()

    # Loop through each search result and extract the video link
    for search_result in search_response.get("items", []):
        video_id = search_result["id"]["videoId"]
        video_title = search_result["snippet"]["title"]
        video_description = search_result["snippet"]["description"]

        # Check if the hashtag is in the video title or description
        if hashtag.lower() in video_title.lower() or hashtag.lower() in video_description.lower():
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)

    # Check if there are more pages of results to retrieve
    next_page_token = search_response.get("nextPageToken")
    if not next_page_token:
        break

# Print the video links
print("Video links:")
for video_link in video_links:
    print(video_link)
