# This file containes design patterns
class Singleton(object):
    """Singleton class"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance


# Decorator
def singleton(cls):
    """Singleton decorator"""
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


class SingletonWithArgs(object):
    """Singleton class with arguments. One object is created for each set of arguments"""

    def __new__(cls, *args, **kwargs):
        # Get instance key
        instance_key = cls.__repr_args__(*args, **kwargs)
        # Create instance dict if not exists
        if not hasattr(cls, "_instance_dict"):
            cls._instance_dict = {}
        # Create instance if not exists
        if instance_key not in cls._instance_dict:
            cls._instance_dict[instance_key] = super(SingletonWithArgs, cls).__new__(
                cls
            )
        # Return instance
        return cls._instance_dict[instance_key]

    @staticmethod
    def __repr_args__(*args, **kwargs):
        return str(args) + str(kwargs)
