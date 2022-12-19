# Gui Code. Maintains gui and keeps track of printer state. Should be ran on
# main thread

global_table = {}
global_table["M155 S1"] = {}
global_table["M155 S1"]["prefix"] = "T:"
global_table["M155 S1"]["description"] = "Returns Nozzle and Bed Temp every second."
global_table["M155 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
global_table["M155 S1"]["labels"] = ["Nozzle Current", "Nozzle Target", "Bed Current", "Bed Target"]
global_table["M155 S1"]["values"] = [0,0,0,0]
global_table["M155 S1"]["gui"] = []

global_table["M154 S1"] = {}
global_table["M154 S1"]["prefix"] = "X:"
global_table["M154 S1"]["description"] = "Returns X,Y,Z,E pos every second."
global_table["M154 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
global_table["M154 S1"]["labels"] = ["X Curr", "Y Curr", "Z Curr", "E Curr"]
global_table["M154 S1"]["values"] = [0,0,0,0]
global_table["M154 S1"]["gui"] = []

global_table["M851"] = {}
global_table["M851"]["prefix"] = "M851"
global_table["M851"]["description"] = "Distance from probe to nozzle."
global_table["M851"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
global_table["M851"]["labels"] = ["X Probe Off", "Y Probe Off", "Z Probe Off"]
global_table["M851"]["values"] = [0,0,0]
global_table["M851"]["gui"] = []

global_table["M92"] = {}
global_table["M92"]["prefix"] = "M92"
global_table["M92"]["description"] = "Steps per mm"
global_table["M92"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
global_table["M92"]["labels"] = ["X Steps per mm", "Y  Steps per mm", "Z Steps per mm", "E  Steps per mm"]
global_table["M92"]["values"] = [0,0,0,0]
global_table["M92"]["gui"] = []

def gui_start():
    
    return