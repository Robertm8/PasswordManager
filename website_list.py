from settings import *
import new_website

def create_new_window(window):
    if window == 'new':
        new_window = Toplevel()
        new_window.geometry('200x200')
        new_website.initialize(new_window)


def initialize(root):
    """
    Sets up main window elements.
    :param root: master frame
    :return: None
    """
    # Frame definitions
    website_frame = Frame(root)

    # Label definitions
    header_label = Label(root, text="Matt's Password Manager")
    select_website_label = Label(website_frame, text='Select Website:')

    # Listbox definition
    website_list = Listbox(website_frame)

    # Scrollbar definition
    website_scroll = Scrollbar(website_frame, orient=VERTICAL)

    # Button definitions
    view_edit_button = Button(root, text='View/Edit', command=lambda: create_new_window('edit'))
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

    # Fill with sample data
    websites = ['www.gmail.com', 'www.youtube.com', 'www.facebook.com', 'www.instagram.com', 'www.reddit.com',
                'www.github.com', 'www.oregonstate.edu', 'www.espn.com', 'www.amazon.com', 'www.pintrest.com',
                'www.pastebin.com', 'www.zoom.us', 'www.yahoo.com', 'www.bing.com']
    for website in websites:
        website_list.insert(END, website)
