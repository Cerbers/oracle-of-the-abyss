# Style Guide

`//` - comment for code blocks and examples in this document



## Imports
- Order: external > standard library > local
- Group import by type
- Separate type groups with one blank line
- Example:
```python
import fastapi
import nltk

import os
import pathlib

from oracle.main import something
from oracle.analysis.rhymes import get_rhymes
```


## Docstrings
- Format: Similar to Google Style
- Two versions: short (one line) and long (multi-line)
- Short version: `"""Brief description."""`
- Long version: `"""Brief description or detailed description

    Parameters, returns, examples etc.
    """`
- Order: description, parameters (args), returns, notes, examples
- Example should show what happens when the function is called with specific arguments
- Example:
```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description // optional
    
    Detailed description with parameters, returns, and raises.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
    
    Returns:
        Description of return value.
    
    Notes:
        Additional notes.
    
    Examples:
        >>> example_function("test", 1)
        True
    """
    return True
```

Ideally docstrings size grows in relation to complexity of function/object.
**Rationale for docstring format**:
- Having clear examples helps with understanding the fucntion's behavior and usage
- Notes might be needed for edge cases or important considerations which can't be in comments
- Having all information in one place makes it easier to map mentally function's behavior rather than running tests or spending extra time testing in the interpreter

## Naming
- Use descriptive names for variables, functions, and classes
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use UPPER_SNAKE_CASE for constants
- Avoid single letter variable names except for loop counters and mathematical operations
