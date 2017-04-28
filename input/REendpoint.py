from REcache import Cache

class Endpoint(object):
    def __init__(self, dc, cLat):
        self.dc = dc
        self.cLat = cLat
        self.latency_array = []
        self.time_saved()
        self.score = 0
        self.totVidReq = 0
        self.EpScore = 0


    def score_per_EP_per_videoRequest(self, vidReq, bestTimeSaved):
        """this function calculates which is the best cache for the current endpoint to get its video request from
        and it then calculates the total time saved for that endpoint, by multiplying the video request
        by the time saved by the endpoint (using the best cache linked to it to retrieve the video)"""
        if bestTimeSaved != []:
            initScore = max(bestTimeSaved)
            vReq_score = vidReq*initScore
            self.totVidReq += vidReq
            self.score += vReq_score

    def get_score_per_EP(self):
        """this function calculates the total score per EP by dividing the total time saved by the total number of requests
        from the endpoint"""
        if self.score != 0 and self.totVidReq != 0:
            self.EpScore = self.score / self.totVidReq
        #need to reset these back to zero for after I calculate the score for each of the algorithms otherwise it will just keep accumulating
        self.score = 0
        self.totVidReq = 0
        Cache.reset_cache_variables(self)
        return self.EpScore

    def time_saved(self):
        #time saved per cache that's linked to the current endpoint
        for i in range(0, len(self.cLat)):
            self.latency_array += [self.dc - self.cLat[i]]
        return self.latency_array

    def get_time_saved(self):
        return self.latency_array