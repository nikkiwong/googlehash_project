class Cache(object):
    def __init__(self, id, size, total):
        self.id = id
        self.total = total
        self.matrix = [size] * self.total
        self.cacheSize = self.matrix[self.id]
        self.videoArray = []

    def return_cache_server_size(self):
        # returns the remaining size of the cache
        return self.cacheSize

    def add_video_to_cache(self, v, vSize):
        if self.cacheSize-vSize >= 0:
            self.videoArray += [(v)]
            self.cacheSize-=vSize



