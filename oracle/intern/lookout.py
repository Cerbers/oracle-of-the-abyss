import time 
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

Parameters = ParamSpec('P')
Result = TypeVar('Result')

def watch_running_time_of_function(func: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
    @wraps(func)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__}: {elapsed:.3f}s")
        return result
    return wrapper