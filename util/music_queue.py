class music_queue(list):

    def __init__(self):
        super().__init__()

        self.__song_urls = []
        self.__index = 0

    def __setitem__(self, title, url):
        self.append(title)
        self.__song_urls.append(url)

    @property
    def url(self):
        return self.__song_urls[self.__index]

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, val):
        self.__index = val

    def inc(self, val):
        self.__index += val

    def dec(self, val):
        self.__index -= val

    def range(self):
        return range(0, len(self))