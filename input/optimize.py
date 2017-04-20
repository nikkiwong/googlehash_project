from Cache import Cache
from Endpoint import Endpoint
from Test import Test

import time

start = time.time()


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def get_request(vr, vsd, x, y):
    for key, value in vr.items():
        if str(x) in key[1] and str(y) in key[0]:
            return value

def read_google(filename):
    data = dict()

    with open(filename, "r") as fin:
        # next() goes to next line down
        system_desc = next(fin)
        number_of_videos, number_of_endpoints, number_of_requests, number_of_caches, cache_size = system_desc.split(" ")
        # type casting because read as strings
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
                ep_to_cache_latency[i].append(ep_to_dc_latency[i])

            cache_list = []
            for j in range(number_of_cache_i):
                cache_id, latency = next(fin).strip().split(" ")
                cache_id = int(cache_id)
                cache_list.append(cache_id)
                latency = int(latency)
                ep_to_cache_latency[i][cache_id] = latency

            ed_cache_list.append(cache_list)

        # removing the dc latency from the cache latency list...
        # don't know how to get rid of it in the above method that the PhD student gave
        # so I am removing it here.
        x = 0
        cache_latency_ep = []
        for i in ep_to_cache_latency:
            # print(i)
            # print(ep_to_dc_latency[x])
            i = remove_values_from_list(i, ep_to_dc_latency[x])
            cache_latency_ep += [i]
            x += 1
            # print(cache_latency_ep)
        ### REQUEST SECTION
        for i in range(number_of_requests):
            video_id, ed_id, requests = next(fin).strip().split(" ")
            video_ed_request[(video_id, ed_id)] = requests

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
    data["cache_latency_ep"] = cache_latency_ep

    return data


data = read_google("input/sample.in")

number_of_requests = data["number_of_requests"]
number_of_caches = data["number_of_caches"]
cache_size = data["cache_size"]

number_of_endpoints = data["number_of_endpoints"]
ep_to_dc_latency = data["ep_to_dc_latency"]
cache_latency_ep = data["cache_latency_ep"]
ep_cache_list = data["ed_cache_list"]
ep_to_cache_latency = data["ep_to_cache_latency"]

number_of_videos = data["number_of_videos"]
video_size_desc = data["video_size_desc"]
video_ep_request = data["video_ed_request"]

video_num_requested_from_ep = [[] for i in range(number_of_endpoints)]
list_endpoint = []
list_cache = []
list_video = []
list_remaining_cache_size = [cache_size] * number_of_caches
list_videoReq_ep_cache = [[] for i in range(number_of_endpoints)]
list_dc = []
list_score = []

for i in range(0, number_of_caches):
    # puts all the cache objects into a list for easy access
    C = Cache(i, cache_size, number_of_caches, number_of_videos)
    list_cache.append(C)

for i in range(0, number_of_endpoints):
    # puts all the endpoint objects into a list for easy access
    EP = Endpoint(i, ep_cache_list, number_of_endpoints, ep_to_dc_latency, cache_latency_ep, ep_to_cache_latency)
    list_endpoint.append(EP)

for i in range(0, number_of_endpoints):
    # puts all the endpoints video details into a list
    list_video.append(list_endpoint[i].get_video_request_and_number_request(video_ep_request, video_size_desc))

for i in range(0, number_of_endpoints):
    for j in list_endpoint[i].get_number_of_caches():
        req = 0
        dcReq = 0
        for x in range(0, len(list_video[i])):
            if list_endpoint[i].get_number_of_caches():
                # if the end point has as cache linked to it
                add = list_cache[j].add_video_to_cache(list_video[i][x][0], list_video[i][x][1])
                if add == True:
                    req += list_video[i][x][2]
                    # getting the total request for current cache
                else:
                    dcReq += list_video[i][x][2]
                    # getting total requests that are not able to be stored in cache

            list_remaining_cache_size[j] = list_cache[j].return_cache_server_size()
            # list_remaining_cache_size default has full memory. As videos being added, the cache size is reduced.
            # ...here we are putting them into a list.
        list_videoReq_ep_cache[i].append(req)
        # list of total video requests that each cache has grouped in endpoints.
    list_dc.append(dcReq)
    list_endpoint[i].time_saved()
    list_endpoint[i].total_time_saved()

print("list_video[i][x][0], list_video[i][x][1]",list_video[0][0][0], list_video[0][0][1])

for i in range(0, len(list_endpoint)):
    # putting only the video numbers that are requested from a particular endpoint into a list
    for j in range(0, len(list_video[i])):
        video_num_requested_from_ep[i].append(list_video[i][j][0])


# print("caches linked to ep0:", ep_cache_list[0])
# print("list of videos:", list_video[0])
# print("endpoint0:", list_endpoint[0])
# print("latency from data center to endpoint[0]:" , ep_to_dc_latency[0])
# print("number of caches:", number_of_caches, ",", len(list_cache))
# print("the videos requested from ep0:", video_num_requested_from_ep[0])
# print("latency from cache to ep0:", ep_to_cache_latency[0])
# for endpoint in range(0, len(ep_cache_list)):
#     for video in range(0, len(list_video[endpoint])-1):
#         for cache in range(0, len(list_cache)):
#             if list_endpoint[endpoint].get_number_of_caches() is None:
#                 print("no cache linked: ",list_video[endpoint][video][2] * ep_to_dc_latency[endpoint])
#             else:
#                 # print(list_cache[cache].get_videoMatrix()[video])
#                 if list_cache[cache].get_videoMatrix()[video] == True:
#                     # pass
#                     print(list_cache[cache].get_videoMatrix()[video])
#                     print(list_cache[cache].get_videoMatrix())

# Calculating the score
# print(ep_to_cache_latency[0])
#
# def score(epCacheList, listVid, listEP, EP_dc_lat, numCache, listCache, vidNumReq, EP_cache_lat ):
#     s = 0
#     for endpoint in range(0, len(epCacheList)):
#         for cache in range(0, len(listCache)):
#             for video in range(0, len(listCache[cache].get_videoMatrix())):
#                 for vid in range(0, len(listVid[endpoint])):
#                     if listEP[endpoint].get_number_of_caches()==[]:
#                         print("no cache linked: ",listVid[endpoint][video][2] * EP_dc_lat[endpoint])
#                         s+=listVid[endpoint][video][2]*EP_dc_lat[endpoint]
#                     else:
#
#                     #swap this with the video.
                    try:
                        if listCache[cache].get_videoMatrix()[video] == True:
                            # if the current cache is linked to current endpoint AND the video is in the list video_num_req from current endpoint
                            if cache in ep_cache_list[endpoint]:
                                if vid + 1 in vidNumReq[endpoint]:
                                    # get_request(video_ep_request, video_size_desc, endpoint, video)
                                    # list_video[endpoint][video][2]*
                                    # print("vid req * time saved in endpoint", endpoint, "from cache", cache, "= video", vid, ":",
                                    #       listVid[endpoint][vid][2], "x", EP_cache_lat[endpoint][cache])
                                    s += listVid[endpoint][vid][2] * EP_cache_lat[endpoint][cache]
                    except:
                        print("dog listVid", len(listVid[endpoint]))
                        # print("dog video index", video)

                        print("dog EP_cache", len(EP_cache_lat[endpoint]))
                        print("dog endpoint index", endpoint)
#
#     return s
#
#
# #HILL CLIMB
#
# a = score(ep_cache_list, list_video, list_endpoint, ep_to_dc_latency, number_of_caches, list_cache, video_num_requested_from_ep, ep_to_cache_latency)
#
# print("original score:", a)
# bestMatrix = list_cache
# n = 0
#
# for i in range(0, number_of_caches):
#     for j in range(0, number_of_videos):
#         if list_cache[i].add_to_matrix(n, video_size_desc[j]):
#             b = score(ep_cache_list, list_video, list_endpoint, ep_to_dc_latency, number_of_caches, list_cache,
#                   video_num_requested_from_ep, ep_to_cache_latency)
#             # print("Hill Climb score:", b)
#             if a<b:
#                 a=b
#                 bestMatrix=list_cache
#             # print("Hill Climb score:", b)
#     n+=1
# print("best Hill Climb score", b)
#
#
# # Test.test_cache_overflow(list_remaining_cache_size, cache_size)
#
#
# end = time.time()
# print(end - start)