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


def query(listbox):
    """
    Deletes data from listbox and populates it with fresh data.
    :param listbox: listbox element
    :return: None
    """
    c.execute("SELECT * FROM data")
    listbox.delete(0, END)
    populate_listbox(listbox)
    listbox.grid(row=1, column=0)


def initialize(window):
    """
    Manager function that calls helper functions to define elements and then draw elements.
    :param window: the current screen
    :return: None
    """
    elements = element_definitions(window)
    draw_elements(elements)
    create_tooltips(elements)


def element_definitions(window):
    """
    Manager for element definitions.
    :param window: the screen where the elements will exist
    :return: tuple of element groups
    """
    frame = Frame(window)
    list_and_scroll = listbox_definitions(frame)
    labels = label_definitions(window, frame)
    buttons = button_definitions(window, list_and_scroll[0])  # list_and_scroll[0] = listbox

    return frame, labels, buttons, list_and_scroll


def listbox_definitions(frame):
    """
    Listbox and scrollbar definitions. Populates the listbox with database data and configures the scrollbar
    to interact with the listbox.
    :param frame: the part of the window where the listbox will be located
    :return: tuple of listbox and scrollbar elements
    """
    listbox = Listbox(frame)
    populate_listbox(listbox)
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Configs for listbox and scrollbar
    listbox.configure(yscrollcommand=scrollbar.set)  # listbox sends messages to scrollbar
    scrollbar.config(command=listbox.yview)  # scrollbar sends messages to listbox

    return listbox, scrollbar


def populate_listbox(listbox):
    """
    Calls fetch_data which queries the database and then uses that data to fill in the listbox.
    :param listbox: listbox element
    :return: None
    """
    results = fetch_data()
    for website in results:
        listbox.insert(END, website)


def label_definitions(window, frame):
    """
    Creates the text on the screen.
    :param window: the screen where the text will exist
    :param frame: the frame where the text will exist
    :return: tuple of text labels
    """
    header = Label(window, text="Matt's Password Manager")
    select_website = Label(frame, text='Select Website:')
    return header, select_website


def button_definitions(window, listbox):
    """
    Creates the button definitions.
    :param window: the screen where the buttons will exist
    :param listbox: the listbox where the buttons pull data from
    :return: tuple of button elements
    """
    view_edit = Button(window, text='View/Edit', command=lambda: create_new_window('edit', listbox.get(ANCHOR)))
    new_entry = Button(window, text='New Entry', command=lambda: create_new_window('new'))
    refresh = Button(window, text='Refresh List', command=lambda: query(listbox))
    cur_version = Button(window, text='Version Info', command=lambda: create_new_window('version'))
    return view_edit, new_entry, refresh, cur_version


def draw_elements(elements):
    """
    Takes a tuple of element groups and draws them to the screen.
    :param elements: tuple containing group of elements. The group of elements may also be a tuple.
    :return:
    """
    # Unpack elements
    frame, labels, buttons, listbox = elements
    header_label, select_website_label = labels
    listbox, scrollbar = listbox
    view_edit, new_entry, refresh, cur_version = buttons

    # Frame
    frame.grid(row=1, column=0, columnspan=2, rowspan=2, padx=(20, 0))

    # Labels
    header_label.grid(row=0, column=0, columnspan=3)
    select_website_label.grid(row=0, column=0)

    # Listbox
    listbox.grid(row=1, column=0)
    scrollbar.grid(row=0, column=1, rowspan=2, sticky=N + S)

    # Buttons
    view_edit.grid(row=1, column=3)
    new_entry.grid(row=2, column=3)
    refresh.grid(row=3, column=0)
    cur_version.grid(row=3, column=3)


def create_tooltips(elements):
    """
    Creates tooltips for the different buttons on the screen.
    :param elements: package of elements that buttons are stored in
    :return: None
    """
    # Unpack buttons
    buttons = elements[2]
    view_edit, new_entry, refresh, cur_version = buttons

    # Create tooltips
    ToolTip(view_edit, msg='Opens a new window to allow for viewing the usernames associated with the '
            'website, and to copy/edit the passwords for those usernames.', delay=0.5)
    ToolTip(new_entry, msg='Opens a new window for new entries. Needs URL, username, and password.', delay=0.5)
    ToolTip(refresh, msg='Refreshes website list above.', delay=0.5)
    ToolTip(cur_version, msg='Opens up recent version log.', delay=0.5)
