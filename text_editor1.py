
from tkinter import *
# import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import os
from PIL import Image, ImageTk


root = Tk()
root.title("TEXT EDITOR")

root.geometry("790x700")
root.minsize(790,700)
root.maxsize(790,700)
# root.minsize(665,666)
root.wm_iconbitmap('mynewicon.ico')


def cut():
    context_text.event_generate("<<Cut>>")
def copy():
    context_text.event_generate("<<copy>>")
def paste():
    context_text.event_generate("<<paste>>")
def undo(event=None):
    context_text.edit_undo()  # Use built-in edit_undo method to undo changes
    return 'break'
def redo(event=None):
    context_text.event_generate("<<Redo>>")
    return 'break'
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        context_text.delete(1.0, tkinter.END)
        with open(file_name) as _file:
            context_text.insert(1.0, _file.read())
        on_context_changed()
def write_to_file(file_name):
    try:
     content = context_text.get(1.0, 'end')
     with open(file_name, 'w') as the_file:
        the_file.write(content)
    except IOError:
        pass
# pass for now but we show some warning - we do this in next section
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
    ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
    root.title('{} - {}'.format(os.path.basename(file_name),PROGRAM_NAME))
    return "break"
def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    context_text.delete(1.0,END)
def select_all(event=None):
    context_text.tag_add('sel','1.0','end')
    return "break"
# find text feature


def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    ignore_case_checkbox = Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value)
    ignore_case_checkbox.grid(row=1, column=1, sticky='e', padx=2, pady=2)
    find_button=Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(search_entry_widget.get(), ignore_case_value.get(),
                                          context_text, search_toplevel,
                                          search_entry_widget)).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
    # search_entry_widget.bind('<Return>', lambda event: find_button.invoke())
    def on_enter(event, button):
        button.invoke()

    search_entry_widget.bind('<Return>', lambda event: on_enter(event, find_button))
    def close_search_window():
        context_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"

def search_output(search_string, ignore_case, content_text, search_toplevel, search_entry_widget):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if search_string:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(search_string, start_pos, nocase=ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(search_string))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', foreground='red', background='yellow')
    search_entry_widget.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))

def on_context_changed():
    # Your implementation here
    pass  # Placeholder for the implementation

def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME,"\nTkinter GUI Application\n Development Blueprints"))
def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo("Help", "Help Book: \nTkinter GUI Application\n Development Blueprints", icon='question')
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()
def on_content_changed(event=None):
    update_line_numbers()

Menubar = Menu(root)
root.config(menu=Menubar)

#file menu
file_menu = Menu(Menubar, tearoff=0)
file_menu.add_command(label="New     ", font="cosmicsams 10 italic",accelerator='Ctrl+N',command=new_file)
file_menu.add_command(label="Open", font="cosmicsams 10 italic",accelerator='Ctrl+O',command=open_file)
file_menu.add_command(label="Save", font="cosmicsams 10 italic",accelerator='Ctrl + S',command=save)
file_menu.add_command(label="Save as" , font="cosmicsams 10 italic",accelerator='Shift+Ctrl+S',command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", font="cosmicsams 10 italic", command=exit_editor)



#editmenu

edit_menu=Menu(Menubar,tearoff=0)
edit_menu.add_command(label="Undo", font="cosmicsams 10 italic",accelerator='Ctrl+Z')
edit_menu.add_command(label="Redo", font="cosmicsams 10 italic",accelerator='Ctrl+Y')

edit_menu.add_separator()

edit_menu.add_command(label="Cut", font="cosmicsams 10 italic",accelerator='Ctrl+X',compound='left',command=cut)
edit_menu.add_command(label="Copy", font="cosmicsams 10 italic",accelerator='Ctrl+C',command=copy)
edit_menu.add_command(label="Paste", font="cosmicsams 10 italic",accelerator='Ctrl+V',command=paste)

edit_menu.add_separator()

# edit_menu.add_command(label="Undo", font="cosmicsams 10 italic",accelerator='Ctrl+F')

# edit_menu.add_separator()

# edit_menu.add_command(label="Undo", font="cosmicsams 10 italic",accelerator='Ctrl+A')





#view menu
show_line_no=IntVar()
show_cursor_location=IntVar()
Highlight_current_line=IntVar()

themes_menu=StringVar()
view_menu=Menu(Menubar,tearoff=0)
themes_menu=Menu(view_menu,tearoff=0)

theme_name=StringVar()
view_menu.add_checkbutton(label="Show line number ",variable=show_line_no)
view_menu.add_checkbutton(label="Show Cursor Location at Bottom ",variable=show_cursor_location)
view_menu.add_checkbutton(label="Highlight Current Line ",variable=Highlight_current_line)
view_menu.add_cascade(label="Themes",menu=themes_menu)
themes_menu.add_radiobutton(label="Aquamarine",variable=theme_name)
themes_menu.add_radiobutton(label="Bold Beige",variable=theme_name)
themes_menu.add_radiobutton(label="Cobalt Blue",variable=theme_name)
themes_menu.add_radiobutton(label="Default",variable=theme_name)
themes_menu.add_radiobutton(label="Greygarious",variable=theme_name)
themes_menu.add_radiobutton(label="Olive Green",variable=theme_name)


#About menu
About_menu=Menu(Menubar,tearoff=0)
About_menu.add_command(label="About", font="cosmicsams 10 italic",command=display_about_messagebox)
About_menu.add_command(label="Help", font="cosmicsams 10 italic",command=display_help_messagebox)



#shortcut frame/ bar
shortcut_bar = Frame(root, height=25, background='silver',borderwidth=5,relief=SUNKEN)
shortcut_bar.pack(expand='no', fill='x',side=TOP)

#line number bar 
line_number_bar = Text(root, width=4, padx=3, takefocus=0, border=0, background='grey', state='disabled', wrap='none',borderwidth=5,relief=SUNKEN)
line_number_bar.pack(side='left', fill='y')

# MAIN MENU

Menubar.add_cascade(label='FILE', menu=file_menu)
Menubar.add_cascade(label='EDIT',menu=edit_menu)# Add corresponding EDIT menu here
Menubar.add_cascade(label='VIEW',menu=view_menu)  # Add corresponding VIEW menu here
Menubar.add_cascade(label='ABOUT',menu=About_menu)  # Add corresponding ABOUT menu here

# TEXT BOX


context_text=Text(root,wrap='word',undo=1,font="roboto 12 bold")
context_text.pack(expand='yes',fill='both')

#binding edit menu keys

context_text.bind('<Control-z>', undo)
context_text.bind('<Control-Z>', undo)

context_text.bind('<Control-y>',redo)#handling Ctrl +small-case y
context_text.bind('<Control-Y>',redo)#handling Ctrl +upper-case y

context_text.bind('<Control-A>',select_all)
context_text.bind('<Control-a>',select_all)

#binding find menu keys
context_text.bind('<Control-N>', new_file)
context_text.bind('<Control-n>', new_file)
context_text.bind('<Control-O>', open_file)
context_text.bind('<Control-o>', open_file)
context_text.bind('<Control-S>', save)
context_text.bind('<Control-s>',save)

#SCROLL BAR
scroll_bar=Scrollbar(context_text)
context_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=context_text.yview)
scroll_bar.pack(side='right',fill='y')


#select all feature


edit_menu.add_command(label="Select All",underline=7,accelerator='Ctrl+A',command=select_all)




root.bind('<Control-f>', find_text)




context_text.bind('<Control-F>',find_text)
context_text.bind('<Control-f>',find_text)




#file dialogue
file_object=tkinter.filedialog



file_name=None

PROGRAM_NAME = "YourProgramName"  # Define PROGRAM_NAME here

# file_object=tkinter.filedialog.askopenfile(mode='r')
# my_file_name=tkinter.filedialog.askopenfilename()

#about and help buttons of the ABOUT MENU
import tkinter.messagebox as tmb
def display_messageboxes():
    tmb.showinfo(title="Show Info", message="This is FYI")
    tmb.showwarning(title="Show Warning", message="Don't be silly")
    tmb.showerror(title="Show Error", message="It leaked")
    tmb.askquestion(title="Ask Question", message="Can you read this?")
    tmb.askokcancel(title="Ask OK Cancel", message="Say Ok or Cancel?")
    tmb.askyesno(title="Ask Yes-No", message="Say yes or no?")
    tmb.askyesnocancel(title="Yes-No-Cancel", message="Say yes no cancel")
    tmb.askretrycancel(title="Ask Retry Cancel", message="Retry or what?")

root.protocol('WM_DELETE_WINDOW', exit_editor)
#bindings fo rthe keyboard shortcut to display help
context_text.bind('<KeyPress-F1>', display_help_messagebox)



# Define icons
icons = {
    "open": PhotoImage(file="open_file.png"),
    "save": PhotoImage(file="save.png"),
    "cut": PhotoImage(file="cut.png"),
    "copy": PhotoImage(file="copy.png"),
    "paste": PhotoImage(file="paste.png"),
    "newfile":PhotoImage(file="newfile.png"),
    "redo":PhotoImage(file="redo.png"),
    "undo":PhotoImage(file="undo.png"),
    "find_text":PhotoImage(file="find_text.png"),
}

# Create buttons with icons and text
open_button = ttk.Button(shortcut_bar, image=icons["open"], text="Open", compound="top", command=open_file)
open_button.pack(side=LEFT, padx=5, pady=5,fill=X)

save_button = ttk.Button(shortcut_bar, image=icons["save"], text="Save", compound="top", command=save)
save_button.pack(side=LEFT, padx=5, pady=5,fill=X)

cut_button = ttk.Button(shortcut_bar, image=icons["cut"], text="Cut", compound="top", command=cut)
cut_button.pack(side=LEFT, padx=5, pady=5,fill=X)

copy_button = ttk.Button(shortcut_bar, image=icons["copy"], text="Copy", compound="top", command=copy)
copy_button.pack(side=LEFT, padx=5, pady=5,fill=X)

paste_button = ttk.Button(shortcut_bar, image=icons["paste"], text="Paste", compound="top", command=paste)
paste_button.pack(side=LEFT, padx=5, pady=5,fill=X)

new_file_button = ttk.Button(shortcut_bar, image=icons["newfile"], text="New File", compound="top", command=new_file)
new_file_button.pack(side=LEFT, padx=5, pady=5,fill=X)

undo_button = ttk.Button(shortcut_bar, image=icons["undo"], text="Undo", compound="top", command=undo)
undo_button.pack(side=LEFT, padx=5, pady=5,fill=X)

redo_button = ttk.Button(shortcut_bar, image=icons["redo"], text="redo", compound="top", command=redo)
redo_button.pack(side=LEFT, padx=5, pady=5,fill=X)

find_text_button = ttk.Button(shortcut_bar, image=icons["find_text"], text="find_text", compound="top", command=find_text)
find_text_button.pack(side=LEFT, padx=5, pady=5,fill=X)

# # Create a text area
# text_area = Text(root)
# text_area.pack(fill=BOTH, expand=True)
# Center align the buttons
# for widget in shortcut_bar.winfo_children():
#     widget.pack_configure(anchor="center")
context_text.bind('<Any-KeyPress>', on_content_changed)
def get_line_numbers():
    output = ''
    if show_line_no.get():
        row, col = context_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i)+ '\n'
    return output
def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('2.0', line_numbers)
    line_number_bar.config(state='disabled')
    # Define a font for line numbers
    line_number_font = ('Courier', 12)  # Adjust the size as needed
    
     # Adjust width of line number bar to match the width of the widest line number
    max_line_number_width = max(len(str(i)) for i in range(1, int(context_text.index("end").split('.')[0])))
    line_number_bar_width = max_line_number_width+2
      # Add extra padding
    line_number_bar.config(width=line_number_bar_width)
update_line_numbers()
# to_highlight_line = BooleanVar()
# view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1, offvalue=0)

color_schemes = {
'Default': '#000000.#FFFFFF',
'Greygarious':'#83406A.#D1D4D1',
'Aquamarine': '#5B8340.#D1E7E0',
'Bold Beige': '#4B4620.#FFF0E1',
'Cobalt Blue':'#ffffBB.#3333aa',
'Olive Green': '#D1E7E0.#5B8340',
'Night Mode': '#FFFFFF.#000000',
}
theme_choice = StringVar(root)

def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    if fg_bg_colors:
        foreground_color, background_color = fg_bg_colors.split('.')
        context_text.config(background=background_color, fg=foreground_color)
    else:
        tkinter.messagebox.showerror("Error", "Theme not found")

# Define theme names for radiobuttons
for theme_name in color_schemes:
    themes_menu.add_radiobutton(label=theme_name, variable=theme_choice, command=change_theme)

root.mainloop()


