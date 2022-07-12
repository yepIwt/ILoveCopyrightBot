import music_tag


class MetaData:

    def __init__(self, path_to_song: str):
        self.path = path_to_song
        self.af = music_tag.load_file(path_to_song)

    def change(self, title: str, artist: str, album: str, track_num: int, release_date: str, volume_n: int, total_discs: int, genre: str, lyrics: str):
        self.af['title'] = title
        self.af['artist'] = artist
        self.af['album'] = album
        self.af['tracknumber'] = track_num
        self.af['year'] = release_date
        self.af['discnumber'] = volume_n
        self.af['totaldiscs'] = total_discs
        self.af['genre'] = genre
        self.af['lyrics'] = lyrics
        self.af.save()

    def set_album_cover(self, path_to_cover: str):
        with open(path_to_cover, 'rb') as img_in:
            self.af['artwork'] = img_in.read()
        self.af.save()