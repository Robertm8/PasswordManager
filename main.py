# Main file for program. Run this.

from settings import *
import login

root = Tk()
root.title(TITLE)
root.geometry('200x200')
root.resizable(False, False)

login.initialize(root)

root.mainloop()
