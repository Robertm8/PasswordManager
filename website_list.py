from settings import *
import new_website
import view_edit_entry

def create_new_window(window, website=None):
    if window == 'new':
        print(website)
        new_window = Toplevel()
        new_window.geometry('200x200')
        new_website.initialize(new_window)
    elif window == 'edit':
        if website == '':
            return
        new_window = Toplevel()
        new_window.geometry('200x200')
        view_edit_entry.initialize(new_window, website)

def initialize(root):
    """
    Sets up main window elements.
    :param root: master frame
    :return: None
    """
    # DB Connection
    c.execute("SELECT url FROM data GROUP BY url")
    results = c.fetchall()
    results = [url[0] for url in results]
    print(results)

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

    # Button definitions
    view_edit_button = Button(root, text='View/Edit', command=lambda: create_new_window('edit', website_list.get(ANCHOR)))
    new_entry_button = Button(root, text='New Entry', command=lambda: create_new_window('new'))

    # Configs
    website_list.configure(yscrollcommand=website_scroll.set)  # listbox sends messages to scrollbar
    website_scroll.config(command=website_list.yview)  # scrollbar sends messages to listbox

    # Draw frames to window
    website_frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    # Draw elements to root
    header_label.grid(row=0, column=0, columnspan=3)
    view_edit_button.grid(row=1, column=3)
    new_entry_button.grid(row=2, column=3)
    # Draw elements to frame
    select_website_label.grid(row=0, column=0)
    website_list.grid(row=1, column=0)
    website_scroll.grid(row=0, column=1, rowspan=2, sticky=N+S)

    # Temporary button
    def query():
        c.execute("SELECT * FROM data")
        records = c.fetchall()
        print(records)

    b1 = Button(root, text='Pull Data', command=query)
    b1.grid(row=3, column=0)
