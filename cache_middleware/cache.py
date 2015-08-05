from storage import FileCache, RedisCache, MemoryCache


class Cache(object):
    STORAGE_CLASSES = {
        'file': FileCache,
        'redis': RedisCache,
        'memory': MemoryCache
    }

    def __init__(self, config):
        if 'storage_type' not in config:
            raise AttributeError('you must specify storage type in the configuration dictionary')
        elif config['storage_type'] not in self.STORAGE_CLASSES:
            raise KeyError('there is no such storage type %s. '
                           'Please, choose one from available storage types: %s'
                           % (config['storage_type'], ', '.join(self.STORAGE_CLASSES.keys())))
        else:
            spec_config = {key: value for key, value in config.items() if key != 'storage_type'}
            self.storage = self.STORAGE_CLASSES[config['storage_type']](**spec_config)

    def __getitem__(self, url):
        return self.storage[url]

    def __setitem__(self, url, response):
        self.storage[url] = response

    def __contains__(self, url):
        return url in self.storage
