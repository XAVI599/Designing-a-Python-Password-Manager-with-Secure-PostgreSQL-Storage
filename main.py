# python-password-manager-with-postgres_database

from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import psycopg


# -- connecting to postgres database ---------------------

conn = psycopg.connect(
    dbname='your database',
    host='localhost', # use localhost if postgres running on your local machine
    user='your databaseuser',
    password='your password',
    port='5432'
)

# -------------- enter data into database-----------------------------------#

def enterdata():

    website_text = website_entry.get()
    email_text = email_entry.get()
    password_text = password_entry.get()


    if len(website_text) < 1 or len(email_text) < 1 or len(password_text) < 1:
        messagebox.showinfo(title="oops", message="Please dont leave any fields empty")
    else:
        # inserting into postgres table
        cursor = conn.cursor()
        try:
            cursor.execute("""insert into password_manager (website,email,password) values (%s,%s,%s);""",
                           (website_text, email_text, password_text))

        except BaseException:
            conn.rollback()

            #inform user an error occured
            messagebox.showinfo(title='Error',message='Data not saved to database')

        else:
            conn.commit()

        finally:
         cursor.close()
         website_entry.delete(0, END)  # To delete data from the entry label
         password_entry.delete(0, END)


# -- search the database for the website #---------------------

def search_database():
    cursor = conn.cursor()
    website_search = website_entry.get()
    try:
        cursor.execute("""select website,email,password from password_manager where website = %s;""", [website_search])
        retrived_data = cursor.fetchall()

        if len(retrived_data) == 0:
            raise Exception

    except Exception:
        conn.rollback()
        messagebox.showinfo(message="Data file not found on the database", title="Error")

    else:
        create_sentence = ''
        website = ''
        all_psd = []
        for t in retrived_data:
            website = t[0]
            email = t[1]
            password = t[2]

            create_sentence += f"Email : {email}\nPassword : {password}\n"
            all_psd.append(password)

        messagebox.showinfo(title=website, message=create_sentence)
        cursor.close()

        # copy the password to clipboard

        pyperclip.copy(all_psd)



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=password)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

# TODO 1 : create canvas

canvas = Canvas(width="200", height=200)
photo_image = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=photo_image)
canvas.grid(row=0, column=1)

# TODO 2:arrange the labels in proper place

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=19)
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
website_entry.focus()

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = Entry(width=37)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0,
                   "Your default gmail address")  # --> 0 denotes the index you can also use a buildin variable called END if u want to continue writing from the end of another text

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=19)
password_entry.grid(row=3, column=1, sticky="w", columnspan=2)

add_button = Button(width=36, text="Add", command=enterdata)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(row=3, column=1, sticky="e", columnspan=2)

search_button = Button(text ="Search",width=16,command=search_database)
search_button.grid(column=1,row=1,sticky="e",columnspan=2)

window.mainloop()
conn.close()


