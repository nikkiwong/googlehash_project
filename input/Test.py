from REmain import add_video_to_cache, score, best_time, HC_algorithm, RS_algorithm, mutation_algorithm, evolution_time, best_children
from REcache import Cache
from REendpoint import Endpoint
import testfile
import unittest



class Test(unittest.TestCase):

    def test_cache_overflow(self):
        T = testfile
        cache0 = Cache(100, 5)
        cache0.add_video_to_cache(2, 33, 10)
        add_video_to_cache(T.video_ed_request, T.ed_cache_list, T.list_cache, T.video_size_desc)
        cacheSize0 = cache0.get_cache_size()
        cs0 = T.list_cache[0].get_cache_size()
        self.assertEqual(cs0, cacheSize0, "size total don't match")

def main():
    unittest.main(verbosity=0)


if __name__ == '__main__':
    main()

