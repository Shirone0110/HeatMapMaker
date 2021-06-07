import numpy as np
import seaborn as sns
import tkinter as tk
from tkinter.constants import DISABLED, END, NORMAL
from tkinter.filedialog import asksaveasfile, askopenfile
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

def create_row(ind):
    #create subframe
    BLFrame.subframe[ind] = Frame(BLFrame)
    BLFrame.subframe[ind].grid(row = ind + 1, column = 0, columnspan = 6)

    #label
    label = tk.Label(BLFrame.subframe[ind], text = "Color " + str(ind + 1))
    label.grid(column = 0, row = ind + 2)

    #color changing button
    BLFrame.buttons[ind] = tk.Button(BLFrame.subframe[ind], width = 3)
    BLFrame.buttons[ind].grid(column = 1, row = ind + 2, padx = 5)
    cmd = lambda btn = BLFrame.buttons[ind]: pressed(btn)
    BLFrame.buttons[ind].configure(command = cmd)

    #left entries
    BLFrame.string_vars.append(StringVar())
    BLFrame.entries[ind * 2] = tk.Entry(BLFrame.subframe[ind], width = 5,
        textvariable = BLFrame.string_vars[ind * 2])
    BLFrame.entries[ind * 2].grid(column = 2, row = ind + 2, padx = 5)

    #right entries
    BLFrame.string_vars.append(StringVar())
    BLFrame.string_vars[ind * 2 + 1].trace('w',
        lambda name, index, mode, var = BLFrame.string_vars[ind * 2 + 1], i = ind: entry(var, i))
    BLFrame.entries[ind * 2 + 1] = tk.Entry(BLFrame.subframe[ind], width = 5,
        textvariable = BLFrame.string_vars[ind * 2 + 1])
    BLFrame.entries[ind * 2 + 1].grid(column = 4, row = ind + 2, padx = 5)

    #decoration
    tk.Label(BLFrame.subframe[ind], text = "to").grid(column = 3, row = ind + 2)
    tk.Label(BLFrame.subframe[ind], text = "%").grid(column = 5, row = ind + 2)

def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

def create_plot(colormap): #create plot with color map
    sns.set(style = 'white')
    data = np.random.rand(10, 10)
    f, ax = plt.subplots(figsize = (4, 3))
    sns.heatmap(vmin = 0.0, vmax = 1.0, data = data, cmap = colormap, linewidths = 0.5)
    return f

def export(fig): #export figure in pdf or png
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

    #get color and range
    for ind in range(num):
        colors.append(BLFrame.buttons[ind].cget('bg'))
        split.append(float(BLFrame.string_vars[ind * 2 + 1].get()) / 100)

    #range from 0 to 1
    split[num - 1] = 1

    #create color map
    cdict = NonLinCdict(split, colors)
    colormap = LinearSegmentedColormap('Custom Color', cdict)

    #create figure
    fig = create_plot(colormap)
    canvas = FigureCanvasTkAgg(fig, master = BRFrame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0)

    #export button
    cmd = lambda fig = fig: export(fig)
    exportbutton = tk.Button(BRFrame, text = "Export", command = cmd)
    exportbutton.grid(row = 1, column = 0, sticky = "se")

def check(num):
    #check all color selected
    for ind in range(num):
        if BLFrame.buttons[ind].cget('bg') == 'SystemButtonFace':
            messagebox.showerror("Error", "Please choose color")
            return
    
    #check all range inserted
    for ind in range(num):
        try:
            float(BLFrame.string_vars[ind * 2 + 1].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter range in numbers")
            return

    #check all range valid
    tmp = 0
    for ind in range(num):
        val = float(BLFrame.string_vars[ind * 2 + 1].get())
        if val < tmp:
            messagebox.showerror("Error", "Please enter valid range")
            return
        tmp = val
    
    preview(num)

def display(num):
    #show number of rows needed
    for ind in range(num):
        BLFrame.entries[ind * 2 + 1].configure(state = NORMAL)
        BLFrame.entries[ind * 2 + 1].delete(0, END)
        BLFrame.subframe[ind].grid()

    for ind in range(num, 10):
        BLFrame.subframe[ind].grid_remove()

    BLFrame.entries[num * 2 - 1].insert(END, '100')
    BLFrame.entries[num * 2 - 1].configure(state = DISABLED)

    #preview button
    cmd = lambda n = num: check(n)
    button = tk.Button(BLFrame, text="Preview", command = cmd)
    button.grid(column = 2, row = 12, sticky = "se")

def init_BLFrame():
    label = tk.Label(BLFrame, text = "Colors")
    label.grid(column = 0, row = 0)

    v = tk.IntVar()
    optionList = np.arange(4, 11, 1)
    dropdown = tk.OptionMenu(BLFrame, v, *optionList, command = display)
    dropdown.grid(column = 1, row = 0)

    BLFrame.buttons = {}
    BLFrame.entries = {}
    BLFrame.string_vars = []
    BLFrame.subframe = {}

    for ind in range(10):
        create_row(ind)
        BLFrame.subframe[ind].grid_remove()

    #set entries status
    BLFrame.entries[0].insert(END, '0')
    for ind in range(10):
        BLFrame.entries[ind * 2].configure(state = DISABLED)

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

    #some random color schemes
    global values
    values = {"1": "pastel", "2": "hls", "3": "Blues", "4": "YlOrBr",
            "5": "icefire"}

    v = tk.StringVar()
    v.set("1")
    draw(v)
    count = 0

    for val, text in values.items():
        count += 1
        tk.Radiobutton(TLFrame, text = text, variable = v, 
            command = lambda v = v: draw(v), 
            value = val).grid(row = count, column = 0, sticky = "nw")

def init_BRFrame():
    canvas = tk.Canvas(BRFrame, width = 400, height = 300)
    canvas.grid(row = 0, column = 0)

def next_btn():
    SetupFrame.grid_remove()
    HeatMapFrame.grid()

def choose_file():
    files = [('CSV', '*.csv')]
    file = askopenfile(filetypes = files, defaultextension = files)
    if file is None:
        return
    addr = file.name
    addr = addr.split('/')
    showfilename.config(text = addr[-1])

def init_SetupFrame():
    #choose file prompt
    tk.Label(SetupFrame, text = "Choose data file").grid(row = 0, column = 0, sticky = "w")

    #show file name
    global showfilename
    showfilename = tk.Label(SetupFrame, text = "No file chosen")
    showfilename.grid(row = 1, column = 1)

    global choosefile, vYesNo

    choosefile = tk.Button(SetupFrame, text = "Browse", command = choose_file)
    choosefile.grid(row = 0, column = 1)

    tk.Label(SetupFrame, text = "Include 0s in calculation?").grid(row = 2, column = 0, sticky = "w")

    vYesNo = tk.IntVar()
    vYesNo.set(0)
    tk.Radiobutton(SetupFrame, text = "Yes", variable = vYesNo, 
        value = 1).grid(row = 2, column = 1, sticky = "nw")
    tk.Radiobutton(SetupFrame, text = "No", variable = vYesNo,
        value = 0).grid(row = 3, column = 1, sticky = "nw")

    next = tk.Button(SetupFrame, text = "Next", command = next_btn)
    next.grid(row = 4, column = 1)

def back_btn():
    HeatMapFrame.grid_remove()
    SetupFrame.grid()

def init_HeatMapFrame():
    global TLFrame, TRFrame, BLFrame, BRFrame
    TLFrame = Frame(HeatMapFrame)
    TLFrame.grid(row = 0, column = 0, sticky = "nswe")
    TRFrame = Frame(HeatMapFrame)
    TRFrame.grid(row = 0, column = 1, sticky = "nswe")
    BLFrame = Frame(HeatMapFrame)
    BLFrame.grid(row = 1, column = 0, sticky = "nswe")
    BRFrame = Frame(HeatMapFrame)
    BRFrame.grid(row = 1, column = 1, sticky = "nswe")

    back = tk.Button(HeatMapFrame, text = "Back", command = back_btn)
    back.grid(row = 2, column = 0, sticky = "sw")

    init_TLFrame()
    init_BLFrame()
    init_BRFrame()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()

sns.set()
root = tk.Tk()
root.wm_title("HeatMap Maker")

HeatMapFrame = Frame(root)
HeatMapFrame.grid(row = 0, column = 0, sticky = "nswe")
HeatMapFrame.grid_remove()

SetupFrame = Frame(root)
SetupFrame.grid(row = 0, column = 0, sticky = "nswe")

init_HeatMapFrame()
init_SetupFrame()

root.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()