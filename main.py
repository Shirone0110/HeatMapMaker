import numpy as np
from pandas.core.indexes.base import Index
import seaborn as sns
import pandas as pd
import tkinter as tk
import threading
from tkinter.constants import DISABLED, END, NORMAL
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter import StringVar, colorchooser, Frame, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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
    BLFrame.subframe[ind].grid(row = ind + 2, column = 1, columnspan = 6)

    #label
    label = tk.Label(BLFrame.subframe[ind], text = "Color " + str(ind + 1))
    label.grid(column = 1, row = ind + 3)

    #color changing button
    BLFrame.buttons[ind] = tk.Button(BLFrame.subframe[ind], width = 3)
    BLFrame.buttons[ind].grid(column = 2, row = ind + 3, padx = 5)
    cmd = lambda btn = BLFrame.buttons[ind]: pressed(btn)
    BLFrame.buttons[ind].configure(command = cmd)

    #left entries
    BLFrame.string_vars.append(StringVar())
    BLFrame.entries[ind * 2] = tk.Entry(BLFrame.subframe[ind], width = 5,
        textvariable = BLFrame.string_vars[ind * 2])
    BLFrame.entries[ind * 2].grid(column = 3, row = ind + 3, padx = 5)

    #right entries
    BLFrame.string_vars.append(StringVar())
    BLFrame.string_vars[ind * 2 + 1].trace('w',
        lambda name, index, mode, var = BLFrame.string_vars[ind * 2 + 1], i = ind: entry(var, i))
    BLFrame.entries[ind * 2 + 1] = tk.Entry(BLFrame.subframe[ind], width = 5,
        textvariable = BLFrame.string_vars[ind * 2 + 1])
    BLFrame.entries[ind * 2 + 1].grid(column = 5, row = ind + 3, padx = 5)

    #decoration
    tk.Label(BLFrame.subframe[ind], text = "to").grid(column = 4, row = ind + 3)
    tk.Label(BLFrame.subframe[ind], text = "%").grid(column = 6, row = ind + 3)

def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb = matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict

def nudge(ax):
    ax.xaxis.tick_top()
    ax.set_xticklabels(data.columns, rotation = 45)
    ax.set_ylabel('')
    ax.xaxis.set_label_position('top')
    for label in ax.get_xticklabels():
        label.set_style('italic')
    ax.tick_params(length = 0)
    return ax

def create_plot(colormap): #create plot with color map
    sns.set(style = 'white')
    plt.close('all')
    f, ax = plt.subplots(figsize = (10, 6))
    max = data.to_numpy().max()
    min = data.to_numpy().min()
    ax = sns.heatmap(vmin = min, vmax = max, data = data.head(vTop.get()), 
        cmap = colormap)
    ax = nudge(ax)
    plt.subplots_adjust(left = 0.17, right = 1.04, bottom = 0.05, top = 0.8)
    return f

def export(fig): #export figure in pdf or png
    files = [('PNG', '*.png'), ('PDF', '*.pdf')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    if file is None:
        return
    addr = file.name
    fig.savefig(addr)

def preview():
    num = vDropdown.get()
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
    canvas = FigureCanvasTkAgg(fig, master = CustomFrame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0)

    #export button
    cmd = lambda fig = fig: export(fig)
    exportbutton = tk.Button(CustomFrame, text = "Export", command = cmd)
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
    
    preview()

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
    button = tk.Button(BLFrame, text = "Preview", command = cmd)
    button.grid(column = 2, row = 12, sticky = "se")

def switch():
    if vOption.get() == 1:
        CustomFrame.grid()
        DefaultFrame.grid_remove()
    else:
        DefaultFrame.grid()
        draw()
        CustomFrame.grid_remove()

def init_BLFrame():
    tk.Radiobutton(BLFrame, text = "Custom", variable = vOption, 
        value = 1, command = switch).grid(row = 0, column = 0, sticky = "nw", columnspan = 2)

    label = tk.Label(BLFrame, text = "Colors")
    label.grid(column = 1, row = 1)

    global vDropdown
    vDropdown = tk.IntVar()
    optionList = np.arange(4, 11, 1)
    dropdown = tk.OptionMenu(BLFrame, vDropdown, *optionList, command = display)
    dropdown.grid(column = 2, row = 1)

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
    plt.close('all')
    f, ax = plt.subplots(figsize = (10, 6))
    if (int(color) < 3):
        cmap = sns.color_palette(values[color])
    else:
        cmap = sns.color_palette(values[color], as_cmap = True)
    ax = sns.heatmap(data.head(vTop.get()), cmap = cmap, center = 0)
    ax = nudge(ax)
    plt.subplots_adjust(left = 0.17, right = 1.04, bottom = 0.05, top = 0.8)
    return f

def draw(): #redraw heatmap when change button
    color = vDefaultColor.get()
    fig = create_default(color)
    canvas = FigureCanvasTkAgg(fig, master = DefaultFrame)  
    canvas.draw()
    canvas.get_tk_widget().grid(row = 0, column = 0)

    cmd = lambda fig = fig: export(fig)
    exportbutton = tk.Button(DefaultFrame, text = "Export", command = cmd)
    exportbutton.grid(row = 1, column = 0, sticky = "se")

def change_default():
    vOption.set(0)
    switch()

def init_TLFrame():
    tk.Radiobutton(TLFrame, text = "Default", variable = vOption, 
        value = 0, command = switch).grid(row = 0, column = 0, sticky = "nw", columnspan = 2)

    label = tk.Label(TLFrame, text = "Choose a color palette:")
    label.grid(column = 1, row = 1, columnspan = 3, sticky = "nw")

    #some random color schemes
    global values, vDefaultColor
    values = {"1": "pastel", "2": "hls", "3": "Blues", "4": "YlOrBr",
            "5": "icefire"}

    vDefaultColor = tk.StringVar()
    vDefaultColor.set("1")
    count = 0

    for val, text in values.items():
        count += 1
        tk.Radiobutton(TLFrame, text = text, variable = vDefaultColor, 
            command = change_default, value = val).grid(row = count + 1, column = 1, sticky = "nw")

def find_top(df):
    df['mean'] = df.mean(axis = 1)
    df = df.sort_values(by = ['mean'], ascending = False)
    del df['mean']
    return df

def rowNames(indices, labels):
    rows = []
    for index in indices:
        rows.append(labels[index + 3])
    return rows

def set_depth(bacterias):
    new_list = []
    depth = min(map(lambda list: len(list), bacterias))
    for otu in bacterias:
        new_list.append(otu[:depth])
    return new_list

def getBacterias(top_otus, path_to_file):
    bacterias = [None] * len(top_otus)
    
    with open(path_to_file, 'r') as file:
        next(file)
        for line in file:
            for i in range(len(top_otus)):
                if top_otus[i] in line:
                    text = line.split()[2:][0]
                    species = text.split(';')[:-1]
                    species = list(map(lambda item: item.split('(')[0], species))
                    species = list(filter(lambda item: 'unclassified' not in item and
                        'uncultured' not in item, species))
                    bacterias[i] = species
                    break
    return bacterias

def process_file():
    path = csvfile.name
    df = pd.read_csv(path)
    df = edit(df)
    column = columnNames(df)
    rows = []
    
    #for ind in range(4, len(df.index)):
    for ind in range(4, 24):
        if vYesNo.get() == 0:
            new = noZeros(df, ind)
        else:
            new = inclZeros(df, ind)
        rows.append(new)
    
    global data
    data = pd.DataFrame(rows, columns = column)
    data = find_top(data)
    ind = rowNames(data.index, df.columns)

    bacterias = getBacterias(ind, taxofile.name)
    bacterias = set_depth(bacterias)

    tax_depth = opts.index(vTax.get())
    rowLabel = []
    for i in range(len(ind)):
        rowLabel.append(bacterias[i][tax_depth])
    data['ind'] = rowLabel
    data.set_index(keys = 'ind', inplace = True)
    #print(data)
    draw()

def choose_file():
    files = [('CSV', '*.csv')]
    global csvfile
    csvfile = askopenfile(filetypes = files, defaultextension = files)
    if csvfile is None:
        return
    addr = csvfile.name
    addr = addr.split('/')
    showfilename.config(text = addr[-1], fg = 'black')

def choose_taxo():
    files = [('Taxonomy', '*.taxonomy')]
    global taxofile
    taxofile = askopenfile(filetypes = files, defaultextension = files)
    if taxofile is None:
        return
    addr = taxofile.name
    addr = addr.split('/')
    showtaxoname.config(text = addr[-1], fg = 'black')

def loading():
    try:
        process_file()
    except IndexError:
        messagebox.showerror("Error", "Taxonomy depth not available") 
        root.config(cursor = "")  
        return
    SetupFrame.grid_remove()
    HeatMapFrame.grid()
    root.config(cursor = "")

def next_btn():
    if showfilename.cget('text') == "No file selected":
        messagebox.showerror("Error", "Please choose data file")
        return

    if showtaxoname.cget('text') == "No file selected":
        messagebox.showerror("Error", "Please choose taxonomy file")
        return

    root.config(cursor = "watch")
    threading.Thread(target = loading).start()
    
#calculates averages for one row not including zeros
def noZeros(df, ind):
    sum = 0
    cnt = 0
    new = []
    lastSpec = df.at[0, "Category"]
    numOtus = df.at[0, "numOtus"]

    for row in df.itertuples():
        if(row[2] == lastSpec):
            sum += row[ind]
            if(row[ind] != 0):
                cnt += 1
        else:
            if(cnt != 0):
                avgOccurrence = sum / (cnt * numOtus)
            else:
                avgOccurrence = 0
            new.append(avgOccurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            if(row[ind] != 0):
                cnt += 1
        lastSpec = row[2]

    return new

#calculates averages for one row including zeros
def inclZeros(df, ind):
    sum = 0
    cnt = 0
    new = []
    lastSpec = df.at[0, "Category"]
    numOtus = df.at[0, "numOtus"]

    for row in df.itertuples():
        if(row[2] == lastSpec):
            sum += row[ind]
            cnt += 1
        else:
            if(cnt != 0):
                avgOccurrence = sum / (cnt * numOtus)
            else:
                avgOccurrence = 0
            new.append(avgOccurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            cnt += 1
        lastSpec = row[2]

    return new

def columnNames(df):
    columns = []
    lastSpec = df.at[0, "Category"]
    genus = df.at[0, "Sub"]
    
    for row in df.itertuples():
        if row[2] != lastSpec:
            columns.append(genus[0] + ". " + lastSpec)
            lastSpec = row[2]
            genus = row[3]
            
    return columns

def edit(df):
    del df['label']
    del df["Group"]
    df = df.loc[df["Category"] != "water"]
    df = df.loc[df["Category"] != "soil"]
    df = df.loc[df["Category"] != "moss"] 
    return df

def init_SetupFrame():
    canvas = tk.Canvas(SetupFrame, width = 300, height = 350)
    canvas.grid(row = 0, column = 0, columnspan = 8, rowspan = 8)

    #choose file prompt
    tk.Label(SetupFrame, text = "1. Choose data file").grid(row = 0, column = 0, 
        sticky = "w", ipadx = 10, ipady = 10)

    #show file name
    global showfilename, vYesNo
    showfilename = tk.Label(SetupFrame, text = "No file selected", fg = 'red')
    showfilename.grid(row = 1, column = 1, sticky = "n")

    choosefile = tk.Button(SetupFrame, text = "Browse", command = choose_file)
    choosefile.grid(row = 0, column = 1)

    tk.Label(SetupFrame, text = "2. Include 0s in calculation?").grid(row = 2, column = 0, 
        sticky = "w", padx = 10)

    vYesNo = tk.IntVar()
    tk.Radiobutton(SetupFrame, text = "Yes", variable = vYesNo, 
        value = 1).grid(row = 2, column = 1)
    tk.Radiobutton(SetupFrame, text = "No", variable = vYesNo,
        value = 0).grid(row = 3, column = 1)
    vYesNo.set(0)

    tk.Label(SetupFrame, text = "3. Choose taxonomy file").grid(row = 4, column = 0, 
        sticky = "w", ipadx = 10, ipady = 10)

    #show file name
    global showtaxoname, opts, vTax
    showtaxoname = tk.Label(SetupFrame, text = "No file selected", fg = 'red')
    showtaxoname.grid(row = 5, column = 1, sticky = "n")

    choosefile = tk.Button(SetupFrame, text = "Browse", command = choose_taxo)
    choosefile.grid(row = 4, column = 1)

    tk.Label(SetupFrame, text = "4. Choose taxonomy depth").grid(row = 6, column = 0, padx = 10)
    opts = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    vTax = tk.StringVar()
    vTax.set(opts[0])
    ddown = tk.OptionMenu(SetupFrame, vTax, *opts)
    ddown.grid(row = 6, column = 1, padx = 10)

    next = tk.Button(SetupFrame, text = "Next", command = next_btn)
    next.grid(row = 7, column = 2, padx = 10, pady = 10)

def back_btn():
    HeatMapFrame.grid_remove()
    SetupFrame.grid()

def setup_plot():
    plt.yticks(rotation = 0)
    plt.rcParams.update({'font.size': 10})

def handleReturn(event):
    TLFrame.focus_set()
    if vOption.get() == 0:
        draw()
    else:
        preview()

def init_HeatMapFrame():
    global TLFrame, DefaultFrame, BLFrame, CustomFrame, vOption, vTop
    vOption = tk.IntVar() # 0 for default, 1 for custom
    vTop = tk.IntVar()
    vTop.set(10)

    tk.Label(HeatMapFrame, text = 'Show top').grid(row = 0, column = 0)
    entry = tk.Entry(HeatMapFrame, width = 5, textvariable = vTop)
    entry.grid(row = 0, column = 1, sticky = "w")
    entry.bind("<Return>", handleReturn)
    tk.Label(HeatMapFrame, text = 'results').grid(row = 0, column = 2, sticky = "w")

    TLFrame = Frame(HeatMapFrame)
    TLFrame.grid(row = 1, column = 0, sticky = "nswe", columnspan = 3)
    DefaultFrame = Frame(HeatMapFrame)
    DefaultFrame.grid(row = 0, column = 3, sticky = "nswe", rowspan = 3)
    BLFrame = Frame(HeatMapFrame)
    BLFrame.grid(row = 2, column = 0, sticky = "nswe", columnspan = 3)
    CustomFrame = Frame(HeatMapFrame)
    CustomFrame.grid(row = 0, column = 3, sticky = "nswe", rowspan = 3)
    CustomFrame.grid_remove()

    tk.Canvas(TLFrame, width = 250, height = 180).grid(row = 0, 
        column = 0, rowspan = 7, columnspan = 7)
    tk.Canvas(BLFrame, width = 250, height = 400).grid(row = 0, 
        column = 0, rowspan = 13, columnspan = 7)
    tk.Canvas(CustomFrame, width = 1000, height = 600).grid(row = 0, column = 0)

    back = tk.Button(HeatMapFrame, text = "Back", command = back_btn)
    back.grid(row = 2, column = 0, sticky = "sw")

    init_TLFrame()
    init_BLFrame()
    setup_plot()

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