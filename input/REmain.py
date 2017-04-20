import read_input
from REcache import Cache
from REendpoint import Endpoint

import time

start = time.time()

data = read_input.read_google("input/me_at_the_zoo.in")

number_of_requests = data["number_of_requests"]
number_of_caches = data["number_of_caches"]
cache_size = data["cache_size"]
number_of_endpoints = data["number_of_endpoints"]
ep_to_dc_latency = data["ep_to_dc_latency"]
ed_cache_list = data["ed_cache_list"]
ep_to_cache_latency = data["ep_to_cache_latency"]
number_of_videos = data["number_of_videos"]
video_size_desc = data["video_size_desc"]
video_ed_request = data["video_ed_request"]

#************************ FUNCTIONS ************************************

def score(list_endpoints):
    """"calculating the fitness of the program"""
    totScore = 0
    for endpoint in list_endpoint:
        totScore += endpoint.get_score_per_EP()
    return totScore


def best_time(video_ed_request, list_cache, list_endpoint):
    """calculating from the best cache the endpoint should get its video requests from"""
    for key, value in video_ed_request.items():
        list_bestTime = []
        for i in range(0, len(list_cache)):
            # print("len cache",len(list_cache))
            # print("matrix before IN BESTTIME cache ", i, ":", list_cache[i].get_videoMatrix())
            # print("vidnum", int(key[0]))
            if list_cache[i].get_videoMatrix()[int(key[0])]:
                #if the video is in the matrix in current cache, then add the time saved of that cache into list_bestTime
                list_bestTime.append(list_endpoint[int(key[1])].get_time_saved()[i])
        # compare all the times saved per cache and pick the best one.
        # print("best time",list_bestTime)
        list_endpoint[int(key[1])].score_per_EP(int(value), list_bestTime)



#************************ CREATING CACHE AND ENDPOINT OBJECTS ************************************

list_endpoint = []
list_cache = []

for endpoint in range(0, number_of_endpoints):
    # puts all the endpoint objects into a list for easy access
    endpoint = Endpoint(ed_cache_list[endpoint], ep_to_dc_latency[endpoint], ep_to_cache_latency[endpoint])
    list_endpoint.append(endpoint)

for cache in range (0, number_of_caches):
    #creating cache objects
    cache = Cache(cache, cache_size, number_of_videos)
    list_cache.append(cache)


print("adding video")

#************************ ADD VIDEO TO CACHE ************************************

for key, value in video_ed_request.items():
    # adding videos that are requested at each endpoint to the caches they are linked to
    for cache in ed_cache_list[int(key[1])]:
        # for video in list_cache[cache].get_videoMatrix():
        # #if the video is NOT IN ANY of the caches
        #     if video == False:
        # # print("video:",key[0])
        list_cache[cache].add_video_to_cache(int(key[0]), video_size_desc[int(key[0])], int(value), int(key[1]))
        list_endpoint[int(key[1])].add_video_request_per_cache(int(key[0]), int(value), int(cache))
        # vid_req[cache] = [value]
    # x = int(key[0]), int(key[1]), int(value)
    # print(x)
        # array.append((x))
print("Finished adding video")

#************** CALCULATING FROM WHICH CACHE AN ENDPOINT SHOULD GET VIDEO REQUESTS FROM *************************

best_time(video_ed_request, list_cache, list_endpoint)

#****************************** HILL CLIMB ALGORITHM ********************************

a = score(list_endpoint)

print("original score:", a)

# n = 0

for cache in list_cache:
    for vidNum in range(0, number_of_videos):
        # print("")
        # print("cache size before:", cache.return_cache_server_size())
        # print("video_size_desc[vidNum]",video_size_desc[vidNum])
        # print("vidNum: ",vidNum)
        # print("")
        # print("matrix before", cache.get_videoMatrix())
        if cache.add_to_matrix(vidNum, video_size_desc[vidNum]):
            # print("HILL CLIMB matrix after:", list_cache[0].get_videoMatrix())
            # print("HILL CLIMB matrix after:", list_cache[1].get_videoMatrix())
            # print("HILL CLIMB matrix after:", list_cache[2].get_videoMatrix())
            # print("HILL CLIMB matrix after:", list_cache[3].get_videoMatrix())

            # print("cache size after:", cache.return_cache_server_size())
            best_time(video_ed_request, list_cache, list_endpoint)
            max = score(list_endpoint)
            print("Hill Climb score:", max)
            if a>max:
                max=a
                # bestMatrix=list_cache
    # n+=1
print("best Hill Climb score", max)


#************** RANDOM GENETIC ALGORITHM *************************




#************** RANDOM SEARCH *************************

# from random import randint
#
# n = 0
# x=0
# for cacheNum in range(0, number_of_caches):
#     while x<50:
#         if list_cache[cacheNum].add_to_matrix(n, video_size_desc[randint(0, number_of_videos)]):
#             best_time(video_ed_request, list_cache, list_endpoint)
#             max = score(list_endpoint)
#             print("Hill Climb score:", max)
#             if a>max:
#                 max=a
#                 bestMatrix=list_cache
#         n+=1
#         x+=1
# print("best Random Search score", max)

#************** SIMULATED ANNEALING *************************


#************************* PRINTING SCORES ******************************

#test printing
# for cache in list_cache:
#     print("")
#     print(cache)
#     print("cache size:", cache.return_cache_server_size())
#     print("cache video:", cache.get_video_in_cache_list())
#     print("cache video:", cache.get_videoMatrix())
#     print("cache video request:", cache.get_vidReq())
# print(list_cache.get_videoMatrix())
# for endpoint in list_endpoint:
#     print("")
#     print("endpoint time saved:", endpoint.get_time_saved())
# print("endpoint vidReq2:", endpoint.get_vidReq())

# print("SCORE:", score(list_endpoint))

end = time.time()
print("time taken:", end - start)