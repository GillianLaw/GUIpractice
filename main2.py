import random
import sqlite3
import string
import PySimpleGUI as sg
import tkinter as Tk
import pyperclip as pc

"""Building a password generator using PySimpleGUI"""

def create_password(length):

    p1 = "".join(random.choice(string.ascii_lowercase) for i in range(2))
    p2 = "".join(random.choice(string.ascii_uppercase) for i in range(2))
    p3 = "".join(random.choice(string.digits) for i in range(3))
    p4 = "".join(random.choice(string.punctuation) for i in range(3))

# Add these together then randomise again.
# Don't want a password lower case first, then upper, etc

    all = p1 + p2 + p3 + p4

    random_password = "".join(random.choice(all) for j in range(length))
    return random_password


def save_to_db(website, password):
    db = sqlite3.connect('passwordOOP.sqlite')
    db.execute("CREATE TABLE IF NOT EXISTS passwordOOP (name TEXT, pass TEXT)")
    db.execute("INSERT INTO passwordOOP (name, pass) VALUES (?, ?)", (website, password))

    update_sql = "SELECT * FROM passwordOOP"
    cursor = db.cursor()
    cursor.execute(update_sql)

    cursor.connection.commit()
    cursor.close()
    db.close()


def search_password(search):
    db = sqlite3.connect('passwordOOP.sqlite')

    for row in db.execute("SELECT * FROM passwordOOP WHERE name LIKE ?", (search,)):
        return row[1]

    db.close()

# def copy_button():
#     clip = Tk()
#     clip.withdraw()
#     clip.clipboard_clear()
#     clip.clipboard_append(window['-OUT-'])
#     clip.destroy()


def main():
    sg.theme('DarkTeal7')

    layout = [  [sg.Text('Welcome to the password generator! Get a new password, or find one you already created')],
                [sg.Text('                              ')],
                [sg.Text('Please enter the site name:'), sg.InputText(size=(15,1), key='-IN-')],
                [sg.Text('If you need a new password, how many characters? (between 6 and 10):'), sg.InputText(size=(3,1), key='-CHAR-')],
                [sg.Button('Give me a NEW password')],
                [sg.Text('           OR                 ')],
                [sg.Button('Find my STORED password')],
                [sg.Text('                              ')],
                # [sg.Output(size=(10,1))],
                [sg.Text('Your password is'), sg.Text(size=(15,1), key='-OUT-')],
                [sg.Text('This password will automatically be saved to your clipboard')],
                [sg.Text('                              ')],
                [sg.Button('Close Window')]
                ]

    window = sg.Window("Gillian's whizzy password generator", layout)

    while True:
        event, values = window.read()
        # End program if user closes window
        if event == "Close Window" or event == sg.WIN_CLOSED:
            break
        if event == 'Give me a NEW password':
            website = str(values['-IN-'])
            length = int(values['-CHAR-'])

            password = create_password(length)
            window['-OUT-'].update(password)
            pc.copy(password)

            save_to_db(website, password)
        if event == 'Find my STORED password':
            search = str(values['-IN-'])
            password = search_password(search)
            window['-OUT-'].update(password)
            pc.copy(password)



    window.close()

if __name__ == '__main__':
    main()
