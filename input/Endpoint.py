class Endpoint(object):
    def __init__(self, id, epc, total, dc, clat):
        self.id = id
        self.array = []
        self.number_of_caches = epc
        self.total = total
        self.dc = dc
        self.clat = clat

    def get_video_request_and_number_request(self, vr, vsize):
        # returns the video number, the size of the video and the number of requests that the called endpoint has
        for key, value in vr.items():
            # for i in range(0, len())
            if str(self.id) in key[1]:
                self.array += [(int(key[0]), vsize[int(key[0])], int(value))]
        return self.array

    def get_dc_latency(self):
        return self.dc[self.id]

    def get_cache_latency(self):
        return self.clat[self.id]

    def get_number_of_caches(self):
        return self.number_of_caches[self.id]


