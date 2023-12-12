from typing import Any


class ValidationError:
    """Custom Validation error for api"""

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        (pass)