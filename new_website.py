from settings import *

def save_click(window, website, username, password):
    """
    What happens when you click the save button.
    :return: None
    """
    c.execute("""INSERT INTO data (url, username, password) 
    VALUES ('""" + website + """', '""" + username + """', '""" + password + """');""")
    conn.commit()
    messagebox.showinfo('Save', 'Username / Password Saved!', parent=window)
    window.destroy()



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
    save_button = Button(window, text='Save', command=lambda: save_click(window, website_entry.get(),
                                                                         username_entry.get(), password_entry.get()))

    # Configs

    # Draw elements to window
    website.pack()
    website_entry.pack()
    username.pack()
    username_entry.pack()
    password.pack()
    password_entry.pack()
    save_button.pack(pady=15)

    # Tooltips
    ToolTip(save_button, msg='Saves the entry into the database.', delay=0.5)