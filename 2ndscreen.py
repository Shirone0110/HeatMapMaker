import numpy as np
import seaborn as sns
import tkinter as tk
from tkinter.constants import DISABLED, END, NORMAL
from tkinter.filedialog import asksaveasfile
from tkinter import StringVar, colorchooser, Frame, messagebox
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
        BLFrame.entries[ind * 2 + 2].configure(state = NORMAL)
        BLFrame.entries[ind * 2 + 2].delete(0, END)
        BLFrame.entries[ind * 2 + 2].insert(END, text)
        BLFrame.entries[ind * 2 + 2].configure(state = DISABLED)
    except KeyError:
        print("Ignore this")

def create_plot(colormap): #create plot
    sns.set(style = 'white')
    data = np.random.rand(10, 10)
    f, ax = plt.subplots(figsize = (4, 3))
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

def export(fig):
    files = [('PNG', '*.png'), ('PDF', '*.pdf')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    if file is None:
        return
    addr = file.name
    addr = addr.split('/')
    fig.savefig(addr[-1])

def preview(num):
    colors = []
    split = [0]
    for ind in range(num):
        colors.append(BLFrame.buttons[ind].cget('bg'))
        split.append(float(BLFrame.string_vars[ind * 2 + 1].get()) / 100)
    split[num - 1] = 1
    cdict = NonLinCdict(split, colors)
    colormap = LinearSegmentedColormap('Custom Color', cdict)
    fig = create_plot(colormap)
    canvas = FigureCanvasTkAgg(fig, master = BRFrame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0)
    cmd = lambda fig = fig: export(fig)
    exportbutton = tk.Button(BRFrame, text = "Export", command = cmd)
    exportbutton.grid(row = 1, column = 0, sticky = "se")

def check(num):
    for ind in range(num):
        if BLFrame.buttons[ind].cget('bg') == 'SystemButtonFace':
            messagebox.showerror("Error", "Please choose color")
            return
    
    for ind in range(num):
        try:
            float(BLFrame.string_vars[ind * 2 + 1].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter range in numbers")
            return

    tmp = 0
    for ind in range(num):
        val = float(BLFrame.string_vars[ind * 2 + 1].get())
        if val < tmp:
            messagebox.showerror("Error", "Please enter valid range")
            return
        tmp = val
    
    preview(num)

def display(num):
    BLFrame.buttons = {}
    BLFrame.entries = {}
    BLFrame.string_vars = []
    
    for ind in range(num):
        #label
        tk.Label(BLFrame, text = "Color " + str(ind + 1)).grid(column = 0, row = ind + 2)

        #choose color buttons
        BLFrame.buttons[ind] = tk.Button(BLFrame, width = 3)
        BLFrame.buttons[ind].grid(column = 1, row = ind + 2)
        cmd = lambda btn = BLFrame.buttons[ind]: pressed(btn)
        BLFrame.buttons[ind].configure(command = cmd)

        #entries left
        BLFrame.string_vars.append(StringVar())
        BLFrame.entries[ind * 2] = tk.Entry(BLFrame, width = 5, 
            textvariable = BLFrame.string_vars[ind * 2])
        BLFrame.entries[ind * 2].grid(column = 2, row = ind + 2)

        tk.Label(BLFrame, text = "to").grid(column = 3, row = ind + 2)

        #entries right
        BLFrame.string_vars.append(StringVar())
        BLFrame.string_vars[ind * 2 + 1].trace('w', 
            lambda name, index, mode, var = BLFrame.string_vars[ind * 2 + 1], i = ind: entry(var, i))
        BLFrame.entries[ind * 2 + 1] = tk.Entry(BLFrame, width = 5, 
                                    textvariable = BLFrame.string_vars[ind * 2 + 1])
        BLFrame.entries[ind * 2 + 1].grid(column = 4, row = ind + 2)

        tk.Label(BLFrame, text = "%").grid(column = 5, row = ind + 2)

    #set entries status
    BLFrame.entries[0].insert(END, '0')
    BLFrame.entries[num * 2 - 1].insert(END, '100')
    for ind in range(num):
        BLFrame.entries[ind * 2].configure(state = DISABLED)
    BLFrame.entries[num * 2 - 1].configure(state = DISABLED)

    #preview button
    cmd = lambda n = num: check(n)
    button = tk.Button(BLFrame, text="Preview", command = cmd)
    button.grid(column = 2, row = num + 2, sticky = "se")

def init_BLFrame():
    label = tk.Label(BLFrame, text = "Colors")
    label.grid(column = 0, row = 0)

    v = tk.IntVar()
    optionList = np.arange(4, 11, 1)
    dropdown = tk.OptionMenu(BLFrame, v, *optionList, command = display)
    dropdown.grid(column = 1, row = 0)

def create_default(color): #create plot
    sns.set(style = 'white')
    data = np.random.rand(10, 10)
    f, ax = plt.subplots(figsize = (4, 3))
    if (int(color) < 3):
        cmap = sns.color_palette(values[color])
    else:
        cmap = sns.color_palette(values[color], as_cmap = True)
    sns.heatmap(data, cmap = cmap, center = 0, linewidths = 0.5)
    return f

def draw(v): #redraw heatmap when change button
    color = v.get()
    fig = create_default(color)
    canvas = FigureCanvasTkAgg(fig, master = TRFrame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0)
    cmd = lambda fig = fig: export(fig)
    exportbutton = tk.Button(TRFrame, text = "Export", command = cmd)
    exportbutton.grid(row = 1, column = 0, sticky = "se")

def init_TLFrame():
    canvas = tk.Canvas(TLFrame, width = 250, height = 320)
    canvas.grid(row = 0, column = 0, rowspan = 10, columnspan = 6)

    label = tk.Label(TLFrame, text = "Choose a color palette:")
    label.grid(column = 0, row = 0, columnspan = 3, sticky = "nw")

    v = tk.StringVar()
    #some random color schemes
    v.set("1")
    draw(v)
    count = 0

    for val, text in values.items():
        count += 1
        tk.Radiobutton(TLFrame, text = text, variable = v, 
            command = lambda v = v: draw(v), 
            value = val).grid(row = count, column = 0, sticky = "nw")

def init_BRFrame():
    canvas = tk.Canvas(BRFrame, width = 420, height = 320)
    canvas.grid(row = 0, column = 0)

sns.set()
root = tk.Tk()
root.wm_title("Choose Color")

MainFrame = Frame(root)
MainFrame.grid(row = 0, column = 0, sticky = "nswe")

TLFrame = Frame(MainFrame)
TLFrame.grid(row = 0, column = 0, sticky = "nswe")
TRFrame = Frame(MainFrame)
TRFrame.grid(row = 0, column = 1, sticky = "nswe")
BLFrame = Frame(MainFrame)
BLFrame.grid(row = 1, column = 0, sticky = "nswe")
BRFrame = Frame(MainFrame)
BRFrame.grid(row = 1, column = 1, sticky = "nswe")

values = {"1": "pastel", "2": "hls",
            "3": "Blues", "4": "YlOrBr",
            "5": "icefire"}

init_TLFrame()
init_BLFrame()
init_BRFrame()

button = tk.Button(root, text="Quit", command=root.quit)
button.grid(row = 2, column = 1)

tk.mainloop()