class music_queue(list):

    def __init__(self):
        super().__init__()
        
        self.__song_urls = []
        self.index = 0

    def __setitem__(self, title, url):
        self.append(title)
        self.__song_urls.append(url)

    @property
    def title(self):
        if self.index not in range(0, len(self)):
            raise IndexError
        
        return self[self.index]

    @property
    def url(self):
        if self.index not in range(0, len(self)):
            raise IndexError
        
        return self.__song_urls[self.index]