def infinite_iterator(iterator):
    """Infinite iterator

    :param iterator: iterator
    :type iterator: iterator
    :yield: item from iterator
    :rtype: Any
    """
    while True:
        for item in iterator:
            yield item


def property_with_cache(func):
    """Property decorator to cache the result of a property. The result is cached in the attribute of name "_{func.__name__}".

    :param func: function to decorate
    :type func: function
    :return: decorated function
    :rtype: function
    """
    @property
    def decorated_func(*args, **kwargs):
        raise RuntimeError("Deprecated. use functools.cached_property instead.")
    return decorated_func
