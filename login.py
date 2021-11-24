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
    Sets up main window elements.
    :param root: master frame
    :return: None
    """

    # Label definitions
    header_label = Label(root, text="Matt's Password Manager")
    username_label = Label(root, text='Username:')
    password_label = Label(root, text='Password:')

    # Input definitions
    username_entry = Entry(root)
    password_entry = Entry(root)

    # Button definitions
    login_button = Button(root, text='Log In', command=lambda: check_credentials(username_entry.get(),
                                                                                 password_entry.get(), root))

    # Draw elements to root
    header_label.pack(pady=20)
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack(pady=20)
