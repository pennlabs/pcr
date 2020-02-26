import time

import MySQLdb as db


class Extractor(object):
  def __init__(self, db_name, db_user, db_pwd):
    self.db = db.connect(db=db_name, user=db_user, passwd=db_pwd)

  def run_query(self, query_str, args=None):
    start = time.time()
    cursor = self.db.cursor()
    cursor.execute(query_str, args)
    results = cursor.fetchall()
    print query_str
    print "Took: %s" % (time.time() - start)
    print "Founds %s results.\n" % len(results)
    return results

  def select(self, fields, tables, conditions=None,
      group_by=None, order_by=None):
    query = ["SELECT", ", ".join(fields), "FROM", ", ".join(tables)]
    if conditions:
      items = ['%s="%s"'% (k, v) for k, v in conditions.items()]
      query.extend(["WHERE", " AND ".join(items)])
          
    if group_by:
      query.extend(["GROUP BY", ", ".join(group_by)])
    if order_by:
      query.extend(["ORDER BY", ", ".join(order_by)])
    return self.run_query(" ".join(query))
