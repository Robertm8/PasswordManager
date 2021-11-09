from settings import *

def translate_results(results):
    """
    Function for decrypting usernames / passwords for a website.
    :param results: encrypted list with a tuple of url / username / password for each username
    :return: decrypted list with a tuple of url / username / password for each username
    """
    print(results)

    decrypted_results = []

    # Open encryption microservice
    for username_pass in results:
        url = username_pass[0]
        subprocess.run(['python', '-m', 'crypto-service', '-d', '-uid', username_pass[3],
                        '-u', username_pass[1], '-p', username_pass[2]])
        sleep(0.05)  # to give enough time for microservice to respond
        RESULTS_FILENAME = 'crypto-service-results.json'

        # Locate file created
        path_to_results = os.path.join('.\\', RESULTS_FILENAME)

        # Load data from file into variables
        with open(path_to_results, 'r') as file:
            u_p_data = json.load(file)
            d_username = u_p_data['username']
            d_password = u_p_data['password']
            uid = u_p_data['uid']

        # Load the decrypted results into new list to be returned
        decrypted_results.append((url, d_username, d_password, uid))

    # Remove files after finishing with them
    os.remove('crypto-service-results.json')

    return decrypted_results

# Will possibly be used for update password, currently unavailable
# def fetch_updated_info(username, password):
#     return

def initialize(window, website):
    """
    Sets up main window elements.
    :param window: the window popup
    :return: None
    """
    # Fetch database entries
    c.execute("SELECT url, username, password, uid FROM data where url = '" + website + "'")
    results = c.fetchall()
    decrypted_results = translate_results(results)
    print(decrypted_results)

    # Nested functions
    def delete_click():
        answer = messagebox.askyesno('Delete', 'Are you sure you want to delete?', parent=window)
        if not answer:
            return
        selected = clicked.get()
        entry = None
        for element in decrypted_results:
            if element[1] == selected:
                entry = element
                break
        c.execute("DELETE FROM data WHERE uid = '" + entry[3] + "';")
        conn.commit()
        window.destroy()

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
        for element in decrypted_results:
            if element[1] == click:
                password_entry.delete(0, END)
                password_entry.insert(0, element[2])
                break

    # Update password feature currently unavailable
    # def update_password():
    #     selected = clicked.get()
    #     new_password = password_entry.get()
    #     # old_uid, new_uid, e_username, e_password = fetch_updated_info(selected, new_password)
    #     print(new_password)
    #     c.execute("""UPDATE data SET password = '""" + new_password + """'
    #     WHERE url = '""" + website +"""' AND username = '""" + selected + """'""")
    #     conn.commit()

    # Label definitions
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')
    website_label = Label(window, text=website)

    # Dropdown definitions
    clicked = StringVar()
    usernames = [user[1] for user in decrypted_results]
    username_dropdown = OptionMenu(window, clicked, *usernames, command=update_password_field)

    # Input definitions
    password_entry = Entry(window)
    # password_entry.insert(0, clicked)

    # Button definition
    copy_username_button = Button(window, text='Copy', command=copy_username)
    copy_password_button = Button(window, text='Copy', command=copy_password)
    # update_button = Button(window, text='Update', command=update_password)  # currently unavailable
    delete_button = Button(window, text='Delete', command=delete_click)

    # Configs

    # Draw elements to window
    username.grid(row=0, column=0)
    username_dropdown.grid(row=1, column=0)
    copy_username_button.grid(row=1, column=1)
    password.grid(row=2, column=0)
    password_entry.grid(row=3, column=0, padx=(20, 10))
    copy_password_button.grid(row=3, column=1, padx=10)
    # update_button.grid(row=4, column=0)  # currently unavailable
    delete_button.grid(row=4, column=1)
    website_label.grid(row=5, column=0, columnspan=2, sticky=S)

    # Tooltips
    ToolTip(copy_username_button, msg='Copies the username.', delay=0.5)
    ToolTip(copy_password_button, msg='Copies the password.', delay=0.5)
    # ToolTip(update_button, msg='Updates the password with whatever is written in the box.', delay=0.5)  # currently unavailable
    ToolTip(delete_button, msg='Deletes the entry from the database.', delay=0.5)
