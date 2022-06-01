import youtube_dl,os, json
from celery import shared_task
from celery.exceptions import Ignore
@shared_task() 
def downloand_video(data):
    try:
        data = json.loads(data)
        url, ss ,to = data['url'], data['ss'],data['to']

        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

        if os.path.exists('video.gif'):
            os.remove('video.gif')

        ydl_opts = {
            'format': "best",
            'videoformat' : "mp4",
            'outtmpl' : "video.mp4",
            'external_downloader': 'ffmpeg',
            'external_downloader_args':  ["-ss", ss, "-to", to],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        raise Ignore()
        


