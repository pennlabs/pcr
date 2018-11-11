import sys, MySQLdb

db=REDACTED

for file in sys.argv:
    if '../adddepts.py' == file:
        continue
    if '' == file:
        continue

    c = db.cursor()
    dept = "".join([x.capitalize() for x in file.split('.')[0]])
    c.execute("""INSERT INTO courses_department (code, name) VALUES (%s, %s)""", (dept, dept))
    
