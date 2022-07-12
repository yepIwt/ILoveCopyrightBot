from yandex_music import Client, supplement
from mdata import MetaData
import os

token = ""


bad_sym = [
	"?",
	"\\",
	"/",
	":",
	"*",
	'"',
	"<",
	">",
	"|"
]


client = Client(token).init()
fetched_track = client.users_likes_tracks()[0].fetch_track()
song_title = fetched_track.title

for s in bad_sym:
    good_title = song_title.replace(s, " ")

fetched_track.download(good_title + ".mp3")
fetched_track.download_cover("cover.jpg")
track_num = fetched_track.albums[0].track_position.index
release_date = fetched_track.albums[0].release_date[:10]
album_title = fetched_track.albums[0].title
artists = f"{', '.join([artist.name for artist in fetched_track.artists])}"

volume_n = fetched_track.albums[0].track_position.volume

album = client.albums_with_tracks(fetched_track.albums[0].id)
totaldiscs = len(album.volumes)
genre = fetched_track.albums[0].genre

lyr_aval = fetched_track.lyrics_available

lyrics = ""
if lyr_aval:
    s = fetched_track.get_supplement()
    lyrics = s.lyrics.full_lyrics

a = MetaData(good_title + '.mp3')
a.change(song_title, artists, album_title, track_num, release_date, volume_n, totaldiscs, genre, lyrics)
a.set_album_cover('cover.jpg')
os.remove("cover.jpg")