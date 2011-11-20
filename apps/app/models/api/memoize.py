import functools
import cPickle

def memoize(func):
  cache = {}
  @functools.wraps(func)
  def memoized(*args, **kwargs):
    hash_ = cPickle.dumps((args, set(kwargs.iteritems())))
    try:
      return cache[hash_]
    except KeyError:
      #this is potentially dangerous
      cache[hash_] = func(*args, **kwargs)
      return cache[hash_]
  return memoized
