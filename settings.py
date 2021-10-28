from tkinter import *
from tkinter import messagebox
import sqlite3
from tktooltip import ToolTip

TITLE = 'Password Manager'
LENGTH = 250
WIDTH = 250

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
# CREATE TABLE data (
# url text,
# username_id text,
# password text
# )
# """)

# c.execute("ALTER TABLE data RENAME username_id TO username")