from yandex_music import Client
from mdata import MetaData

token = ""

client = Client(token).init()

album = client.albums_with_tracks(5442072)

tracks = []
for i, volume in enumerate(album.volumes):
	if len(album.volumes) > 1:
		tracks.append(f'💿 Диск {i + 1}')
	tracks += volume

text = 'АЛЬБОМ\n\n'
text += f'{album.title}\n'
text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
text += f'{album.year} · {album.genre}\n'

cover = album.cover_uri
if cover:
	text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

text += 'Список треков:'

print(text)

for track in tracks:
	if isinstance(track, str):
		print(track)
	else:
		# track.download(track.title + '.mp3')
		artists = ''
		if track.artists:
			artists = ' - ' + ', '.join(artist.name for artist in track.artists)
		print(track.title + artists)