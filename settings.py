from tkinter import *
from tkinter import messagebox
import sqlite3

TITLE = 'Password Manager'
LENGTH = 400
WIDTH = 400

conn = sqlite3.connect('passwords.db')
c = conn.cursor()


# c.execute("""
# CREATE TABLE username_password (
# username text,
# password text
# )
# """)
#
# c.execute("""
# CREATE TABLE websites (
# url text,
# username_id int
# )
# """)

# c.execute("ALTER TABLE websites RENAME COLUMN username_id to username")