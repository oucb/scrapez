from flask_caching import Cache
cache = Cache()
cache_kwargs = {
    'config': {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': 'redis://localhost'
    }
}
EXTENSIONS = [
    (cache, cache_kwargs),
]
