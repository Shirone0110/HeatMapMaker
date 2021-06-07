import tkinter as tk
from tkinter.constants import DISABLED, END, NORMAL
import numpy as np
import seaborn as sns
from tkinter import StringVar, colorchooser, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap

def pressed(btn):
    color = colorchooser.askcolor(title = "Choose color")
    btn.configure(bg = color[1])

def entry(sv, ind):
    text = sv.get()
    try:
        root.entries[ind * 2 + 2].configure(state = NORMAL)
        root.entries[ind * 2 + 2].delete(0, END)
        root.entries[ind * 2 + 2].insert(END, text)
        root.entries[ind * 2 + 2].configure(state = DISABLED)
    except KeyError:
        print("Ignore this")

def create_plot(colormap): #create plot
    sns.set(style = 'white')
    data = np.random.rand(10, 10)
    f, ax = plt.subplots(figsize = (5, 4))
    sns.heatmap(vmin = 0.0, vmax = 1.0, data = data, cmap = colormap, linewidths = 0.5)
    return f

def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

def preview(num):
    colors = []
    split = [0]
    for ind in range(num):
        colors.append(root.buttons[ind].cget('bg'))
        split.append(float(root.string_vars[ind * 2 + 1].get()) / 100)
    split[num - 1] = 1
    cdict = NonLinCdict(split, colors)
    colormap = LinearSegmentedColormap('Custom Color', cdict)
    fig = create_plot(colormap)
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = num + 4, column = 0, columnspan = 15, rowspan = 13)

    #redraw quit button
    button = tk.Button(root, text="Quit", command=root.quit)
    button.grid(row = num + 5, column = 14)

def check(num):
    for ind in range(num):
        if root.buttons[ind].cget('bg') == 'SystemButtonFace':
            messagebox.showerror("Error", "Please choose color")
            return
    
    for ind in range(num):
        try:
            float(root.string_vars[ind * 2 + 1].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter range in numbers")
            return

    tmp = 0
    for ind in range(num):
        val = float(root.string_vars[ind * 2 + 1].get())
        if val < tmp:
            messagebox.showerror("Error", "Please enter valid range")
            return
        tmp = val
    
    preview(num)

def display(num):
    root.buttons = {}
    root.entries = {}
    root.string_vars = []
    for ind in range(num):
        #label
        tk.Label(root, text = "Color " + str(ind + 1)).grid(column = 0, row = ind + 2)

        #choose color buttons
        root.buttons[ind] = tk.Button(root, width = 3)
        root.buttons[ind].grid(column = 1, row = ind + 2)
        cmd = lambda btn = root.buttons[ind]: pressed(btn)
        root.buttons[ind].configure(command = cmd)

        #entries left
        root.string_vars.append(StringVar())
        root.entries[ind * 2] = tk.Entry(root, width = 5, textvariable = root.string_vars[ind * 2])
        root.entries[ind * 2].grid(column = 2, row = ind + 2)

        tk.Label(root, text = "to").grid(column = 3, row = ind + 2)

        #entries right
        root.string_vars.append(StringVar())
        root.string_vars[ind * 2 + 1].trace('w', 
            lambda name, index, mode, var = root.string_vars[ind * 2 + 1], i = ind: entry(var, i))
        root.entries[ind * 2 + 1] = tk.Entry(root, width = 5, 
                                    textvariable = root.string_vars[ind * 2 + 1])
        root.entries[ind * 2 + 1].grid(column = 4, row = ind + 2)

        tk.Label(root, text = "%").grid(column = 5, row = ind + 2)

    #set entries status
    root.entries[0].insert(END, '0')
    root.entries[num * 2 - 1].insert(END, '100')
    for ind in range(num):
        root.entries[ind * 2].configure(state = DISABLED)
    root.entries[num * 2 - 1].configure(state = DISABLED)

    #preview button
    cmd = lambda n = num: check(n)
    button = tk.Button(root, text="Preview", command = cmd)
    button.grid(column = 2, row = num + 2)

sns.set()
root = tk.Tk()
root.wm_title("Choose Color")

label = tk.Label(root, text = "Colors")
label.grid(column = 0, row = 0)

v = tk.IntVar()
optionList = np.arange(4, 13, 1)
dropdown = tk.OptionMenu(root, v, *optionList, command = display)
dropdown.grid(column = 1, row = 0)

tk.mainloop()