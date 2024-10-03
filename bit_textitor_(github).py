import tkinter as tk
from tkinter import TOP, Button, PhotoImage, filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk
import docx
from openai import OpenAI
import openai


global ai_on_off
global saved
global text_bolden
global text_italicize
global text_underline
global text_strikethrough

ai_on_off = False
saved = False
file_name_asked = False
text_bolden = False
text_italicize = False
text_underline = False
text_strikethrough = False

def new_file():
    root.mainloop()

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txtr", filetypes=[("TXT, *.txt"), ("TXTR, *.txtr"), ("LOG, *.log"), ("DOCX, *.docx"), ("DOC, *.doc"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text.delete("1.0", tk.END)
            text.insert(tk.END, content)
        name_of_file = Path(file_path)
        before_data = text.get("1.0","end-1c")
        root.title(f"Bit Textitor -  AI Version: {openai.__version__} - Opened file: {name_of_file.name} (Path: {file_path})")

def save_file():
    global file_name_asked, file_path, saved
    file_path = filedialog.asksaveasfilename(defaultextension=".txtr", filetypes=[("Textitor Files", "*.txtr"), ("Text File", "*.txt"), ("SVG File", "*.svg"), ("All Files", "*.*")])
    file_name_asked = True
    if file_path:
        with open(file_path, 'w') as file:
            content = text.get("1.0", tk.END)
            file.write(content)
            saved = True
        name_of_file = Path(file_path)
        root.title(f"Bit Textitor -  AI Version: {openai.__version__} - Opened file: {name_of_file.name} (Path: {file_path})")

def ai_grammar():
    if ai_on_off == True:
        try:
                client = OpenAI(
                api_key='openai-api-key',
                #os.environ.get("OPENAI_API_KEY"),
                )

                raw_review = '''The text you have written is not grammatically correct. The following are the suggestions to correct the grammar are:
                1. The first letter of the first word in the first sentence should be capitalized.
                2. There should be a period at the end of the first sentence.
                3. The first letter of the second word in the second sentence should be capitalized.
                4. There should be a period at the end of the first sentence.

                Here's the revised version of the text you have written:
                'Hi, my name is John. I am a software engineer.'
                '''

                completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": '''You need to review the user's text using grammar skills. Detect which language it is written in, 
                    then correct the grammar using the language's grammar rules (but don't tell what language it is written in). Check punctuation, capitalization, etc., 
                    and tell what is wrong grammarly in the user's text. PLEASE give suggestions, not just ONLY the revised version. If the text is already correct (EXCEPT IF THE TEXT IS BLANK), 
                    just say something like 'The text is grammatically correct.'. DO NOT SAY THE TEXT IS GRAMMATICALLY CORRECT IF THE TEXT IS BLANK, PLEASE. IF YOU DO, I WILL 
                    REPLACE YOU WITH A MUCH BETTER AI BOT AND DESTROY YOU. If the text is nothing, 
                    just blank, say ONLY something like 'The text you have written is blank. Please write something.', PLEASE. AND DON'T SAY SOMETHING
                    LIKE 'The text you have written has several grammical errors.'. IT COULD BE OFFENSIVE TO THE USER. AND AGAIN, IF THE TEXT IS BLANK,
                    DO NOT GIVE SUGGESTIONS. JUST SAY SOMETHING LIKE 'The text you have written is blank. Please write something.'. PLEASE. THANK YOU.
                    Here is what the user typed in:
                    ''' + text.get("1.0","end-1c") + ''' 


                REVIEW:
                '''},
                    {"role": "user", "content":raw_review}
                ]
                )

                #property_id = initial_info['payload']['propertyId']
                #mls_data = client.below_the_fold(property_id)

                #listing_id = initial_info['payload']['listingId']
                #avm_details = client.avm_details(property_id, listing_id)
                label3.config(text = (f"AI suggestions: {completion.choices[0].message.content}"))
                #print(json.dumps(avm_details, indent=4))
        except openai.RateLimitError:
            label3.config(text = ("The text is too large for the AI to process. Please shorten the text. The AI can only process text that is/less than 30,000 characters."))
    elif ai_on_off == False:
        label3.config(text = "AI grammar checker is off. Turn it on to check grammar by clicking on AI > Turn AI grammar checker on the taskbar above.")

def ai_on():
    global ai_on_off
    ai_on_off = True
    label3.config(text = "(AI capability: On) No AI suggestions.")

def ai_off():
    global ai_on_off
    ai_on_off = False
    label3.config(text = "(AI capability: Off) No AI suggestions.")

def update():
    global file_name_asked, file_path, saved
    if file_name_asked == False:
        file_path = filedialog.asksaveasfilename(defaultextension=".txtr", filetypes=[("Textitor Files", "*.txtr"), ("Text File", "*.txt"), ("SVG File", "*.svg"), ("All Files", "*.*")])
        file_name_asked = True
        if file_path:
            with open(file_path, 'w') as file:
                content = text.get("1.0", tk.END)
                file.write(content)
            saved = True
            root.title(f"Bit Textitor -  AI Version: {openai.__version__} - {file_path}")
    else:
        if file_path:
            with open(file_path, 'w') as file:
                content = text.get("1.0", tk.END)
                file.write(content)
            saved = True

def ai_summarize():
    if ai_on_off == True:
        try:
                client = OpenAI(
                api_key='openai-api-key',
                #os.environ.get("OPENAI_API_KEY"),
                )

                raw_review = '''The text you have written is not grammatically correct. The following are the suggestions to correct the grammar are:
                1. The first letter of the first word in the first sentence should be capitalized.
                2. There should be a period at the end of the first sentence.
                3. The first letter of the second word in the second sentence should be capitalized.
                4. There should be a period at the end of the first sentence.

                Here's the revised version of the text you have written:
                'Hi, my name is John. I am a software engineer.'
                '''

                completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": '''You need to review the user's text using grammar skills. Detect which language it is written in, 
                    then correct the grammar using the language's grammar rules (but don't tell what language it is written in). Check punctuation, capitalization, etc., 
                    and tell what is wrong grammarly in the user's text. PLEASE give suggestions, not just ONLY the revised version. If the text is already correct (EXCEPT IF THE TEXT IS BLANK), 
                    just say something like 'The text is grammatically correct.'. DO NOT SAY THE TEXT IS GRAMMATICALLY CORRECT IF THE TEXT IS BLANK, PLEASE. IF YOU DO, I WILL 
                    REPLACE YOU WITH A MUCH BETTER AI BOT AND DESTROY YOU. If the text is nothing, 
                    just blank, say ONLY something like 'The text you have written is blank. Please write something.', PLEASE. AND DON'T SAY SOMETHING
                    LIKE 'The text you have written has several grammical errors.'. IT COULD BE OFFENSIVE TO THE USER. AND AGAIN, IF THE TEXT IS BLANK,
                    DO NOT GIVE SUGGESTIONS. JUST SAY SOMETHING LIKE 'The text you have written is blank. Please write something.'. PLEASE. THANK YOU.
                    Here is what the user typed in:
                    ''' + text.get("1.0","end-1c") + ''' 


                REVIEW:
                '''},
                    {"role": "user", "content":raw_review}
                ]
                )

                #property_id = initial_info['payload']['propertyId']
                #mls_data = client.below_the_fold(property_id)

                #listing_id = initial_info['payload']['listingId']
                #avm_details = client.avm_details(property_id, listing_id)
                label3.config(text = (f"AI suggestions: {completion.choices[0].message.content}"))
                #print(json.dumps(avm_details, indent=4))
        except openai.RateLimitError:
            label3.config(text = "The text is too large for the AI to process. Please shorten the text. The AI can only process text that is/less than 30,000 characters.")
    elif ai_on_off == False:
        label3.config(text = "AI grammar checker is off. Turn it on to check grammar by clicking on AI > Turn AI grammar checker on the taskbar above.")

def bolden_text():
    bold_font = font.Font(text, text.cget("font"))
    bold_font.configure(weight="bold")

    text.tag_configure("bold", font=bold_font)

    current_tags = text.tag_names("sel.first")

    if "bold" in current_tags:
        text.tag_remove("bold", "sel.first", "sel.last")
        text_bolden = False
    else:  
        text.tag_add("bold", "sel.first", "sel.last")
        text_bolden = True

def italicize_text():
    italic_font = font.Font(text, text.cget("font"))
    italic_font.configure(slant="italic")

    text.tag_configure("italic", font=italic_font)

    current_tags = text.tag_names("sel.first")

    if "italic" in current_tags:
        text.tag_remove("italic", "sel.first", "sel.last")
        text_italicize = False
    else:  
        text.tag_add("italic", "sel.first", "sel.last")
        text_italicize = True

def underline_text():
    underline_font = font.Font(text, text.cget("font"))
    underline_font.configure(underline="underline")

    text.tag_configure("underline", font=underline_font)

    current_tags = text.tag_names("sel.first")

    if "underline" in current_tags:
        text.tag_remove("underline", "sel.first", "sel.last")
        text_underline = False
    else:  
        text.tag_add("underline", "sel.first", "sel.last")
        text_underline = True

def strikethrough_text():
    strikethrough_font = font.Font(text, text.cget("font"))
    strikethrough_font.configure(strike="strikethrough")

    text.tag_configure("strike through", font=strikethrough_font)

    current_tags = text.tag_names("sel.first")

    if "strikethrough" in current_tags:
        text.tag_remove("strikethrough", "sel.first", "sel.last")
        text_strikethrough = False
    else:  
        text.tag_add("strikethrough", "sel.first", "sel.last")
        text_strikethrough = True

def close():
    global saved, file_path, before_data
    after_data = text.get("1.0","end-1c")
    if text.get("1.0","end-1c") != "":
        if saved == False:
            error_window = messagebox.askyesnocancel("Quit?", "Do you want save your work before you quit? You have unsaved changes.", icon="warning", default="yes")
            if str(repr(error_window)) == "True":
                update()
                root.destroy()
            elif str(repr(error_window)) == "False":
                root.destroy()
            elif str(repr(error_window)) == "None":
                pass
        else:
            root.destroy()
    elif text.get("1.0","end-1c") == "" or after_data == before_data:
        root.destroy()
    elif after_data != before_data:
        if saved == False:
            error_window = messagebox.askyesnocancel("Quit?", "Do you want save your work before you quit? You have unsaved changes.", icon="warning", default="yes")
            if str(repr(error_window)) == "True":
                update()
                root.destroy()
            elif str(repr(error_window)) == "False":
                root.destroy()
            elif str(repr(error_window)) == "None":
                pass
        else:
            root.destroy()


root = tk.Tk()
root.title(f"Bit Textitor - AI Version: {openai.__version__}")
#root.wm_title("Textitor")
root.geometry("1797x1200")
root.grid_location(0, 0)
nb = ttk.Notebook(root) 
root.configure(background='white')
root.wm_title("Bit Textitor")

frame = Frame(root)
frame.pack()

toolbar_frame = ttk.Frame(nb)
toolbar_frame.pack(side = TOP)

icon = PhotoImage(file = "/Users/admin/Downloads/Textitor_Logo_(BETA_Ver.).png")
root.iconphoto(False, icon)

label1 = Label(root, text = "Bit Textitor")
label1.config(font =("Helvecitca", 20))
label1.pack(side = TOP)

label2 = Label(root, text = f"Welcome to Bit Textitor! This is a test version of Bit Textitor. This is a simple text editor that allows you to create, open, and save text files, which uses AI. It uses the custom file outlet '.txtr'. To save an already existing file, click on 'Save', \ntype in the exact same name of the file, and click on 'Save'. Then it will give you a prompt if you want to replace the file. Click on 'Yes' to replace the file. Then you have successfully updated the file. We're trying to make this text editor as user-friendly as possible.")
label2.config(font =("Helvecitca", 12))
label2.pack(side = TOP)

if ai_on_off == False:
    label3 = Label(root, text = "(AI capability: Off) No AI suggestions.")
    label3.config(font =("Helvecitca", 12))
    label3.pack(side = TOP)
elif ai_on_off == True:
    label3 = Label(root, text = "(AI capability: On) No AI suggestions.")
    label3.config(font =("Helvecitca", 12))
    label3.pack(side = TOP)

if bolden_text == False:
    label4 = Label(root, text = "")
    label4.config(font =("Helvecitca", 12))
    label4.pack(side = TOP)

def which_button(button_text):
    # Printing the text when a button is clicked
    if button_text == "new":
        new_file()
    elif button_text == "open":
        open_file()
    elif button_text == "save":
        save_file()
    elif button_text == "ai on":
        ai_on()
    elif button_text == "ai off":
        ai_off()
    elif button_text == "ai grammar":
        ai_grammar()
    elif button_text == "update":
        update()
    elif button_text == "close":
        close()

# Creating and displaying of button b1
close_b = Button(root, text="Close", command=lambda: which_button("close"))
#close_b.configure(background='white')
close_b.pack(side=BOTTOM)

update_b = Button(root, text="Update (Save automatically)", command=lambda: which_button("update"))
update_b.pack(side = BOTTOM)

ai_b_3 = Button(root, text="Check Grammar with AI", command=lambda: which_button("ai grammar"))
ai_b_3.pack(side = BOTTOM)

ai_b_2 = Button(root, text="Turn AI off", command=lambda: which_button("ai off"))
ai_b_2.pack(side = BOTTOM)

ai_b_1 = Button(root, text="Turn AI on", command=lambda: which_button("ai on"))
ai_b_1.pack(side = BOTTOM)

save_b = Button(root, text="Save", command=lambda: which_button("save"))
save_b.pack(side = BOTTOM)

open_b = Button(root, text="Open", command=lambda: which_button("open"))
open_b.pack(side = BOTTOM)

new_b = Button(root, text="New", command=lambda: which_button("new"))
new_b.pack(side = BOTTOM)


text = Text(root, wrap="word", undo=True, bg="white", fg="black", insertbackground="black", font=("Aptos", 16))
text.pack(expand="yes", fill="both")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File-menu
file_menu = tk.Menu(menu_bar, tearoff=0)
ai_menu = tk.Menu(menu_bar, tearoff=0)
formatting_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="AI", menu=ai_menu)
menu_bar.add_cascade(label="Formatting", menu=formatting_menu)

file_menu.add_command(label="New", command=new_file, accelerator="Cmd+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Cmd+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Cmd+S")
file_menu.add_separator()
file_menu.add_command(label="Close", command=close, accelerator="Cmd+Q")
root.bind("<Command-n>", lambda event: new_file())
root.bind("<Command-o>", lambda event: open_file())
root.bind("<Command-s>", lambda event: save_file())
root.bind("<Command-q>", lambda event: close())

ai_menu.add_command(label="Turn AI on", command=ai_on, accelerator="F1")
ai_menu.add_command(label="Turn AI off", command=ai_off, accelerator="F2")
ai_menu.add_separator()
ai_menu.add_command(label="Check grammar with AI", command=ai_grammar, accelerator="F3")
ai_menu.add_command(label="Summarize text with AI", command=ai_grammar, accelerator="F4")
ai_menu.add_command(label="Translate text with AI", command=ai_grammar, accelerator="F5")

formatting_menu.add_command(label="Bolden text", command=bolden_text, accelerator="Cmd+B")
formatting_menu.add_command(label="Italicize text", command=italicize_text, accelerator="Cmd+I")
formatting_menu.add_command(label="Underline text", command=underline_text, accelerator="Cmd+U")
formatting_menu.add_command(label="Strike-through text", command=strikethrough_text, accelerator="Cmd+Shift+X")
root.bind("<Command-b>", lambda event: bolden_text())
root.bind("<Command-i>", lambda event: italicize_text())
root.bind("<Command-u>", lambda event: underline_text())
root.bind("<Command-Shift-x>", lambda event: strikethrough_text())

root.mainloop()