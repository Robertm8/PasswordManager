from settings import *
# import website_list
import login

root = Tk()
root.title(TITLE)
root.geometry('200x200')
root.resizable(False, False)

login.initialize(root)

root.mainloop()
