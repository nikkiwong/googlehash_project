class Set:
    def __init__(self):
        """ self is tied to the instance of Set."""
        self.__size = 0
        self.__array = []

    def get_size(self):
        return self.__size

    def add(self, e):
        for i in range(self.__size):
            if self.__array[i] == e:
                return False
        # need to increase size because more important than length of array
        self.__size += 1
        self.__array += [e]
        return True

    def print_setArray(self):
        for i in range(self.__size):
            print(self.__array[i], end=" ")  # if you have end="" it gives you a space instead of a new line..

    def get_setArray(self):
        self.get_set = []
        for i in self.__array:
            self.get_set += [i]
        return self.get_set

    def remove(self, e):
        found = False
        i = 0
        while i < self.__size and found == False:
            if self.__array[i] == e:
                found = True
            i += 1
        if found:
            #             self.__array.pop(i-1)
            #             self.__size -=1
            while i < self.__size:
                self.__array[i - 1] = self.__array[i]
                i += 1
            # #need to decrease the size of the array otherwise it will just print the last number twice because you're only shift and substituting, so there's no blank to sub the last number.
            self.__size -= 1
            self.__array = self.__array[1:]  # gets rid of index 0
            #

    def is_empty(self):
        if self.__size == 0:
            return True
        else:
            return False

class Cache(object):

    def __init__(self, id, size, vTotal):
        self.id = id
        self.size = size
        self.cacheTotal = self.size
        self.vidMatrix = [False]*vTotal
        self.videoArray = Set()
        self.videoReq = 0
        self.addedVideo = 0

    def add_video_to_cache(self, v, vSize, vReq):
        #only adds videos if the video's size that you want to put in the cache is not greater
        #than the remaining size in the cache. Uses the set data structure so there are no
        #duplicat videos in the cache.
        if self.cacheTotal-vSize > 0:
            # print("")
            # print("video:", int(v), ", video size:", vSize )
            # print("before cache size", self.cacheTotal)
            if self.videoArray.add(v):
                self.cacheTotal -= vSize
                self.vidMatrix[v] = True
            self.videoReq += vReq
            # print("videos that have been added to the cache", self.id,":", self.videoArray.get_setArray())
            # print("remaining cache size",self.cacheTotal)
            return True
        else:
            # print("video too big for cache", self.id, "!!")
            # print("remaining cache size", self.cacheTotal)
            return False

    def return_cache_server_size(self):
        # returns the remaining size of the cache
        # print(self.matrix)
        return self.cacheTotal

    def get_video_in_cache_list(self):
        return self.videoArray.get_setArray()

    def get_vidReq(self):
        return self.videoReq

    def get_videoMatrix(self):
        return self.vidMatrix

    def hill_climb(self, n, eachVSize):

        #HILL CLIMB
        #only adds videos if the video's size that you want to put in the cache is not greater than the remaining size in the cache
        if self.cacheTotal-eachVSize > 0:
            if self.vidMatrix[n] == True:
                return False
            else:
                self.vidMatrix[self.addedVideo] = False
                #reverting the last added video back to original because in hill climb you only change one!
                self.vidMatrix[n] = True
                self.cacheTotal -= eachVSize
                self.addedVideo = n

                return True

    def random_hill_climb(self, n, eachVSize):

        #HILL CLIMB
        #only adds videos if the video's size that you want to put in the cache is not greater than the remaining size in the cache
        if self.cacheTotal-eachVSize > 0:
            if self.vidMatrix[n] == True:
                self.vidMatrix[n] = False
                self.cacheTotal += eachVSize
            else:
                self.vidMatrix[self.addedVideo] = False
                #reverting the last added video back to original because in hill climb you only change one!
                self.vidMatrix[n] = True
                self.cacheTotal -= eachVSize
                # self.addedVideo = n




    def __repr__(self):
        return "cache" + str(self.id)