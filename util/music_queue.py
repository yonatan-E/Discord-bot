class music_queue(list):

    def __init__(self):
        super().__init__()

        self.__song_urls = {}
        self.__current = 0

    def __setitem__(self, title, url):
        super().append(title)
        self.__song_urls[title] = url
    
    def next(self):
        if self.__current >= len(self):
            raise IndexError

        self.__current += 1
        return self.__song_urls[self[self.__current - 1]]
    
    def prev(self):
        if self.__current < 0:
            raise IndexError
    
        self.__current -= 1
        return self.__song_urls[self[self.__current + 1]]

    def reset(self):
        self.__current = 0

    @property
    def current(self):
        return self.__current