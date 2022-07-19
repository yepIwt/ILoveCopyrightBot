#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    ILoveCopyrightBot downloads whatever you want from the url
    yepIwt, 2022
"""

from aiogram import Bot, Dispatcher, executor, types
import yandexmusic
import tiktok_video
import youtube_video

TELEGRAM_TOKEN = ""
YANDEX_MUSIC_TOKEN = ""

class ILoveCopyrightBot:

    def __init__(self, tg_token: str):
        self.bot = Bot(token = tg_token)
        self.yandex = yandexmusic.YandexMusicDownload(YANDEX_MUSIC_TOKEN)
        self.tiktok = tiktok_video.TikTokDownload()
        self.youtube = youtube_video.YouTubeDownload()
    
    async def welcome_page(self, message: types.Message):
        await message.answer("Привет, отправь мне любую ссылку с контентом и я его скачаю")

    async def message_got(self, message: types.Message):
        if 'https://' in message.text:
            if 'music.yandex.ru' in message.text:
                if 'track' in message.text:
                    await message.answer("Яндекс.Музыка.Трек: получена ссылка")

                    # Словесно-адресное порно
                    a1 = message.text.split('/')
                    track_id = a1[a1.index('track') + 1]
                    album_id = a1[a1.index('album') + 1]
                    obj = ['{}:{}'.format(track_id, album_id)]

                    # Отправка трека
                    try:
                        downloaded_path = self.yandex.track(obj, message.from_user.id)
                    except:
                        await message.answer("Хуевая ссылка.")
                    else:
                        f = open(downloaded_path, 'rb')
                        await message.answer_audio(f)
                elif 'album' in message.text:
                    await message.answer("Яндекс.Музыка.Альбом: получена ссылка")

                    # Словесно-адресное порно
                    a1 = message.text.split('/')
                    album_id = a1[a1.index('album') + 1]

                    # Отправка альбома
                    downloaded_path = self.yandex.album(album_id, message.from_user.id)
                    f = open(downloaded_path, 'rb')
                    await message.answer_document(f)

            elif 'tiktok.com' in message.text:
                await message.answer("ТикТок.Видео: получена ссылка")

                # Словесно-адресное порно
                k = message.text.split('/')
                n = k[k.index('video') + 1]
                if '?' in n:
                    n = n[:n.find('?')]
                
                try:
                    downloaded_path = self.tiktok.video(n, message.from_user.id)
                except:
                    await message.answer("Хуевая ссылка.")
                else:
                    f = open(downloaded_path, 'rb')
                    await message.answer_video(f)

            elif 'youtube.com' in message.text or 'youtu.be' in message.text:
                await message.answer("YouTube.Видео: получена ссылка")
                
                try:
                    downloaded_path = self.youtube.video(message.text, message.from_user.id)
                except:
                    await message.answer("Хуевая ссылка.")
                else:
                    f = open(downloaded_path, 'rb')
                    await message.answer_video(f)
        else:
            await message.answer("Нет, это не сработает.")
    
    def start(self):
        dp = Dispatcher(self.bot)
        dp.register_message_handler(self.welcome_page, commands = ['start'])
        dp.register_message_handler(self.message_got, content_types = ['text'])
        executor.start_polling(dp, skip_updates = True)

if __name__ == "__main__":
    cpbot = ILoveCopyrightBot(TELEGRAM_TOKEN)
    cpbot.start()