
"""
dataflow - Objects with dataflow semantics
Alberto Bertogli (albertito@blitiri.com.ar)
"""

import thread
import threading

class DFObject(object):
  "Object with dataflow semantics"
  def __init__(self):
    self.__isset = False
    self.__value = None
    self.__lock = threading.Condition()

  def getval(self):
    self.__lock.acquire()
    while not self.__isset:
      self.__lock.wait()
    self.__lock.release()
    return self.__value

  def setval(self, value):
    self.__lock.acquire()
    self.__value = value
    self.__isset = True
    self.__lock.notifyAll()
    self.__lock.release()

  val = property(getval, setval)

  def unset(self):
    self.__lock.acquire()
    self.__value = None
    self.__isset = False
    self.__lock.release()


class _DFWrapper:
  """Dataflow wrapper class for the decorator defined below.
  It's closely related so don't use it.

  We don't use a new-style class, otherwise we would have to implement
  stub methods for __getattribute__, __hash__ and lots of others that
  are inherited from object by default. This works too and is simple.
  I'll deal with them when they become mandatory.
  """
  def __init__(self):
    self._override = True
    self._isset = False
    self._value = None
    self._lock = threading.Condition()
    self._override = False

  def _wait(self):
    self._lock.acquire()
    while not self._isset:
      self._lock.wait()
    self._lock.release()

  def __getattr__(self, name):
    if self.__dict__['_override']:
      return self.__dict__[name]
    self._wait()
    return self._value.__getattribute__(name)

  def __setattr__(self, name, val):
    if name == '_override' or self._override:
      self.__dict__[name] = val
      return
    self._wait()
    setattr(self._value, name, val)
    return

def dataflow(f):
  "Dataflow decorator"
  def threadedf(obj, *args, **kwargs):
    v = f(*args, **kwargs)
    obj._override = True
    olock = obj._lock
    olock.acquire()
    obj._value = v
    obj._isset = True
    obj._wait = lambda: True
    obj._override = False
    olock.notifyAll()
    olock.release()

  def newf(*args, **kwargs):
    o = _DFWrapper()
    thread.start_new_thread(threadedf, (o,) + args, kwargs)
    return o

  return newf



