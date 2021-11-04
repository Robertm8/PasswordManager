from settings import *

def save_click(window, website, username, password):
    """
    What happens when you click the save button.
    :return: None
    """


    # Open encryption microservice
    subprocess.run(['python', '-m', 'crypto-service', '-e', '-u' f'{username}', '-p', f'{password}', '-o', '.\\'])
    sleep(1)  # to give enough time for microservice to respond
    results_filename = None
    key_filename = None
    # Identify the files created
    for (dirpath, dirnames, filenames) in os.walk('.\\'):
        for file in filenames:
            if file[0:9] == 'encrypted':
                results_filename = file
            elif file[1:4] == 'key':
                key_filename = file

    # Locate those files created
    path_to_results = os.path.join('.\\', results_filename)
    path_to_key = os.path.join('.\\', key_filename)

    # Load data from those files into variables
    with open(path_to_results, 'r') as file:
        u_p_data = json.load(file)
        e_username = u_p_data['username']
        e_password = u_p_data['password']
    with open(path_to_key) as file:
        for line in file:
            k_data = line

    # Remove files after finishing with them
    os.remove(results_filename)
    os.remove(key_filename)

    # Save encrypted data to database
    c.execute("""INSERT INTO data (url, username, password, key)
    VALUES ('""" + website + """', '""" + e_username + """', '""" + e_password + """', '""" + k_data + """');""")
    conn.commit()
    messagebox.showinfo('Save', 'Username / Password Saved!', parent=window)
    window.destroy()
    print(u_p_data)
    print(e_username)
    print(e_password)
    print(k_data)


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