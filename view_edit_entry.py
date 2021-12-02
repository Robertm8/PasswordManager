from settings import *


def fetch_data(website):
    """
    Runs query to database and decrypts the data.
    :param website: website that was selected
    :return: decrypted results
    """
    c.execute("SELECT url, username, password, uid FROM data where url = '" + website + "'")
    results = c.fetchall()
    return translate_results(results)


def translate_results(results):
    """
    Function for decrypting usernames / passwords for a website.
    :param results: encrypted list with a tuple of url / username / password for each username
    :return: decrypted list with a tuple of url / username / password for each username
    """

    decrypted_results = []

    # Open encryption microservice
    for username_pass in results:
        url = username_pass[0]
        subprocess.run(['python', '-m', 'crypto-service', '-d', '-uid', username_pass[3],
                        '-u', username_pass[1], '-p', username_pass[2]])
        sleep(0.05)  # to give enough time for microservice to respond
        results_filename = 'crypto-service-results.json'

        # Locate file created
        path_to_results = os.path.join('.\\', results_filename)

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


def update_password_field(clicked, decrypted_results, password_entry):
    """
    Updates the password field upon selecting a username. Returns first match it finds.
    :param clicked: tkinter string variable
    :param decrypted_results: list of usernames and passwords
    :param password_entry: the entry element where password is located
    :return: None
    """
    click = clicked.get()
    for element in decrypted_results:
        if element[1] == click:
            password_entry.delete(0, END)
            password_entry.insert(0, element[2])
            break


def copy_username(window, clicked):
    """
    Copies username to the clipboard.
    :param window: window where button that calls this function resides
    :param clicked: tkinter string variable
    :return: None
    """
    selected = clicked.get()
    window.clipboard_clear()
    window.clipboard_append(selected)


def copy_password(window, password_entry):
    """
    Copies password to the clipboard.
    :param window: window where button that calls this function resides
    :param password_entry: password text field element
    :return: None
    """
    selected = password_entry.get()
    window.clipboard_clear()
    window.clipboard_append(selected)


def delete_click(window, decrypted_results, clicked):
    """
    Deletes the username/password combo from the database.
    :param window: window where button that calls this function resides
    :param decrypted_results: list of usernames and passwords
    :param clicked: tkinter string variable
    :return:
    """
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


def initialize(window, website):
    """
    Manager function that calls helper functions to define elements and then draw elements.
    :param window: the window popup
    :param website: the website being viewed
    :return: None
    """
    elements = element_definitions(window, website)
    draw_elements(elements)
    create_tooltips(elements)


def element_definitions(window, website):
    """
    Manager for element definitions.
    :param window: the screen where the elements will exist
    :param website: the website being viewed
    :return: tuple of element groups
    """
    clicked = StringVar()
    decrypted_results = fetch_data(website)  # db query

    labels = label_definitions(window, website)
    entry = entry_definition(window)
    dropdown = dropdown_definition(window, entry, clicked, decrypted_results)
    buttons = button_definitions(window, clicked, entry, decrypted_results)

    return labels, dropdown, entry, buttons


def label_definitions(window, website):
    """
    Creates the text on the screen.
    :param window: the screen where the text will exist
    :param website: the website that was selected
    :return: tuple of text labels
    """
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')
    website_label = Label(window, text=website)

    return username, password, website_label


def dropdown_definition(window, entry, clicked, decrypted_results):
    """
    Creates dropdown menu populated with usernames.
    :param window: the screen where the dropdown exists
    :param entry: the password field
    :param clicked: tkinter string variable
    :param decrypted_results: unencrypted data from database
    :return:
    """
    usernames = [user[1] for user in decrypted_results]
    clicked.set(usernames[0])  # initial selection
    update_password_field(clicked, decrypted_results, entry)  # password call for the initial selection

    username_dropdown = OptionMenu(window, clicked, *usernames,
                                   command=lambda _: update_password_field(clicked, decrypted_results, entry))

    return username_dropdown


def entry_definition(window):
    """
    Entry field where password will be displayed.
    :param window: the screen where entry box is located
    :return: entry element
    """
    entry = Entry(window)
    return entry


def button_definitions(window, clicked, entry, decrypted_results):
    """
    Definition of various buttons located on the screen. Buttons are both copy buttons and delete button.
    :param window: screen where buttons are located
    :param clicked: tkinter string variable
    :param entry: password field on screen
    :param decrypted_results: unencrypted data from database
    :return: tuple of button elements
    """
    copy_username_button = Button(window, text='Copy', command=lambda: copy_username(window, clicked))
    copy_password_button = Button(window, text='Copy', command=lambda: copy_password(window, entry))
    delete_button = Button(window, text='Delete', command=lambda: delete_click(window, decrypted_results, clicked))

    return copy_username_button, copy_password_button, delete_button


def draw_elements(elements):
    """
    Takes a tuple of element groups and draws them to the screen.
    :param elements: tuple containing group of elements. The group of elements may also be a tuple.
    :return: None
    """
    # Unpack elements
    labels, dropdown, entry, buttons = elements
    username, password, website = labels
    copy_username_button, copy_password_button, delete_button = buttons

    # Draw elements
    username.grid(row=0, column=0)
    dropdown.grid(row=1, column=0)
    copy_username_button.grid(row=1, column=1)
    password.grid(row=2, column=0)
    entry.grid(row=3, column=0, padx=(20, 10))
    copy_password_button.grid(row=3, column=1, padx=10)
    delete_button.grid(row=4, column=1)
    website.grid(row=5, column=0, columnspan=2, sticky=S)


def create_tooltips(elements):
    """
    Creates tooltips for the different buttons on the screen.
    :param elements: package of elements that buttons are stored in
    :return: None
    """
    # Unpack buttons
    buttons = elements[3]
    copy_username_button, copy_password_button, delete_button = buttons

    # Create tooltips
    ToolTip(copy_username_button, msg='Copies the username.', delay=0.5)
    ToolTip(copy_password_button, msg='Copies the password.', delay=0.5)
    ToolTip(delete_button, msg='Deletes the entry from the database.', delay=0.5)
