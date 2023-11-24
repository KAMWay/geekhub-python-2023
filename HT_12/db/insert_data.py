import sqlite3

con = sqlite3.connect("atm.db")
cur = con.cursor()

cur.execute('''INSERT INTO users (username, password)
               VALUES ('admin', 'admin'),
                      ('user1', 'password1');''')
con.commit()

cur.execute('''INSERT INTO atm (info)
               VALUES ('test ATM');''')
con.commit()

cur.execute('''INSERT INTO atm_banknotes (atm_id, denomination, amount) 
               VALUES (1, 10, 1),
                      (1, 20, 2),
                      (1, 50, 3),
                      (1, 100, 4),
                      (1, 200, 5),
                      (1, 500, 6),
                      (1, 1000, 7);''')
con.commit()

con.close()
