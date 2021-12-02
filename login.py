from settings import *
import website_list
import hashlib


def create_new_window():
    """
    Opens the next window which is the website_list.
    :return: None
    """
    new_window = Toplevel()
    new_window.protocol("WM_DELETE_WINDOW", exit)  # exits the program if later window is closed
    new_window.geometry('250x250')
    website_list.initialize(new_window)


def check_credentials(username, password, parent):
    """
    Verifies credentials of user by checking encrypted username and password against a stored encrypted
    value located in 'credentials.txt'. This uses SHA256 1-way encryption. If successful, calls
    create_new_window and removes this window from view.
    :param username: string
    :param password: string
    :param parent: window calling this function (login screen)
    :return: None
    """
    username_byte = bytes(username, encoding='ASCII')
    password_byte = bytes(password, encoding='ASCII')
    encrypt_username = hashlib.sha256(username_byte).hexdigest()
    encrypt_password = hashlib.sha256(password_byte).hexdigest()
    credentials = []
    with open('credentials.txt', 'r') as infile:
        for line in infile:
            credentials.append(line.strip())
    if encrypt_username != credentials[0] or encrypt_password != credentials[1]:
        return False
    create_new_window()
    parent.withdraw()


def initialize(root):
    """
    Manager function that calls helper functions to define elements and then draw elements.
    :param root: master frame
    :return: None
    """

    elements = element_definitions(root)
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
    header = Label(window, text="Matt's Password Manager")
    username = Label(window, text='Username:')
    password = Label(window, text='Password:')
    return header, username, password


def entry_definitions(window):
    """
    Creates the entry fields on the screen.
    :param window: the screen where the entry fields will exist
    :return: tuple of the entry fields
    """
    username = Entry(window)
    password = Entry(window)
    return username, password


def button_definition(window, entries):
    """
    Creates the login button.
    :param window: the screen where the button will exist
    :param entries: tuple of entry fields that the button interacts with
    :return: login button element
    """
    username_entry, password_entry = entries
    login_button = Button(window, text='Log In', command=lambda: check_credentials(username_entry.get(),
                                                                                   password_entry.get(), window))
    return login_button


def draw_elements(elements):
    """
    Takes a tuple of element groups and draws them to the screen.
    :param elements: tuple containing group of elements. The group of elements may also be a tuple.
    :return:
    """

    # Unpack elements
    labels, entries, login_button = elements
    header_label, username_label, password_label = labels
    username_entry, password_entry = entries

    # Draw elements
    header_label.pack(pady=20)
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack(pady=20)


def create_tooltip(elements):
    """
    Creates tooltips for the different buttons on the screen.
    :param elements: package of elements that buttons are stored in
    :return: None
    """
    login_button = elements[2]
    ToolTip(login_button, msg='Logs into user account.', delay=0.5)
