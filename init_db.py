# flask_blog/init_db.py
import sqlite3


def main():
    # open a connection between python script and database.db to create it
    connection = sqlite3.connect('database.db')

    # open the schema.sql to read what inside it
    with open('schema.sql') as f:
        connection.executescript(f.read())

    # make the cursor to execute what inside the schema in database
    cur = connection.cursor()

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('First Post', 'Content for the first post')
                )

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('Second Post', 'Content for the second post')
                )

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                ('user', 'pass')
                )
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
