from settings import *
import website_list

root = Tk()
root.title(TITLE)
root.geometry(str(LENGTH)+'x'+str(WIDTH))
root.resizable(False, False)

website_list.initialize(root)

root.mainloop()
