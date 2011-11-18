from __future__ import division


def average(reviews, attr):
  """Compute the average value of an attribute."""
  average = 0.0
  valid = 0
  for review in reviews:
    try:
      average += getattr(review, attr)
    except AttributeError:
      continue
    else:
      valid += 1
  try:
    return average / valid
  except ZeroDivisionError as e:
    raise e
