from settings import *


def save_click(window, website, username, password):
    """
    Saves website to database. Does this by calling an encryption microservice which will return encryption
    data which is stored in the database.
    :return: None
    """

    # Open encryption microservice
    subprocess.run(['python', '-m', 'crypto-service', '-e', '-u' f'{username}', '-p', f'{password}'])
    sleep(0.05)  # to give enough time for microservice to respond
    results_filename = 'crypto-service-results.json'

    # Locate file created
    path_to_results = os.path.join('.\\', results_filename)

    # Load data from file into variables
    with open(path_to_results, 'r') as file:
        u_p_data = json.load(file)
        e_username = u_p_data['username']
        e_password = u_p_data['password']
        uid = u_p_data['uid']

    # Remove file after finishing with it
    os.remove(results_filename)

    # Save encrypted data to database
    c.execute("""INSERT INTO data (url, username, password, uid)
    VALUES ('""" + website + """', '""" + e_username + """', '""" + e_password + """', '""" + uid + """');""")
    conn.commit()
    messagebox.showinfo('Save', 'Username / Password Saved!', parent=window)
    window.destroy()


def initialize(window):
    """
    Sets up main window elements.
    :param window: the window popup
    :return: None
    """

    elements = element_definitions(window)
    draw_elements(elements)
    create_tooltip(elements)


def element_definitions(window):
    """
    Manager for element definitions.
    :param window: the screen where the elements will exist
    :return: tuple of element groups
    """
    labels = label_definitions(window)
    entries = entry_definitions(window)
    button = button_definition(window, entries)

    return labels, entries, button


def label_definitions(window):
    """
    Creates the text on the screen.
    :param window: the screen where the text will exist
    :return: tuple of text labels
    """
    website = Label(window, text='Website:')
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')

    return website, username, password


def entry_definitions(window):
    """
    Creates the entry fields on the screen.
    :param window: the screen where the entry fields will exist
    :return: tuple of the entry fields
    """
    website = Entry(window)
    username = Entry(window)
    password = Entry(window)

    return website, username, password


def button_definition(window, entries):
    """
    Creates the save button.
    :param window: the screen where the button will exist
    :param entries: tuple of entry fields that the button interacts with
    :return: save button element
    """
    website, username, password = entries
    save_button = Button(window, text='Save', command=lambda: save_click(window, website.get(), username.get(),
                                                                         password.get()))

    return save_button


def draw_elements(elements):
    """
    Takes a tuple of element groups and draws them to the screen.
    :param elements: tuple containing group of elements. The group of elements may also be a tuple.
    :return:
    """

    # Unpack elements
    labels, entries, save_button = elements
    website_label, username_label, password_label = labels
    website_entry, username_entry, password_entry = entries

    # Draw elements
    website_label.pack()
    website_entry.pack()
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    save_button.pack(pady=15)


def create_tooltip(elements):
    """
    Creates tooltips for the different buttons on the screen.
    :param elements: package of elements that buttons are stored in
    :return: None
    """
    save_button = elements[2]
    ToolTip(save_button, msg='Saves the entry into the database.', delay=0.5)
