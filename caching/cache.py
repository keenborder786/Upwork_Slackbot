from redis import Redis


class Cache:
    def __init__(self , host , ttl):
        self.cache_client = Redis(host=host, port=6379 , decode_responses = True)
        self.ttl =  ttl