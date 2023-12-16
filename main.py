def compare_first_words(string1, string2):
    words1 = string1.split()
    words2 = string2.split()
    return words1[0] == words2[0]


def playlist_items(spotify_playlist_id):
    for offset in itertools.count(step = 100):
        resp = spotify_client.playlist_items(spotify_playlist_id, offset = offset, limit = 100)
        for item in resp["items"]:
            yield item
        if resp["next"] is None:
            return

import re
import spotipy
import ytmusicapi
import itertools

print("Welcome to playlist migration!")
# link = input("Please share the link of the Spotify link you want to migrate: ")

# match = re.search(r'playlist/(\w+)\?', link)

# if match:
#     playlist_id = match.group(1)

playlist_id = "2MRa7vEsWCXQe8LI6cXtJp"

from spotipy.oauth2 import SpotifyClientCredentials
client_id = ""//Enter your id here
client_secret = ""//Enter your secret here


auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify_client = spotipy.Spotify(auth_manager=auth_manager)
playlist_name = spotify_client.playlist(playlist_id)['name']
print(f"The current name of the playlist is: {playlist_name}, Do you want to change it [y/n]?")
if (input() == 'y'):
    playlist_name = input("What do you want the new name to be? ")
    

resp = spotify_client.playlist_items(playlist_id, offset = 100)

items = list(playlist_items(playlist_id))


ytmusicapi.setup(filepath="browser.json", headers_raw=""" """)//Enter the details from the network tab here

from ytmusicapi import YTMusic
ytmusic = YTMusic("browser.json")

# yt_playlist_id = ytmusic.create_playlist(playlist_name, f"Copied from spotify: {link}")
yt_playlist_id = ytmusic.create_playlist(playlist_name, f"Copied from spotify:")


video_ids = []

for item in items:
    title = item["track"]["name"]
    album = item["track"]["album"]["name"]
    artists = " ".join([a["name"] for a in item["track"]["artists"] if a["type"] == "artist"])
    query_all = f"{title} {album} {artists}"
    print(query_all)
    print("****************************************")
    search_results = ytmusic.search(query_all)
    for result in search_results:
        if (result['resultType'] == 'song' and compare_first_words(result['title'], title)):
            print(f"Match!")
            video_ids.append(result['videoId'])
            print(video_ids)
            print("*****************")
            break
        else:
            print(f"No Match!")
            
ytmusic.add_playlist_items(yt_playlist_id, video_ids)
