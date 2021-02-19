import tkinter as tk

HEIGHT = 500
WIDTH = 600
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg="#cce6ff")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


button = tk.Button(frame, text="Test button")
button.pack(side="left")

label = tk.Label(frame, text="This is a label", bg="yellow")
label.pack(side="right  ")

entry = tk.Entry(frame, bg="green")
entry.pack()

root.mainloop()