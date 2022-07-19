import os
from TikTokApi import TikTokApi

class TikTokDownload:

    def __init__(self):
        pass

    def create_cache_folder(self, telegramID: int) -> None:
        path = f'cache/{telegramID}'
        if os.access(path, os.R_OK):
            pass
        else:
            os.mkdir(path)
    
    def video(self, video_id: int, telegramID: int):
        path = f'cache/{telegramID}/'

        self.create_cache_folder(telegramID)

        with TikTokApi() as api:
            video = api.video(id = video_id)
            video_data = video.bytes()
            with open(path + "out.mp4", "wb") as out_file:
                out_file.write(video_data)

        return path + "out.mp4"