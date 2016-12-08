import functools as f


def compose(*functions):
    """ A compose function which I've taken directly from:
        https://mathieularose.com/function-composition-in-python/
        """
    def compose2(g, h):
        return lambda x: g(h(x))
    return f.reduce(compose2, functions, lambda x: x)

