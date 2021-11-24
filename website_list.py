from settings import *
import new_website
import view_edit_entry
import version

def create_new_window(window, website=None):
    """
    Creates a new window based on the button clicked.
    :param window: string, given by the button being clicked
    :param website: string, given by the website selected from the list of websites
    :return: None
    """
    if window == 'new':
        new_window = Toplevel()
        new_window.geometry('200x200')
        new_website.initialize(new_window)
    elif window == 'edit':
        if website == '':
            return
        new_window = Toplevel()
        new_window.geometry('250x150')
        view_edit_entry.initialize(new_window, website)
    elif window == 'version':
        new_window = Toplevel()
        new_window.geometry('200x200')
        version.initialize(new_window)

def fetch_data():
    """
    Queries the database for all URLs and groups them by URL.
    :return: List of URLs
    """
    c.execute("SELECT url FROM data GROUP BY url")
    results = c.fetchall()
    return [url[0] for url in results]

def initialize(root):
    """
    Sets up main window elements.
    :param root: master frame
    :return: None
    """
    # DB Connection
    results = fetch_data()

    # Frame definitions
    website_frame = Frame(root)

    # Label definitions
    header_label = Label(root, text="Matt's Password Manager")
    select_website_label = Label(website_frame, text='Select Website:')

    # Listbox definition
    website_list = Listbox(website_frame)
    for website in results:
        website_list.insert(END, website)

    # Scrollbar definition
    website_scroll = Scrollbar(website_frame, orient=VERTICAL)

    # Refresh query for button
    def query():
        c.execute("SELECT * FROM data")
        records = c.fetchall()
        website_list.delete(0, END)
        results = fetch_data()
        for website in results:
            website_list.insert(END, website)
        website_list.grid(row=1, column=0)

    # Button definitions
    view_edit_button = Button(root, text='View/Edit', command=lambda: create_new_window('edit', website_list.get(ANCHOR)))
    new_entry_button = Button(root, text='New Entry', command=lambda: create_new_window('new'))
    refresh_button = Button(root, text='Refresh List', command=query)
    version_button = Button(root, text='Version Info', command=lambda: create_new_window('version'))

    # Configs
    website_list.configure(yscrollcommand=website_scroll.set)  # listbox sends messages to scrollbar
    website_scroll.config(command=website_list.yview)  # scrollbar sends messages to listbox

    # Draw frames to window
    website_frame.grid(row=1, column=0, columnspan=2, rowspan=2, padx=(20, 0))
    # Draw elements to root
    header_label.grid(row=0, column=0, columnspan=3)
    view_edit_button.grid(row=1, column=3)
    new_entry_button.grid(row=2, column=3)
    # Draw elements to frame
    select_website_label.grid(row=0, column=0)
    website_list.grid(row=1, column=0)
    website_scroll.grid(row=0, column=1, rowspan=2, sticky=N+S)
    refresh_button.grid(row=3, column=0)
    version_button.grid(row=3, column=3)

    # Tooltips
    ToolTip(view_edit_button, msg='Opens a new window to allow for viewing the usernames associated with the '
                                    'website, and to copy/edit the passwords for those usernames.', delay=0.5)
    ToolTip(new_entry_button, msg='Opens a new window for new entries. Needs URL, username, and password.', delay=0.5)
    ToolTip(refresh_button, msg='Refreshes website list above.', delay=0.5)
    ToolTip(version_button, msg='Opens up recent version log.', delay=0.5)
