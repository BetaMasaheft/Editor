import itertools as it

# from https://docs.python.org/dev/library/itertools.html#itertools-recipes
def partition(pred, iterable):
    t1, t2 = it.tee(iterable)
    return it.filterfalse(pred, t1), filter(pred, t2)

