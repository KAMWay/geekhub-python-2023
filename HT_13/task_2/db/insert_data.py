import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute('''INSERT INTO books (author, title, publisher_info, number, number_available)
               VALUES ('Tom Cruse','Book name 1', 'Publisher info, 2012', 10, 8),
                      ('Albert Someone','Book name 2', 'Publisher info, 2020', 5, 4);
            ''')
con.commit()

cur.execute('''INSERT INTO categories (info) 
               VALUES ('history'),
                      ('chemical'),
                      ('biology');
            ''')
con.commit()

cur.execute('''INSERT INTO persons (name, lastname, role) 
               VALUES ('admin', 'admin', 'ADMIN'),
                      ('Smit', 'Adams', 'STUDENT'),
                      ('Tom', 'Vagner', 'TEACHER'),
                      ('Bill', 'Owner', 'STUDENT');
            ''')
con.commit()

cur.execute('''INSERT INTO persons_books (person_id, book_id) 
               VALUES (1,1),
                      (3,1),                
                      (2,2);
            ''')
con.commit()

cur.execute('''INSERT INTO books_categories (book_id, category_id) 
               VALUES (1,1),
                      (2,1),                
                      (1,2);
            ''')
con.commit()

con.close()
