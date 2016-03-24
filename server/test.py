from __future__ import print_function

import pymysql

conn = pymysql.connect(host='127.0.0.1',  user='ruser', passwd='pass', db='restforum')

cur = conn.cursor()

cur.execute("SELECT * FROM users")

#print(cur.description)

print()

for row in cur:
   print(row[1])

cur.close()
conn.close()
