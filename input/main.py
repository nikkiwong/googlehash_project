from Cache import Cache
from Endpoint import Endpoint

def read_google(filename):
    data = dict()


    with open(filename, "r") as fin:
        #next() goes to next line down
        system_desc = next(fin)
        number_of_videos, number_of_endpoints, number_of_requests, number_of_caches, cache_size= system_desc.split(" ")
        #type casting because read as strings
        number_of_videos = int(number_of_videos)
        number_of_endpoints = int(number_of_endpoints)
        number_of_requests = int(number_of_requests)
        number_of_caches = int(number_of_caches)
        cache_size = int(cache_size)

        video_ed_request = dict()
        video_size_desc = next(fin).strip().split(" ")
        for i in range(len(video_size_desc)):
            video_size_desc[i] = int(video_size_desc[i])
        ed_cache_list = []

        ### CACHE SECTION

        ep_to_cache_latency = []

        ep_to_dc_latency = []
        for i in range(number_of_endpoints):


            ep_to_dc_latency.append([])
            ep_to_cache_latency.append([])

            dc_latency, number_of_cache_i = next(fin).strip().split(" ")
            dc_latency = int(dc_latency)
            number_of_cache_i = int(number_of_cache_i)

            ep_to_dc_latency[i] = dc_latency

            for j in range(number_of_caches):
                ep_to_cache_latency[i].append(ep_to_dc_latency[i]+1)

            cache_list = []
            for j in range(number_of_cache_i):
                cache_id, latency = next(fin).strip().split(" ")
                cache_id = int(cache_id)
                cache_list.append(cache_id)
                latency = int(latency)
                ep_to_cache_latency[i][cache_id] = latency

            ed_cache_list.append(cache_list)

        ### REQUEST SECTION
        for i in range(number_of_requests):
            video_id, ed_id, requests = next(fin).strip().split(" ")
            video_ed_request[(video_id,ed_id)] = requests


    data["number_of_videos"] = number_of_videos
    data["number_of_endpoints"] = number_of_endpoints
    data["number_of_requests"] = number_of_requests
    data["number_of_caches"] = number_of_caches
    data["cache_size"] = cache_size
    data["video_size_desc"] = video_size_desc
    data["ep_to_dc_latency"] = ep_to_dc_latency
    data["ep_to_cache_latency"] = ep_to_cache_latency
    data["ed_cache_list"] = ed_cache_list
    data["video_ed_request"] = video_ed_request

    return data

data = read_google("input/sample.in")

number_of_requests = data["number_of_requests"]
number_of_caches = data["number_of_caches"]
cache_size = data["cache_size"]

number_of_endpoints = data["number_of_endpoints"]
ep_to_dc_latency = data["ep_to_dc_latency"]
ep_to_cache_latency = data["ep_to_cache_latency"]
ep_cache_list = data["ed_cache_list"]


number_of_videos= data["number_of_videos"]
video_size_desc = data["video_size_desc"]
video_ep_request = data["video_ed_request"]
print(ep_cache_list)
EP1 = Endpoint(0, ep_cache_list, number_of_endpoints, ep_to_dc_latency, ep_to_cache_latency)
C1 = Cache(0, cache_size, number_of_caches)
EP1_videos = EP1.get_video_request_and_number_request(video_ep_request, video_size_desc)
print("getting video requests, video size and number of requests for this video from EP1: ", EP1_videos)
# print("getting the size of the video:", )
# print("vr:", video_ep_request, "vsd", video_size_desc)
print("getting the caches that are linked to EP1: ", EP1.get_number_of_caches())
print("the current size of Cache1", C1.return_cache_server_size())

list_endpoint = []
list_cache = []

for i in range(0, number_of_endpoints):
    #puts all the endpoint objects into a list for easy access
    EP = Endpoint(i, ep_cache_list, number_of_endpoints, ep_to_dc_latency, ep_to_cache_latency)
    list_endpoint.append(EP)
    list_video.append(list_endpoint[i].get_video_request_and_number_request(video_ep_request, video_size_desc))

for i in range(0, number_of_caches):
    #puts all the cache objects into a list for easy access
    C = Cache(0, cache_size, number_of_caches)
    list_cache.append(C)

for i in range(0,len(EP1_videos)):
    #adds video to one cache
    C1.add_video_to_cache(EP1_videos[i][0],EP1_videos[i][1])

print("the current size of Cache1", C1.return_cache_server_size())
