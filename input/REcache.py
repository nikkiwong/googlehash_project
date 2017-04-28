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

    def __init__(self, size, vTotal):
        self.cacheTotal = size
        self.vidMatrix = [False]*vTotal
        self.videoArray = Set() #this cache uses the Set data structure to store videos
        self.addedVideo = 0

    def add_video_to_cache(self, v, vSize, vReq):
        #only adds videos to the current cache if the video's size that you want to put in the cache is not greater
        #than the remaining size in the cache.
        if self.cacheTotal-vSize > 0:
            #Uses a Set array data structure so there are no duplicate videos in the same cache.
            if self.videoArray.add(v):
                #if the current video is not already in this cache, add it to the cache.
                self.cacheTotal -= vSize
                #reduce the video size from the total cache size
                #so we know how much space we have left for the next video requested.
                self.vidMatrix[v] = True
                #now that the video has been added, in the video matrix,
                #add True to the position of the added video in the array vidMatrix
                return True
        else:
            #if the cache has no space for the video then it will return false
            return False

    def reset_cache_variables(self):
        #this variable is used to reset the counter everytime after the score has been calculated *refer to REendpoint*
        self.addedVideo = 0

    def get_videoMatrix(self):
        return self.vidMatrix

    # HILL CLIMB
    def hill_climb(self, n, eachVSize):
        """this function adds one video to the cache if there is space and it will remove the previously added video"""
        if self.cacheTotal-eachVSize > 0:
            if self.vidMatrix[n] == True:
                return False
            else:
                if self.addedVideo!=0:
                    #this is just for the initial run because addedVideo has not been assigned the value of n yet.
                    self.vidMatrix[self.addedVideo] = False
                #reverting the last added video back to original because in hill climb you only change one!
                self.vidMatrix[n] = True
                self.cacheTotal -= eachVSize
                self.addedVideo = n
                return True

    # RANDOM SEARCH
    def random_search(self, n, eachVSize):
        """this function is to only add videos that have been passed through the function if the video doesn't already exist
        and if there is space in the cache"""
        if self.cacheTotal-eachVSize > 0:
            if self.vidMatrix[n] != True:
                self.vidMatrix[n] = True
                self.cacheTotal -= eachVSize

    # GENETIC ALGORITHM
    def mutate_solution(self, n, eachVSize):
        """this function removes the video from the cache if its already there, if not then it will add it in the cache
        if there is enough space for it"""
        if self.vidMatrix[n] == True:
            self.vidMatrix[n] = False
            self.cacheTotal += eachVSize
            return False
        else:
            if self.cacheTotal - eachVSize > 0:
                self.vidMatrix[n] = True
                self.cacheTotal -= eachVSize
                return True