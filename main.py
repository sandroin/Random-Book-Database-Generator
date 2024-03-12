import sqlite3
import random


def name_generator():
    pronouns = ["The", "My", "His", "Our", "Her", "John's", "Jane's"]
    adjectives = ["Unforgettable", "Scary", "Mysterious", "Mystic", "Amazing", "Wonderful", "Incredible",
                  "Intriguing", "Abandoned"]
    nouns = ["Adventure", "House", "City", "Child", "Creature", "Village", "Region"]
    return f"{random.choice(pronouns)} {random.choice(adjectives)} {random.choice(nouns)}"


def pages_generator():
    return random.randint(200, 600)


def cover_type_generator():
    cover_types = ["Hardcover", "Paperback"]
    return random.choice(cover_types)


def category_generator():
    categories = ["Fantasy", "Mystery", "Thriller", "Horror", "Adventure", "Detective"]
    return random.choice(categories)


connection = sqlite3.connect('book.db')

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS books")

cursor.execute("""CREATE TABLE books (
                name text,
                pages integer,
                cover_type text,
                category text
                );""")

for _ in range(10):
    cursor.execute("INSERT INTO books (name, pages, cover_type, category) VALUES (?, ?, ?, ?)",
                   (name_generator(), pages_generator(), cover_type_generator(), category_generator()))
connection.commit()

cursor.execute("""SELECT * FROM books""")

rows = cursor.fetchall()

for row in rows:
    print(row)
print("\n-----------------------------------------------------------------------------------\n")

cursor.execute("""SELECT avg(pages) from books""")
avg_pages = cursor.fetchone()[0]

print("Average number of pages is {}.".format(avg_pages))

cursor.execute("""SELECT name FROM books WHERE pages = (SELECT max(pages) from books)""")
max_pages = cursor.fetchone()[0]

print("{} has the most pages.".format(max_pages))

connection.close()
