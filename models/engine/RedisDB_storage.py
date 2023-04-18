from functools import wraps
from redis import Redis
from typing import Callable, Dict, List
import json

def cached(timeout=86400):
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = f"{method.__name__}:{str(args)}:{str(kwargs)}"
            result = self._cache.get(key)
            if result is not None:
                return result.decode('utf-8')
            else:
                result = method(self, *args, **kwargs)
                self._cache.set(key, json.dumps(result), ex=timeout)
                return result
        return wrapper
    return decorator


class Cache:
    def __init__(self):
        self._cache = Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        return self._cache.get(key)
    
    def get_dict(self, key) -> Dict:
        value = self.get(key)
        if value is None:
            return {}
        return json.loads(value)

    def get_list(self, key) -> List:
        result = self.get(key)
        if result is not None:
            return json.loads(result)
        return []

    def delete(self, key):
        return self._cache.delete(key)

    def delete_list_dict_item(self, key, item_key):
        list_of_dicts = self.get_list(key)
        for d in list_of_dicts:
            if item_key in d:
                del d[item_key]
                self.set_list(key, list_of_dicts)
                return True
        return False

    def exists(self, key):
        return self._cache.exists(key)

    def set(self, key, value):
        return self._cache.set(key, value)

    def set_list(self, key, values):
        for value in values:
            self._cache.lpush(key, value)

    @cached(timeout=86400)
    def set_dict(self, key, value: Dict):
        self.set(key, json.dumps(value))

    @cached(timeout=86400)
    def set_cache(self, key, value):
        if isinstance(value, bool):
            value = int(value)
        elif isinstance(value, dict):
            value = str(value)
        return self._cache.set(key, value, ex=86400)
