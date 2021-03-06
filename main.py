import json
import tkinter
import random
import pyperclip
from tkinter import messagebox, END, E

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+',
           '^', ',', '.', ':', '|', '=', '?', '@', ']']


frame = tkinter.Tk()
frame.title("Password Manager")
frame.config(padx=50, pady=50)


def pass_generate():

    password_letter = [random.choice(letters) for _ in range(random.randint(3, 9))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(3, 9))]
    password_number = [random.choice(numbers) for _ in range(random.randint(3, 9))]
    password_list = password_letter + password_symbols + password_number

    random.shuffle(password_list)
    final_password = "".join(password_list)
    password_input.delete(0, 'end')
    password_input.insert(0, final_password)
    pyperclip.copy(password_input.get())


def password_checking(password):
    count_letter = 0
    count_symbol = 0
    count_number = 0
    for char in password:
        if char in letters:
            count_letter += 1
        elif char in numbers:
            count_number += 1
        else:
            count_symbol += 1

    if not 32 > len(password) > 8 or not count_number > 0 or not count_symbol > 0:
        messagebox.showwarning('Yes', '• Must be 8-32 characters long\n'
                                      '• At least one number\n'
                                      '• At least one special character from the')
    else:
        messagebox.showinfo('Ok', 'Successfully Saved!')
        return True


def add_detail():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    format_data = {str(website).lower(): {
                "username": username,
                "password": password
    }}

    if len(website_input.get()) < 1 or len(username_input.get()) < 1 or len(password_input.get()) < 1:
        messagebox.showwarning('Ok', "Field is Empty")
    else:
        if password_checking(password_input.get()):
            try:
                with open("password_book.json", mode="r") as password_file:
                    data = json.load(password_file)

            except FileNotFoundError:
                with open("password_book.json", mode="w") as password_file:
                    json.dump(format_data, password_file, indent=4)

            else:
                data.update(format_data)

                with open("password_book.json", mode="w") as password_file:
                    json.dump(data, password_file, indent=4)

            finally:
                website_input.delete(0, END)
                username_input.delete(0, END)
                password_input.delete(0, END)


def search():
    try:
        with open("password_book.json") as password_file:
            data = json.load(password_file)
    except KeyError:
        messagebox.showwarning('Ok', "Website is not Found")
        website_input.delete(0, END)
        username_input.delete(0, END)
        password_input.delete(0, END)
    except FileNotFoundError:
        messagebox.showwarning('Ok', "Website is not Found")

    else:
        website = str(website_input.get()).lower()
        username_input.delete(0, END)
        password_input.delete(0, END)
        username_input.insert(0, data[website]["username"])
        password_input.insert(0, data[website]["password"])

# canvas
canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
lock_image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 110, image=lock_image)
canvas.grid(row=0, column=1)

# label
website_label = tkinter.Label(text="Website:", font=("Arial", 15, "bold"),
                              anchor="center")
website_label.grid(row=1, column=0)

username_label = tkinter.Label(text="Email /Username:", font=("Arial", 15, "bold"),
                               anchor="center")
username_label.grid(row=2, column=0)

password_label = tkinter.Label(text="Password:", font=("Arial", 15, "bold"),
                               anchor="center")
password_label.grid(row=3, column=0)

# Entry
website_input = tkinter.Entry(width=22)
website_input.grid(row=1, column=1, )
website_input.focus()

username_input = tkinter.Entry(width=40)
username_input.grid(row=2, column=1, columnspan=2)

password_input = tkinter.Entry(width=22)
password_input.grid(row=3, column=1)

# button
pass_generate_button = tkinter.Button(text="Generate Password",
                                      bd=0, font=("Arial", 15),
                                      command=pass_generate, fg="#000000", width=14)
pass_generate_button.grid(row=3, column=2)

add_button = tkinter.Button(text="Add", bd=0, width=38, font=("Arial", 15, "bold"),
                            command=add_detail, fg="#000000")
add_button.grid(row=4, column=1, columnspan=2)

search_button = tkinter.Button(text="Search", bd=0, font=("Arial", 15),
                               command=search, fg="#000000", width=14)
search_button.grid(row=1, column=2, sticky=E)

frame.mainloop()
