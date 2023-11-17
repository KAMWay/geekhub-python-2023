import sqlite3

con = sqlite3.connect("atm.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
           (id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            username    TEXT        NOT NULL UNIQUE,
            password    TEXT        NOT NULL);''')

cur.execute('''CREATE TABLE IF NOT EXISTS user_balance
           (user_id     INTEGER     NOT NULL UNIQUE,
            balance     REAL        DEFAULT 0 CHECK(balance >= 0),
            FOREIGN KEY (user_id)   REFERENCES users (id) ON DELETE CASCADE );''')

cur.execute('''CREATE TABLE IF NOT EXISTS user_transactions 
           (user_id     INTEGER     NOT NULL,
            dt          DATETIME    NOT NULL,
            amount      REAL,
            balance     REAL        CHECK(balance >= 0),
            FOREIGN KEY (user_id)   REFERENCES users (id) ON DELETE CASCADE );''')

cur.execute('''CREATE TABLE IF NOT EXISTS atm
           (id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            info        TEXT);''')

cur.execute('''CREATE TABLE IF NOT EXISTS atm_banknotes
           (atm_id          INTEGER     NOT NULL,
            denomination    INTEGER     CHECK(denomination >= 0),
            amount          INTEGER     CHECK(amount >= 0),
            UNIQUE (atm_id, denomination),
            FOREIGN KEY (atm_id)        REFERENCES atm (id) ON DELETE CASCADE );''')

con.close()
