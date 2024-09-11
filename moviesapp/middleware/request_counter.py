from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Initialize the key if it doesn't exist
        if cache.get('request_count') is None:
            cache.set('request_count', 0)
        # Increment the request count key in Redis
        cache.incr('request_count', 1)
