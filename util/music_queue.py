class music_queue(list):

    def __init__(self):
        super().__init__()

        self.__song_urls = []
        self.index = 0

    def __setitem__(self, title, url):
        self.append(title)
        self.__song_urls.append(url)

    @property
    def url(self):
        return self.__song_urls[self.__index]

    def range(self):
        return range(0, len(self))