import shelve
import time

# https://github.com/wrobell/geotiler/blob/a85f2c39fbacdc54b5bd2d818186d364138ad0d6/examples/ex-shelvecache.py#L43
class Cache:
    def __init__(self, filename):
        self.cache = shelve.open(filename, writeback=True)

    def get(self, key):
        try:
            data = self.cache[key][0]
        except:
            data = None
        return data


    def set(self, key, data):
        if key not in self.cache:
            self.cache[key] = (data, time.time())
        return


    def close(self):
        self.cache.close()
