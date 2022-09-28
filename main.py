import os
import requests
from bs4 import BeautifulSoup

CLIENT_ID = os.environ.get("Client_ID")
CLIENT_SECRET = os.environ.get("Client_Secret")
SPOTIFY_URI = os.environ.get("Spotify_URI")

#*********************************************Billboard Top 100 songs***************************************************

date = input("Which year do you wanna travel to?Type the date in this format YYYY-MM-DD:")
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url=billboard_url)
data = response.text
music_data = BeautifulSoup(data,"html.parser")
list_data = music_data.find_all(name="h3",class_="a-no-trucate")
song_names = [i.getText().strip() for i in list_data]

#*****************************************************Spotify***********************************************************
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIFY_URI,
        scope="playlist-modify-private")
)
user_id = sp.current_user()["id"]

# import pprint
# data  = {"access_token": "BQCnRsNTVZHyuZGgOZFAVb8d1U_YTBPJzzCLZxGTioYN3sWARyYW6B5fCfzHMow2V_iECaGpbB7Z_Istv-vz2OBow8izA4EtSNEIrqiYWExO4d8ECoxZRZSoIBBKG3M-6OSdLAuQT_yBgJW-G9rJvJplidhIICoOGYDGy_mJ8izw6_6EUhC2E17VGg5YRMULGxLoGcAEKi7uj7mbE1yXkAsMczXUtU87TQ", "token_type": "Bearer", "expires_in": 3600, "refresh_token": "AQDZfMP8aq4wGVri_iveryreSAff9JaMRhVJz84qb8lgXAm8Wqd3N9YnazUyNh3Cw5Q8wyy8D9ItntfNdKpl1u9zeFxt_Xb9fIfO-cUfFkonKhKn9XvryuhArFHnDszPq2E", "scope": "playlist-modify-private", "expires_at": 1663430063}
# json = pprint.pprint(data)
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=True)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)