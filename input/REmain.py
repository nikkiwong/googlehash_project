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
    # """if video is not in cache it calculates the endpoint score from """
    for key, value in video_ed_request.items():
        list_bestTime = []
        for i in range(0, len(list_cache)):
            if list_cache[i].get_videoMatrix()[int(key[0])]:
                list_bestTime.append(list_endpoint[int(key[1])].get_time_saved()[i])
        # #check out this function score_per_EP to see if it has something to do with the score decreasing all the time.
        # print("list best time:", list_bestTime)
        # if list_bestTime != []:
        #     print("max best time:", max(list_bestTime))
        #     print("Best time score: video req", int(value)," x best time ", max(list_bestTime), "=", int(value)* max(list_bestTime))
        list_endpoint[int(key[1])].score_per_EP(int(value), list_bestTime)


def add_video_to_cache(video_ed_request, ed_cache_list, list_cache, video_size_desc, list_endpoint):
    for key, value in video_ed_request.items():
        for cache in ed_cache_list[int(key[1])]:
            if list_cache[cache].add_video_to_cache(int(key[0]), video_size_desc[int(key[0])], int(value)):
                list_endpoint[int(key[1])].add_video_request_per_cache(int(key[0]), int(value), int(cache))


def hill_climb_algorithm(number_of_caches, number_of_videos, list_cache, video_size_desc, video_ed_request, list_endpoint):
    maximum = 0
    for cache in range(0, number_of_caches):
        for video in range(0, number_of_videos):
            list_cache[cache].hill_climb(video, video_size_desc[video])
            best_time(video_ed_request, list_cache, list_endpoint)
            new_score = score(list_endpoint)
            # print("new score:", new_score)
            if maximum < new_score:
                maximum = new_score
    return maximum


#************************ CREATING CACHE AND ENDPOINT OBJECTS ************************************

list_endpoint = []
list_cache = []

for endpoint in range(0, number_of_endpoints):
    # puts all the endpoint objects into a list for easy access
    endpoint = Endpoint(ed_cache_list[endpoint], ep_to_dc_latency[endpoint], ep_to_cache_latency[endpoint], number_of_videos)
    list_endpoint.append(endpoint)

for cache in range (0, number_of_caches):
    #creating cache objects
    cache = Cache(cache, cache_size, number_of_videos)
    list_cache.append(cache)

#************************ ADD VIDEO TO CACHE ************************************

print("Adding video...")

add_video_to_cache(video_ed_request, ed_cache_list, list_cache, video_size_desc, list_endpoint)

print("Finished adding video.")

#************** CALCULATING FROM WHICH CACHE AN ENDPOINT SHOULD GET VIDEO REQUESTS FROM *************************

best_time(video_ed_request, list_cache, list_endpoint)

#****************************** HILL CLIMB ALGORITHM ********************************

maximum = score(list_endpoint)

print("First score:", maximum)

print("Starting Hill Climb...")

hillClimbScore = hill_climb_algorithm(number_of_caches, number_of_videos, list_cache, video_size_desc, video_ed_request, list_endpoint)
print("Finished Hill Climb.")

if maximum<hillClimbScore:
    maximum = hillClimbScore

print("best Hill Climb score", maximum)

#************** RANDOM GENETIC ALGORITHM *************************




#************** RANDOM SEARCH *************************

from random import randint
randomMax=0
x=0
for cacheNum in range(0, number_of_caches):
    while x<1000:
        n = randint(0, number_of_videos-1)
        list_cache[cacheNum].random_hill_climb(n, video_size_desc[n])
        best_time(video_ed_request, list_cache, list_endpoint)
        randomMax = score(list_endpoint)
        if maximum<randomMax:
            maximum=randomMax
            bestMatrix=list_cache
        x+=1
print("best Random Search score", maximum)

#************** SIMULATED ANNEALING *************************


#************************* PRINTING SCORES ******************************

#test printing
# for cache in list_cache:
#     print("")
#     print(cache)
#     print("cache size:", cache.return_cache_server_size())
#     print("cache video:", cache.get_video_in_cache_list())
# print("cache video:", list_cache[0].get_videoMatrix())
#     print("cache video request:", cache.get_vidReq())
# print(list_cache.get_videoMatrix())
# for endpoint in list_endpoint:
#     print("")
#     print("endpoint time saved:", endpoint.get_time_saved())
# print("endpoint vidReq2:", endpoint.get_vidReq())

# print("SCORE:", score(list_endpoint))

end = time.time()
print("time taken:", end - start)