from REcache import Cache

class Endpoint(object):
    def __init__(self, epc, dc, cLat, totVid):
        self.number_of_caches = epc
        self.dc = dc
        self.cLat = cLat
        self.latency_array = []
        self.list_vidNum = [False] * totVid
        self.time_saved()
        self.list_vidReq = [0] * totVid
        self.score = 0
        self.totVidReq = 0
        self.EpScore = 0

    # def add_video_request_per_cache(self, vidNum, vidReq, cacheId):
    #     videoReq = 0
    #     for EPcache in self.number_of_caches:
    #         if EPcache == cacheId:
    #             self.list_vidNum[vidNum] = True
    #             self.list_vidReq[vidNum] = vidReq

    def score_per_EP_per_videoRequest(self, vidReq, bestTimeSaved):
        if bestTimeSaved != []:
            # print("inside score_per_EP loop")
            initScore = max(bestTimeSaved)
            vReq_score = vidReq*initScore
            # print("best cache:", initScore)
            # print("vReq_score:", vReq_score)
            self.totVidReq += vidReq
            self.score += vReq_score
        #     self.EpScore = self.score / self.totVidReq
        # return self.EpScore

    def get_score_per_EP(self):
        # print("")
        # print("get score:" , self.score)
        # print("totVidReq:", self.totVidReq)
        if self.score != 0 and self.totVidReq != 0:
            self.EpScore = self.score / self.totVidReq
        #need to reset these back to zero for when I calculate the other algorithms otherwise it will just keep accumulating
        self.score = 0
        self.totVidReq = 0
        Cache.reset_cache_variables(self)
        return self.EpScore

    def get_vidReq(self):
        return self.list_vidReq

    def get_dc_latency(self):
        return self.dc

    def get_cache_latency(self):
        return self.cLat

    def get_number_of_caches(self):
        return self.number_of_caches

    def time_saved(self):
        #time saved per cache that's linked to the current endpoint
        for i in range(0, len(self.cLat)):
            self.latency_array += [self.dc - self.cLat[i]]
        return self.latency_array

    def get_time_saved(self):
        return self.latency_array

    # def total_time_saved(self):
    #     #the total time saved by the endpoint using the caches linked to it
    #     for i in range(0, len(self.cLat)):
    #         self.totLat += self.dc - self.cLat[i]
    #     return self.totLat


