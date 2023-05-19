import abc
from typing import Dict


# This file containes design patterns
class SingletonMeta(type):
    """Meta Singleton class"""

    _instances: Dict = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABCMeta(abc.ABCMeta):
    """Abstract and meta Singleton class"""

    _instances: Dict = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Decorator
def singleton(cls):
    """Singleton decorator"""
    instance: Dict = None

    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


class SingletonMetaWithArgs(type):
    """Meta Singleton class with arguments. One object is created for each set of arguments"""

    _instances: Dict = dict()

    def __call__(cls, *args, **kwargs):
        # Get instance key
        instance_key = cls.__repr_args__(*args, **kwargs)
        if cls not in cls._instances.keys():
            cls._instances[cls] = dict()
        # Create instance if not exists
        if instance_key not in cls._instances[cls].keys():
            cls._instances[cls][instance_key] = super(
                SingletonMetaWithArgs, cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls][instance_key]

    @staticmethod
    def __repr_args__(*args, **kwargs):
        return str(args) + str(kwargs)


class SingletonABCMetaWithArgs(abc.ABCMeta):
    """Abstract and Meta Singleton class with arguments. One object is created for each set of arguments"""

    _instances: Dict = dict()

    def __call__(cls, *args, **kwargs):
        # Get instance key
        instance_key = cls.__repr_args__(*args, **kwargs)
        if cls not in cls._instances.keys():
            cls._instances[cls] = dict()
        # Create instance if not exists
        if instance_key not in cls._instances[cls].keys():
            cls._instances[cls][instance_key] = super(
                SingletonABCMetaWithArgs, cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls][instance_key]

    @staticmethod
    def __repr_args__(*args, **kwargs):
        return str(args) + str(kwargs)


# Decorator
def singletonWithArgs(cls):
    """SingletonWithArgs decorator"""
    instances: Dict = dict()

    def wrapper(*args, **kwargs):
        nonlocal instances
        instance_key = SingletonMetaWithArgs.__repr_args__(*args, **kwargs)
        if instance_key not in instances.keys():
            instances[instance_key] = cls(*args, **kwargs)
        return instances[instance_key]

    return wrapper
