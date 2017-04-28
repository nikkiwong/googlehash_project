import read_input
from REcache import Cache
from REendpoint import Endpoint
from random import randint, sample
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

# @jit is a function from the library numba. I'm not sure if it makes much difference here, but it basically helps to
#speed up codes.

# ************************ FUNCTIONS ************************************

@jit
def add_video_to_cache(video_ed_request, ed_cache_list, list_cache, video_size_desc):
    """this function adds videos to the caches linked to the corresponding endpoints"""
    for key, value in video_ed_request.items():
        # using the dictionary provided, I iterate through the dictionary.
        for cache in ed_cache_list[int(key[1])]:
            # for each cache that is linked to the current endpoint
            list_cache[cache].add_video_to_cache(int(key[0]), video_size_desc[int(key[0])])
            # add the current video into to the cache that is linked to the current endpoint.


@jit
def score(list_endpoints):
    """"calculating the fitness of the program"""
    totScore = 0
    for endpoint in list_endpoints:
        #iterating through all the endpoints and summing up all their scores into totScore
        totScore += endpoint.get_score_per_EP()
    return totScore


@jit
def best_time(video_ed_request, list_cache, list_endpoint):
    """calculating from the best cache the endpoint should get its video requests from"""
    for key, value in video_ed_request.items():
    #iterate through the dictionary that has the videos linked with the endpoints.
        list_bestTime = []
        for i in range(0, len(list_cache)):
            #now we will iterate through all the caches one by one.
            if list_cache[i].get_videoMatrix()[int(key[0])]:
                #if the current video being requested in current endpoint is in the current cache then
                list_bestTime.append(list_endpoint[int(key[1])].get_time_saved()[i])
                #add the time saved (dc-latency) from the current cache to the current endpoint into list_bestTime
        list_endpoint[int(key[1])].score_per_EP_per_videoRequest(int(value), list_bestTime)
        #the cache that saves the endpoint the most time is selected from the list. Then the score for that video at that endpoint is calculated *refer to report for detail*


@jit
def HC_algorithm(number_of_caches, number_of_videos, list_cache, video_size_desc, video_ed_request, list_endpoint):
    """this function calculates the Hill Climb. ONLY ONE video is added at a time"""
    maximum = 0
    parent = []
    randomSelection = []
    for cache in range(0, number_of_caches):
    #iterate through the caches one at a time
        for video in range(0, number_of_videos):
        #iterate through all the videos one at a time
            if list_cache[cache].hill_climb(video, video_size_desc[video]):
            #if the video is successfully added then the above function returns true
                best_time(video_ed_request, list_cache, list_endpoint)
                new_score = score(list_endpoint)
                #calculates the score for the new matrix created by adding current video into the current cache
                if maximum < new_score:
                    #if the score is greater than the maximum then the new score will replace the current maximum score
                    maximum = new_score
                    parent.append(copy.deepcopy(list_cache))
                    #add this cache list to the parent list

    parent_index = sample(range(len(parent) // 2, len(parent)), 4)
    #now we want to randomly select 4 of the cache lists we stored in the parent list earlier.
    # We only choose from the last half of the list because those would be the best 50% of the scores as the best ones were always appended to the end of the parent list.
    for i in parent_index:
        # storing only the cache list that is at the index location in the parent list, randomly chosen from above.
        randomSelection.append(parent[i])
    return maximum, randomSelection


@jit
def RS_algorithm(number_of_caches, number_of_videos, list_cache, video_size_desc):
    """this function RANDOMLY adds videos one at a time into half of the caches in the cache list!"""
    randomMax = 0
    x = 0
    cacheIndex = sample(range(0, number_of_caches), number_of_caches // 2)
    for cacheNum in cacheIndex:
        #iterate through the first half of the cache one at a time!
        while x < (number_of_videos) * 100:
            #we will add x amount of random videos to the cache
            n = randint(0, number_of_videos - 1)
            #we get n random numbers that are the available video numbers from the file.
            list_cache[cacheNum].random_search(n, video_size_desc[n])
            #add random videos into the current cache
            x += 1
    return randomMax


@jit
def mutation_algorithm(number_of_caches, number_of_videos, list_cache, list_endpoint, video_ed_request, video_size_desc):
    """this function generates mutations in each cache"""
    mutate_Max = 0
    parents = []

    cacheIndex = sample(range(0, number_of_caches), number_of_caches//3)
    #using this so that there are no duplicate random selection of caches
    #selecing random caches to put videos into.
    for cacheNum in cacheIndex:
    #iterates through the caches randomly adding a random video for that random cache selected
        n = randint(0, number_of_videos - 1)
        # chose random video number from 0 to the number of videos that are give from the file.
        #adding cache list to parent list regardless of successful mutation,best score or worst score (simulated annealing)
        parents.append(copy.deepcopy(list_cache))

        if list_cache[cacheNum].mutate_solution(n, video_size_desc[n]):
            #if the random video generated was successfully added to the current cache returns True
            best_time(video_ed_request, list_cache, list_endpoint)
            new_score = score(list_endpoint)
            #calcute the total score after mutation of the current cache

            parents.append(copy.deepcopy(list_cache))
            if new_score > mutate_Max:
                #if the new score generated by the mutate cache is greater than the previous max then make new score the new max.
                mutate_Max = new_score

    return mutate_Max, parents

def evolution_time(parents):
    """this function evolves the solutions, from parent to child, create a new generation of cache lists"""
    children = []
    while len(children) <= len(parents):
        # making the same number of children as there are parents
        A = randint(0, len(parents) - 1)
        B = randint(0, len(parents) - 1)
        if A != B:
        #making sure that no two parents are the same
            parent_A = parents[A]
            parent_B = parents[B]
            half = len(parent_A) // 2
            child = parent_A[:half] + parent_B[half:]
            #the child is created using half of parent A and half of parent B
            children.append(child)
            # so we have the same amount of children compared to parents

    return children


@jit
def best_children(children, video_ed_request, list_endpoint):
    """"this function calculates the scores for the children generated from the genetic algorithm and
    stores only the cache lists that gave a score greater than the best score generated by the parents from the genetic algorithm"""
    best_new_score = []
    new_children = []
    for child in children:
        #iterating through the children and calculating their scores
        best_time(video_ed_request, child, list_endpoint)
        child_score = score(list_endpoint)
        if child_score > max(mutation):
            #if the child score is greater than the best overall score.
            best_new_score.append(child_score)
            new_children.append(child)
            #score the score and the cache list into their corresponding lists
    if best_new_score == []:
        #if the children didn't generated any better scores, then return false
        return False
    else:
        return True, new_children, best_new_score


# ************************ CREATING CACHE AND ENDPOINT OBJECTS ************************************

list_endpoint = []
list_cache = []

for endpoint in range(0, number_of_endpoints):
    # puts all the endpoint objects into a list for easy access
    endpoint = Endpoint(ep_to_dc_latency[endpoint], ep_to_cache_latency[endpoint])
    list_endpoint.append(endpoint)

for cache in range(0, number_of_caches):
    # creating cache objects and putting them into a list
    cache = Cache(cache_size, number_of_videos)
    list_cache.append(cache)

# ************************ ADD VIDEO TO CACHE ************************************

#creating deep copies of the lists.
originalEP = copy.deepcopy(list_endpoint)
originalCache = copy.deepcopy(list_cache)
randomEP = copy.deepcopy(list_endpoint)
randomCache = copy.deepcopy(list_cache)


#adding videos to the cache in an orderly fashion in terms of iterating through the dictionary and calculating the score
add_video_to_cache(video_ed_request, ed_cache_list, originalCache, video_size_desc)
best_time(video_ed_request, originalCache, originalEP)
originalMaximum = score(originalEP)

#adding videos to all the caches at completely random and calculating the score
RS_algorithm(number_of_caches, number_of_videos, randomCache, video_size_desc)
best_time(video_ed_request, randomCache, randomEP)
randomMaximum = score(randomEP)

best_score = []
best_score.append(originalMaximum)
best_score.append(randomMaximum)

# ****************************** HILL CLIMB ALGORITHM ********************************


parents = []

#computing the hill climb algorithm on the cache lists that had videos randomly put in
hillClimbScore = HC_algorithm(number_of_caches, number_of_videos, randomCache, video_size_desc, video_ed_request,
                              randomEP)
if originalMaximum < hillClimbScore[0]:
    randomMaximum = hillClimbScore[0]

# storing the local best solutions
parents += hillClimbScore[1]


# ************** GENETIC ALGORITHM *************************

# --- Part 1: Mutation ---

count = 0
entering = 1
mutation = []

mutation_score = mutation_algorithm(number_of_caches, number_of_videos, randomCache, randomEP, video_ed_request,
                                    video_size_desc)
mutation.append(mutation_score[0])
# storing the mutated matrices into cache lists.

parents += mutation_score[1]


# --- Part 2: Evolution ---

#here I am randomly selecting a third of caches from the list of cache lists from parents
parents_index = sample(range(0, len(parents)), len(parents)//3)


randomParents = []
for i in parents_index:
    randomParents.append(parents[i])
#evolving the randomly selected parents
children = evolution_time(randomParents)

#calculating the score from the children generated by the evolution of parents
evolutionScore = best_children(children, video_ed_request, randomEP)
if evolutionScore:
    best_score += evolutionScore[2]

generation = 0
best_generations = []


#evolving the children generated by the parents (further evolution)
children = evolution_time(children)
child = best_children(children, video_ed_request, randomEP)
if child:
    best_score += child[2]


# ****************************** EVALUATING GENETIC ALGORITHM PARAMETERS *******************************

# if there are no better solutions from the generation of children, then lets mutate some of them!
child_index = sample(range(0, len(children)), 4)

#choose 4 random lists of these children lists to mutate
for i in child_index:
    mutate_children = mutation_algorithm(number_of_caches, number_of_videos, children[i], randomEP, video_ed_request,
                                         video_size_desc)

if mutate_children[0] > max(mutation):
    best_generations.append(child)
    best_score.append(mutate_children[0])

best_score += mutation

print("BEST OVERALL SCORE:", max(best_score))

# ************************ TIME *************************````````````````````
end = time.time()
print("time taken:", end - start)
