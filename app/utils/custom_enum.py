from enum import Enum

class CustomEnum(Enum):
    """Custom Enum class with some custom methods"""

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_