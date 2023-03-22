import googleapiclient.discovery
import pandas as pd

# Set up API key
api_key = "AIzaSyBw-VWCD-28ighChu3aSrryaxL8F1GIcIo"

# Set up YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Search for channels with over 100 subscribers and a specific hashtag
search_response = youtube.search().list(
    q="#pulsechain",
    type="channel",
    order="viewCount",
    fields="items(id(channelId))"
).execute()

# Retrieve social media links from channel's last 100 videos and bio
channels = []
for item in search_response["items"]:
    channel_response = youtube.channels().list(
        part="snippet",
        id=item["id"]["channelId"]
    ).execute()
    for channel in channel_response["items"]:
        description = channel["snippet"]["description"]
        videos_response = youtube.search().list(
            part="snippet",
            channelId=channel["id"],
            maxResults=100,
            order="date",
            type="video",
            fields="items(snippet(publishedAt,channelId,description))"
        ).execute()
        for video in videos_response["items"]:
            video_description = video["snippet"]["description"]
            if "http" in video_description:
                for line in video_description.splitlines():
                    if "http" in line:
                        if "facebook.com" in line or "twitter.com" in line or "instagram.com" in line:
                            channels.append({
                                "Channel Name": channel["snippet"]["title"],
                                "Channel Link": f"https://www.youtube.com/channel/{channel['id']}",
                                "Social Media Link": line.strip(),
                                "Video Link": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                                "Published At": video["snippet"]["publishedAt"]
                            })

# Create spreadsheet
print(channels)
df = pd.DataFrame(channels)
df.to_excel("channels.xlsx", index=False)
print("Spreadsheet created!")
