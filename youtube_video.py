from pytube import YouTube
import os

class YouTubeDownload:

    def __init__(self):
        pass

    def create_cache_folder(self, telegramID: int) -> None:
        path = f'cache/{telegramID}'
        if os.access(path, os.R_OK):
            pass
        else:
            os.mkdir(path)
    
    def video(self, url: int, telegramID: int):
        path = f'cache/{telegramID}/'

        self.create_cache_folder(telegramID)

        yt = YouTube(url)
        where_locate = path + yt.title + '.mp4'
        
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path = path, filename = yt.title + '.mp4')

        return where_locate