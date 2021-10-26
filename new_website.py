from settings import *

def save_click(window):
    """
    What happens when you click the save button.
    :return: None
    """
    save_message = messagebox.showinfo('Save', 'Username / Password Saved!', parent=window)


def initialize(window):
    """
    Sets up main window elements.
    :param window: the window popup
    :return: None
    """
    # Label definitions
    website = Label(window, text='Website:')
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')

    # Input definitions
    website_entry = Entry(window)
    username_entry = Entry(window)
    password_entry = Entry(window)

    # Button definition
    save_button = Button(window, text='Save', command=lambda: save_click(window))

    # Configs

    # Draw elements to window
    website.pack()
    website_entry.pack()
    username.pack()
    username_entry.pack()
    password.pack()
    password_entry.pack()
    save_button.pack()