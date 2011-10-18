from __future__ import division


ERROR = u"\u00A0"


def average(reviews, attr):
  average = 0.0
  valid = 0
  for review in reviews:
    if attr in review:
      average += review[attr]
      valid += 1
  if valid > 0:
    average = str(round(average / valid, 2))
    if len(average) < 4:
      average += '0' * (4 - len(average))
    return average
  else:
    return ERROR


