import tkinter
from tkinter.ttk import *
from tkinter import *
import fls_main

root = Tk()
root.title("Heart Disease Diagnosis")
style = Style()
root.configure(bg='lightblue')


line1 = Label(root, bg="lightblue", pady=5,
              text="If you are suffering from A Heart Disease").pack()
line2 = Label(
    root, bg="lightblue", pady=5, text="This program will help in diagnois of the severity of it.").pack()
line3 = Label(
    root, bg="lightblue", pady=5, text="Please input the various parameters to help us in the diagnosis.").pack()
# line4 = Label(root, text="(0 is least)").pack()

age, bp, chl, diabetes, chest_pain, ecg = DoubleVar(), DoubleVar(
), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar()

age_label = Label(root, bg="lightblue", pady=5, text="Your age").pack()
age_field = Entry(root)
age_field.pack()

bp_label = Label(root, bg="lightblue", pady=5,
                 text="Systolic Blood Pressure").pack()
bp_field = Entry(root)
bp_field.pack()

chl_label = Label(root, bg="lightblue", pady=5,
                  text="Cholestrol in mg/dL").pack()
chl_field = Entry(root)
chl_field.pack()

diabetes_label = Label(root, bg="lightblue", pady=5,
                       text="Diabetes HbA1c").pack()
diabetes_field = Entry(root)
diabetes_field.pack()

chest_pain_label = Label(root, bg="lightblue", pady=5,
                         text="Chest Pain").pack()
chest_pain_label = Label(
    root, bg="lightblue", text="(Note : 0 is minumum and 1 is maximum chest pain)").pack()
chest_pain_slider = Scale(
    root, bg="white", from_=0, to=1, orient=HORIZONTAL, resolution=0.1, variable=chest_pain)
chest_pain_slider.pack()

# ecg_label = Label(root, bg="lightblue", pady=5, text="ECG in mV").pack()
# ecg_field = Entry(root, bg="white")
# ecg_field.pack()


def Click():
    output_label = Label(root, bg="lightblue", pady=5, text=("Inputs:", age_field.get(),
                                                             bp_field.get(),
                                                             chl_field.get(),
                                                             diabetes_field.get(),
                                                             chest_pain_slider.get(),
                                                             #  ecg_field.get()
                                                             )).pack()
    chance = fls_main.calculate_FLS(
        float(age_field.get()), float(bp_field.get()), float(chl_field.get()), float(diabetes.get()), float(chest_pain_slider.get()))
    output_label = Label(root, bg="lightblue", pady=5, text=(
        chance, "% likely to get a Heart Disease.")).pack()


# calc_button = tkinter.Button(
#     root, text="Diagnose Heart Disease", command=Click).pack()

btn1 = tkinter.Button(root, text='Diagnose Heart Disease', font=('calibri', 12, 'bold'), bg='white', pady=5,
                      fg='red', activebackground='red', activeforeground='white',
                      command=Click).pack()
# btn1.grid(row = 0, column = 3, pad = 10)
root.mainloop()
