from tkinter import *
from tkinter import font

root = Tk()
root.geometry('500x500')


# Create Font_Chooser function
def font_chooser(e):
    our_font.config(family=my_listbox.get(my_listbox.curselection()))


# Designate our Font
our_font = font.Font(family="Arial", size=30)

# Add Frame
my_frame = Frame(root, width=480, height=275)
my_frame.pack(pady=10)
# Freeze frame in place
my_frame.grid_propagate(False)
my_frame.columnconfigure(0, weight=1)

# Add Text Box
my_text = Text(my_frame, font=our_font)
my_text.grid(row=0, column=0)
my_text.grid_rowconfigure(0, weight=1)
my_text.grid_columnconfigure(0, weight=1)

# Add listbox
my_listbox = Listbox(root, selectmode=SINGLE, width=80)
my_listbox.pack()

# Add Font Families to Listbox
for f in font.families():
    my_listbox.insert('end', f)

# Bind the listbox
my_listbox.bind('<ButtonRelease-1>', font_chooser)

root.mainloop()
