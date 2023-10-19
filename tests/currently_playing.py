import requests

SPOTIFY_PLAYING_ENDPOINT = "https://api.spotify.com/v1/me/player"
TOKEN = ""

headers = {"Authorization": f"Bearer {TOKEN}"}
r = requests.get(SPOTIFY_PLAYING_ENDPOINT, headers=headers)
data = r.json()

player = {
    'title': data['item']['name'],
    'artist': data['item']['artists'][0]['name'],
    'image': data['item']['album']['images'][0]['url'],
    'is_playing': data['is_playing'],
    'device_name_volume': data['device']['volume_percent'],
    'device_name': data['device']['name'],
    'device_supports_volume': data['device']['supports_volume']
}

print(player)

