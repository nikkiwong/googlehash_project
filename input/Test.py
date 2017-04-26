class Test:
    def test_cache_overflow(cache_array, cache_size):
        for i in cache_array:
            if i>cache_size or i<0:
                return -1

