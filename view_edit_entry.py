from settings import *

def initialize(window, website):
    """
    Sets up main window elements.
    :param window: the window popup
    :return: None
    """
    # Fetch database entries
    c.execute("SELECT url, username, password FROM data where url = '" + website + "'")
    results = c.fetchall()
    print(results)

    # Nested functions
    def delete_click():
        answer = messagebox.askyesno('Delete', 'Are you sure you want to delete?', parent=window)
        if not answer:
            return
        selected = clicked.get()
        entry = None
        for element in results:
            if element[1] == selected:
                entry = element
                break
        c.execute("""
        DELETE FROM data WHERE url = '""" + entry[0] + """' 
        AND username = '""" + entry[1] + """'""")
        conn.commit()

    def copy_username():
        """
        Copies username to the clipboard.
        :return: None
        """
        selected = clicked.get()
        window.clipboard_clear()
        window.clipboard_append(selected)

    def copy_password():
        """
        Copies password to the clipboard.
        :return: None
        """
        selected = password_entry.get()
        window.clipboard_clear()
        window.clipboard_append(selected)

    def update_password_field(click):
        """
        Updates the password field upon selecting a username. Returns first match it finds.
        :param click: string of what was clicked in the drop down menu
        :return: None
        """
        for element in results:
            if element[1] == click:
                password_entry.delete(0, END)
                password_entry.insert(0, element[2])
                break

    def update_password():
        selected = clicked.get()
        new_password = password_entry.get()
        print(new_password)
        c.execute("""UPDATE data SET password = '""" + new_password + """' 
        WHERE url = '""" + website +"""' AND username = '""" + selected + """'""")
        conn.commit()

    # Label definitions
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')
    website_label = Label(window, text=website)

    # Dropdown definitions
    clicked = StringVar()
    usernames = [user[1] for user in results]
    username_dropdown = OptionMenu(window, clicked, *usernames, command=update_password_field)

    # Input definitions
    password_entry = Entry(window)
    # password_entry.insert(0, clicked)

    # Button definition
    copy_username_button = Button(window, text='Copy', command=copy_username)
    copy_password_button = Button(window, text='Copy', command=copy_password)
    update_button = Button(window, text='Update', command=update_password)
    delete_button = Button(window, text='Delete', command=delete_click)

    # Configs

    # Draw elements to window
    username.grid(row=0, column=0)
    username_dropdown.grid(row=1, column=0)
    copy_username_button.grid(row=1, column=1)
    password.grid(row=2, column=0)
    password_entry.grid(row=3, column=0)
    copy_password_button.grid(row=3, column=1)
    update_button.grid(row=4, column=0)
    delete_button.grid(row=4, column=1)
    website_label.grid(row=5, column=0, columnspan=2, sticky=S)