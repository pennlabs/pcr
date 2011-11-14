from __future__ import division


ERROR = u"\u00A0" #empty string


def average(reviews, attr):
  average = 0.0
  valid = 0
  for review in reviews:
    try:
      average += getattr(review, attr)
    except AttributeError:
      continue
    else:
      valid += 1
  if valid > 0:
    return "%.2f" % average / valid
  else:
    return ERROR


