import read_input
from REcache import Cache
from REendpoint import Endpoint
from random import randint
from numba import jit
import time
import copy

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

def add_video_to_cache(video_ed_request, ed_cache_list, list_cache, video_size_desc):
    for key, value in video_ed_request.items():
        for cache in ed_cache_list[int(key[1])]:
            list_cache[cache].add_video_to_cache(int(key[0]), video_size_desc[int(key[0])], int(value))

@jit
def score(list_endpoints):
    """"calculating the fitness of the program"""
    totScore = 0
    for endpoint in list_endpoints:
        totScore += endpoint.get_score_per_EP()
    return totScore

@jit
def best_time(video_ed_request, list_cache, list_endpoint):
    """calculating from the best cache the endpoint should get its video requests from"""
    for key, value in video_ed_request.items():
        list_bestTime = []
        for i in range(0, len(list_cache)):
            if list_cache[i].get_videoMatrix()[int(key[0])]:
                list_bestTime.append(list_endpoint[int(key[1])].get_time_saved()[i])
        list_endpoint[int(key[1])].score_per_EP_per_videoRequest(int(value), list_bestTime)


@jit
def HC_algorithm(number_of_caches, number_of_videos, list_cache, video_size_desc, video_ed_request, list_endpoint):
    maximum = 0
    parent = []
    for cache in range(0, number_of_caches):
        # print("1")
        for video in range(0, number_of_videos):
            # print("2")
            if list_cache[cache].hill_climb(video, video_size_desc[video]):
                best_time(video_ed_request, list_cache, list_endpoint)
                new_score = score(list_endpoint)
                # print("dog:", new_score)
                if maximum < new_score:
                    maximum = new_score
                    parent.append(copy.deepcopy(list_cache))
                    # print("cat", maximum)
    return maximum, parent
@jit
def RS_algorithm(number_of_caches, number_of_videos, list_cache, list_endpoint, video_ed_request, video_size_desc):
    randomMax=0
    x=0
    for cacheNum in range(0, number_of_caches):
        while x<(number_of_videos/2):
            n = randint(0, number_of_videos-1)
            list_cache[cacheNum].random_search(n, video_size_desc[n])
            x+=1
    return randomMax


#very repetitive??? should I always start from the original list or work from the "new" list that keeps getting generated??

@jit
def GA_algorithm(number_of_caches, number_of_videos, list_cache, bestTime, scoreEP, video_size_desc):
    GA_Max=0
    x=0
    for cacheNum in range(0, number_of_caches):
        while x<1000:
            n = randint(0, number_of_videos-1)
            # print("n = ",n)
            if list_cache[cacheNum].genetic_algorithm(n, video_size_desc[n]):
                # print("I'm IN!")
                best_time(video_ed_request, list_cache, list_endpoint)
                new_score = score(list_endpoint)
                if new_score>GA_Max:
                    # print("inside GA algo", GA_Max)
                    GA_Max= new_score
                    # print("inside GA algo", GA_Max)
            x+=1
    return GA_Max

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
originalEP = copy.deepcopy(list_endpoint)
originalCache = copy.deepcopy(list_cache)
randomEP = copy.deepcopy(list_endpoint)
randomCache = copy.deepcopy(list_cache)

print("Adding video...")

add_video_to_cache(video_ed_request, ed_cache_list, originalCache, video_size_desc)
best_time(video_ed_request, originalCache, originalEP)
originalMaximum = score(originalEP)
print("")
print("Finished adding video.")


print("Adding video randomly...")

RS_algorithm(number_of_caches, number_of_videos, randomCache, randomEP, video_ed_request, video_size_desc)
best_time(video_ed_request, randomCache, randomEP)
randomMaximum = score(randomEP)
print("Finished adding video randomly...")


#****************************** HILL CLIMB ALGORITHM ********************************

#seems to finish too quickly for the bigger files...?


# hillClimbScore = maximum-1
print("Original score:", originalMaximum)
print("Random search:", randomMaximum)
print("Starting Hill Climb...")
parents = []

while True:
    hillClimbScore = HC_algorithm(number_of_caches, number_of_videos, randomCache, video_size_desc, video_ed_request, randomEP)
    if originalMaximum<hillClimbScore[0]:
        #storing the best solutions as long as there is improvements
        parents.append(hillClimbScore[1])
        print("new score", hillClimbScore[0])
        randomMaximum = hillClimbScore[0]
    else:
        break
print("Finished Hill Climb...")

print("best Hill Climb score", randomMaximum)

print("Number of good hill climb cache list:", len(parents))

#************** GENETIC ALGORITHM *************************
print("")
print("Starting genetic algorithm...")
count=0
while count<20:
    GA_score = GA_algorithm(number_of_caches, number_of_videos, randomCache, randomEP, video_ed_request, video_size_desc)
    if originalMaximum < GA_score and originalMaximum != GA_score:
        #want to keep the cache matrices that give scores higher than the original cache list.
        parents.append(copy.deepcopy(randomCache))
        #storing the best 20 cache lists.
        count+=1
        print("best genetic algorithm score:", GA_score)

print("Finished genetic algorithm...")

# print("best genetic algorithm score:", GA_score)

#************************ TIME *************************````````````````````
end = time.time()
print("time taken:", end - start)