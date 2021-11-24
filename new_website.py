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
    RESULTS_FILENAME = 'crypto-service-results.json'

    # Locate file created
    path_to_results = os.path.join('.\\', RESULTS_FILENAME)

    # Load data from file into variables
    with open(path_to_results, 'r') as file:
        u_p_data = json.load(file)
        e_username = u_p_data['username']
        e_password = u_p_data['password']
        uid = u_p_data['uid']

    # Remove file after finishing with it
    os.remove(RESULTS_FILENAME)

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