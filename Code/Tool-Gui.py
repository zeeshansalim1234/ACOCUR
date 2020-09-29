from tkinter import *
import numpy as np
import pandas as pd

def btnsubmit():

    ans = myTextBox.get()

    if pd.isnull(ans):
        text = "Please enter your choice"
    else:
        if not ans.isdigit():
            text = "The entered choice is not a valid number"
        else:
            text = "Entered choice is : " + ans


    label_error = Label(root, text= text)
    label_error.grid(row=3, column = 1)


root = Tk()
root.title('ACOCUR Tool')
root.geometry('400x600')

titleLabel = Label(root, text="Welcome to ACOCUR !!").grid(row=0, column=0, columnspan=2)
# titleLabel.pack()

choiceLabel = Label(root, text="Enter your choice").grid(row=1, column = 0)
myTextBox = Entry(root, width=30)
myTextBox.grid(row=1, column = 1)

myButton = Button(root, text="Submit", padx=10, pady=5, command=btnsubmit)
myButton.grid(row=2, column = 1)

root.mainloop()
