from tkinter import *
from tkinter import messagebox
import sqlite3
from tktooltip import ToolTip
import subprocess
import os
from time import sleep
import json

TITLE = 'Password Manager'
LENGTH = 250
WIDTH = 250

conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Just a reference for the code used to set up the database structure.
# c.execute("""
# CREATE TABLE data (
# url text,
# username text,
# password text,
# uid text
# )
# """)