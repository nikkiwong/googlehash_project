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

#************************ FUNCTIONS ************************************

def add_video_to_cache(video_ed_request, ed_cache_list, list_cache, video_size_desc):
    #This function adds videos to the cache
    for key, value in video_ed_request.items():
        #using the dictionary provided, I iterate through the dictionary.
        for cache in ed_cache_list[int(key[1])]:
            #for each cache that is linked to the current endpoint
            list_cache[cache].add_video_to_cache(int(key[0]), video_size_desc[int(key[0])], int(value))
            #add the current video into to the cache that is linked to the current endpoint.

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
    randomSelection = []

    for cache in range(0, number_of_caches):
        for video in range(0, number_of_videos):

            if list_cache[cache].hill_climb(video, video_size_desc[video]):
                best_time(video_ed_request, list_cache, list_endpoint)
                new_score = score(list_endpoint)
                # print("dog:", new_score)
                if maximum < new_score:
                    maximum = new_score
                    parent.append(copy.deepcopy(list_cache))
                    # print("cat", maximum)

    parent_index = sample(range(len(parent)//2, len(parent)), 4)
    for i in parent_index:
        #storing only the cache list that is at the index randomly chosen from above.
        randomSelection.append(parent[i])
    #from the list of best cache list (matrices) I will pick a random 4 from the last 50% of the list
    #because the best lists are added to the end of parent.
    return maximum, randomSelection

@jit
def RS_algorithm(number_of_caches, number_of_videos, list_cache, list_endpoint, video_ed_request, video_size_desc):
    randomMax=0
    x=0
    for cacheNum in range(0, number_of_caches):
        while x<(number_of_videos)*100:
            n = randint(0, number_of_videos-1)
            list_cache[cacheNum].random_search(n, video_size_desc[n])
            x+=1
    return randomMax

@jit
def mutation_algorithm(number_of_caches, number_of_videos, list_cache, bestTime, scoreEP, video_size_desc):
    mutate_Max=0
    x=0
    parents = []
    randomSelection =[]

    for cacheNum in range(0, number_of_caches):
        while x<1000:
            n = randint(0, number_of_videos-1)
            # print("n = ",n)
            if list_cache[cacheNum].mutate_solution(n, video_size_desc[n]):
                # print("I'm IN!")
                best_time(video_ed_request, list_cache, list_endpoint)
                new_score = score(list_endpoint)
                if n%2==0 and new_score<mutate_Max:
                    #storing a random cache list if the random number generated (n)
                    #is divisible by 2. Implementing the simulated annealing here
                    #by taking cache list that is not the best solution.
                    parents.append(copy.deepcopy(list_cache))
                    # for parent in parents:
                        # print("parents:", parent)
                if new_score>mutate_Max:
                    # print("inside GA algo", GA_Max)
                    mutate_Max= new_score
                    # print("inside GA algo", GA_Max)
            x+=1
    # print("PARENTS",parents)
    parent_index = sample(range(len(parents)//2, len(parents)), 4)
    for i in parent_index:
        randomSelection.append(parents[i])
    return mutate_Max, randomSelection

def evolution_time(parents):
    children = []
    while len(children) < len(parents):
        # making 20 children, generated from a random 20 selection of parents
        A = randint(0, len(parents) - 1)
        B = randint(0, len(parents) - 1)
        if A != B:
            parent_A = parents[A]
            parent_B = parents[B]
            half = len(parent_A) // 2
            child = parent_A[:half] + parent_B[half:]
            children.append(child)
            #so we have the same amount of children compared to parents
    return children

@jit
def best_children(children, video_ed_request, list_endpoint):
    best_new_score = []
    new_children = []
    for child in children:
        best_time(video_ed_request, child, list_endpoint)
        child_score = score(list_endpoint)
        # print("evolved child score: ", child_score)
        if child_score > max(mutation):
            best_new_score.append(child_score)
            new_children.append(child)
    if best_new_score == []:
        return False
    else:
        return True, new_children, best_new_score

#************************ CREATING CACHE AND ENDPOINT OBJECTS ************************************

list_endpoint = []
list_cache = []

for endpoint in range(0, number_of_endpoints):
    # puts all the endpoint objects into a list for easy access
    endpoint = Endpoint(ep_to_dc_latency[endpoint], ep_to_cache_latency[endpoint])
    list_endpoint.append(endpoint)


for cache in range (0, number_of_caches):
    #creating cache objects
    cache = Cache(cache_size, number_of_videos)
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


hillClimbScore = HC_algorithm(number_of_caches, number_of_videos, randomCache, video_size_desc, video_ed_request, randomEP)
if originalMaximum<hillClimbScore[0]:
    print("new score", hillClimbScore[0])
    randomMaximum = hillClimbScore[0]

#storing the local best solutions
parents += hillClimbScore[1]

print("Finished Hill Climb...")

print("best Hill Climb score", randomMaximum)

print("Number of good hill climb cache list:", len(parents))

#************** GENETIC ALGORITHM *************************

# --- Part 1: Mutation ---
print("")
print("Starting mutation algorithm...")
count=0
entering = 1
mutation = []
while count<12:
    mutation_score = mutation_algorithm(number_of_caches, number_of_videos, randomCache, randomEP, video_ed_request, video_size_desc)
    if originalMaximum <= mutation_score[0]:
        #want to keep the cache matrices that give scores higher than the original cache list.
        parents.append(copy.deepcopy(randomCache))
        mutation.append(mutation_score[0])
        #storing the best 20 cache lists.
        # print("COUNTCOUNT",count)
        # print("adding to list:", entering)
        # entering+=1
        # print("best mutation algorithm score:", mutation_score[0])
        count += 1
        # print("mutation score:", mutation_score[1])
parents+=mutation_score[1]
print("Finished mutation algorithm...")
print("best mutation algorithm score:", max(mutation))

# --- Part 2: Evolution ---
print("Time to evolve!")
children = evolution_time(parents)
print("Evolution complete")
best_score = []
evolutionScore = best_children(children, video_ed_request, randomEP)
if evolutionScore:
    best_score += evolutionScore[2]
    print("Awesome! We have some children with better score than the parent!")
    print("Let's see if we can generate an even better generation!")
    print("Best score from the children:", max(best_score))
else:
    print("Nope... no good children this time round! Lets make more!")

generation = 0
best_generations = []
best_score = []
while generation<5:
    # we are generating new children using the previous generations children (up to 5 generations)
    #Let the work of evolution in generations begin
    # print(len(children))
    children = evolution_time(children)
    child = best_children(children, video_ed_request, randomEP)
    if child:
        best_score += child[2]
    generation+=1

if best_score!=[]:
    print("The best overall solution from the genetic algorithm:", max(best_score))
else:
    print("Genetic algorithm for 5 generations didn't provide a better solution compared to the solution produced by the parent." )

#****************************** EVALUATING GENETIC ALGORITHM PARAMETERS *******************************

#if there are no better solutions from the generation of children, then lets mutate them!
x=0
print("")
print("Let's try mutating the children")

while x < 20:
    #mutating 20 generation of children
    for child in children:
        mutate_children = mutation_algorithm(number_of_caches, number_of_videos, child, randomEP, video_ed_request,
                                        video_size_desc)
        # print("mutate children",mutate_children[0])
        if mutate_children[0]>max(mutation):
            # print(x)
            best_generations.append(child)
            best_score.append(mutate_children[0])
            # print("Better than parent mutation:", mutate_children[0])
    x+=1

if max(best_score)>max(mutation):
    print("After trying mutating the children, the best overall score from genetic algorithm:",max(best_score))
else:
    print("Mutating the children for 20 generations didn't provide a better solution compared to the solution produced by the parent." )
    print("Parent score:", max(mutation))



#************************ TIME *************************````````````````````
end = time.time()
print("time taken:", end - start)