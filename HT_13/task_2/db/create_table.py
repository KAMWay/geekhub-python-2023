import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS persons(
            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            name        TEXT        NOT NULL UNIQUE,
            lastname    TEXT        NOT NULL UNIQUE,
            role        TEXT        NOT NULL DEFAULT 'STUDENT' ,
            UNIQUE (name, lastname)
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS authors(
            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT        NOT NULL UNIQUE
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS books(
            id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
            author_id           INTEGER     NOT NULL,
            title               TEXT        NOT NULL,
            publisher_info      TEXT        NOT NULL,
            number              INTEGER     DEFAULT 0 CHECK(number >= 0),
            number_available    INTEGER     DEFAULT 0 CHECK(number >= number_available and number_available>=0),
            UNIQUE (author_id, title, publisher_info),
            FOREIGN KEY (author_id) REFERENCES authors (id) ON DELETE CASCADE
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS categories(
            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            info        TEXT        NOT NULL UNIQUE
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS books_categories(
            book_id         INTEGER     NOT NULL,
            category_id     INTEGER     NOT NULL,
            UNIQUE (book_id, category_id),
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE 
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS persons_books(
            person_id   INTEGER     NOT NULL,
            book_id     INTEGER     NOT NULL,
            UNIQUE (person_id, book_id),
            FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE 
            );''')

con.close()



# cur.execute('''CREATE TABLE IF NOT EXISTS groups(
#             id      INTEGER     PRIMARY KEY AUTOINCREMENT,
#             info    TEXT        NOT NULL UNIQUE
#             );''')


# cur.execute('''CREATE TABLE IF NOT EXISTS student_group(
#             person_id   INTEGER     NOT NULL UNIQUE,
#             group_id    INTEGER     NOT NULL,
#             FOREIGN KEY (person_id)  REFERENCES persons (id) ON DELETE CASCADE,
#             FOREIGN KEY (group_id)   REFERENCES groups (id) ON DELETE CASCADE
#             );''')
#
# cur.execute('''CREATE TABLE IF NOT EXISTS teacher_groups(
#             person_id   INTEGER     NOT NULL,
#             group_id    INTEGER     NOT NULL,
#             UNIQUE (person_id, group_id),
#             FOREIGN KEY (person_id)  REFERENCES persons (id) ON DELETE CASCADE,
#             FOREIGN KEY (group_id)   REFERENCES groups (id) ON DELETE CASCADE
#             );''')

