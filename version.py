from settings import *

def initialize(window):
    """
    Sets up main window elements.
    :param window: the window popup
    :return: None
    """
    # Label definitions
    version = Label(window, text='Version Info: 1.0')
    updates = Label(window, text='Latest Update: \n Added database. \n Cleaned up aesthetics.')

    # Draw elements to window
    version.pack()
    updates.pack()
