import time 
import os
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

Parameters = ParamSpec('Parameters')
Result = TypeVar('Result')

def watch_running_time_of_function(func: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
    @wraps(func)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        if os.getenv("ORACLE_LOOKOUT") == "1":
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{func.__name__}: {elapsed:.3f}s")
            return result
        
        return func(*args, **kwargs)
    return wrapper