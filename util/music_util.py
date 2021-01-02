import youtube_dl

class yt_searcher:

    YDL_OPTS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    def search(self, name):
        with youtube_dl.YoutubeDL(self.YDL_OPTS) as ydl:
            info = ydl.extract_info(f'ytsearch:{name}', download=False)['entries'][0]
            
            return info['title'], info['url']