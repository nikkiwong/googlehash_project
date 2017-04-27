
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
                ep_to_cache_latency[i].append(ep_to_dc_latency[i])

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

#
#
# data = read_google("input/sample.in")
# print(data["number_of_requests"])
# sum = 0
# for i in data["video_ed_request"]:
#     sum += int(data["video_ed_request"][i])
# print("number of individual requests=", sum, " which is different from the number of request descriptions ", data["number_of_requests"])
# print(data["ed_cache_list"])
# # print(data["number_of_caches"])
# print("end point to cache latency for endpoint 0: ", data["ep_to_cache_latency"][0])
# print(data["video_size_desc"])
# print("number of videos: ", data["number_of_videos"])
# print("end point to cache latency for endpoint 0: ", data["ep_to_cache_latency"][0])
#
# for key, value in data["video_ed_request"].items():
#     # for i in range(0, len())
#         if '1' in key[1]:
#             print(key[0], value)
# a,b,c,d,e,f,g,h,i,j,k,l,= 1,2,3,4,5,12,6,7,8,9,10,11
# list = [[a,b,c], [d,e,f],[g,h,i],[j,k,l]]
# print(list[0])
# d = {i:list[i] for i in range(len(list))}
# print(d)
#
# print({i : chr(65+i) for i in range(4)})
#
