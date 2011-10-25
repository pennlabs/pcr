from __future__ import division


ERROR = u"\u00A0"


def average(reviews, attr):
  average = 0.0
  valid = 0
  for review in reviews:
    if hasattr(review, attr):
      average += getattr(review, attr)
      valid += 1
  if valid > 0:
    return "%.2f" % round(average / valid, 2)
  else:
    return ERROR


