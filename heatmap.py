#!/usr/bin/env python
import tkinter as tk
import seaborn as sns
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def create_plot(color): #create plot
    sns.set(style = 'white')
    data = np.random.rand(10, 10)
    f, ax = plt.subplots(figsize = (6, 6))
    if (int(color) < 3):
        cmap = sns.color_palette(values[color])
    else:
        cmap = sns.color_palette(values[color], as_cmap = True)
    sns.heatmap(data, cmap = cmap, center = 0, linewidths = 0.5)
    return f

def redraw(): #redraw heatmap when change button
    color = v.get()
    print(color)
    fig = create_plot(color)
    canvas.figure = fig
    canvas.draw()

def init(root): #initialize radio buttons and quit button
    label = tk.Label(root, text = """Choose a color palette:""").pack(anchor = tk.W)

    for val, text in values.items():
        tk.Radiobutton(root, 
            text = text,
            padx = 20, 
            variable = v, 
            command = redraw,
            value = val).pack(anchor=tk.W)
    
    v.set("1")
    
    button = tk.Button(root, text="Quit", command=root.quit)
    button.pack()

sns.set()
root = tk.Tk()
root.wm_title("Heatmap")

v = tk.StringVar()
#some random color schemes
values = {"1": "pastel", "2": "hls",
        "3": "Blues", "4": "YlOrBr",
        "5": "icefire"}
init(root)

#initial plot
fig = create_plot("1")
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.draw()
canvas.get_tk_widget().pack()

tk.mainloop()

