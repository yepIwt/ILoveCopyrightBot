from yandex_music import Client
import os
import zipfile
import shutil
from mdata import MetaData

class YandexMusicDownload:

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

	def __init__(self, yandex_music_token: str):
		self.client = Client(yandex_music_token).init()
	
	def create_cache_folder(self, telegramID: int) -> None:
		path = f'cache/{telegramID}'
		if os.access(path, os.R_OK):
			pass
		else:
			os.mkdir(path)
	
	def track(self, albumIDtrackID: int, telegramID: int, delete_after = False):
		path = f'cache/{telegramID}/'
		
		self.create_cache_folder(telegramID)
		
		fetched_track = self.client.tracks(albumIDtrackID)[0] # Получаем объект песни

		song_title = fetched_track.title # Название трека

		# Удаление помех сохранению
		for s in self.bad_sym:
			good_title = song_title.replace(s, " ")

		track_num = fetched_track.albums[0].track_position.index # Место в альбоме
		release_date = fetched_track.albums[0].release_date[:10] # Год выхода
		album_title = fetched_track.albums[0].title # Название альбома
		artists = f"{', '.join([artist.name for artist in fetched_track.artists])}" # Исполнители
		volume_n = fetched_track.albums[0].track_position.volume # Номер диска
		genre = fetched_track.albums[0].genre # Жанр

		album = self.client.albums_with_tracks(fetched_track.albums[0].id) # Получаем объкет альбома
		totaldiscs = len(album.volumes) # Количество дисков        

		lyr_aval = fetched_track.lyrics_available # Проверяем доступен ли текст

		# Получение текста трека
		lyrics = ""
		if lyr_aval:
			s = fetched_track.get_supplement()
			lyrics = s.lyrics.full_lyrics
		
		fetched_track.download(path + good_title + ".mp3") # Скачивание трека
		fetched_track.download_cover(path + "cover.jpg") # Скачивание обложки трека

		a = MetaData(path + good_title + '.mp3') # Создаем объект для работы с метаданными
		
		# Применяем метаданные
		a.change(song_title, artists, album_title, track_num, release_date, volume_n, totaldiscs, genre, lyrics)

		# Наклеиваем обложку
		a.set_album_cover(path +'cover.jpg')
		os.remove(path + "cover.jpg")

		return path + good_title + '.mp3'

	def album(self, albumID: int, telegramID: int):
		path = f'cache/{telegramID}/'
		
		self.create_cache_folder(telegramID)
		shutil.rmtree(path)

		album = self.client.albums_with_tracks(albumID)

		#print(album.volumes)

		tracks = []
		for volume in album.volumes:
			tracks += volume

		cover = album.cover_uri
		album_id = album.id

		for s in self.bad_sym:
			good_title = album.title.replace(s, " ")

		downloaded_tracks = set()
		for track in tracks:
			obj = "{}:{}".format(track.id, album_id)
			downloaded_tracks.add(self.track(obj, telegramID))

		downloaded_tracks = list(downloaded_tracks)
		with zipfile.ZipFile(path + good_title + ".zip", 'w') as zipped_f:
			for track in downloaded_tracks:
				zipped_f.write(
					track,
					os.path.basename(track)
				)

		return path + good_title + ".zip"