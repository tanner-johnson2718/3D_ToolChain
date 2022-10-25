import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Multiline('', key="printer_output", size=(80,20), disabled=1)],
            [sg.InputText(key="cmd_box", size=(80,1))],
        ]

# Create the Window
window = sg.Window('Window Title', layout, finalize=1)
window["cmd_box"].bind("<Return>", "enter_hit")

# Window Elements
printer_output = window["printer_output"]
cmd_box = window["cmd_box"]

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == "cmd_box" + "enter_hit":
        printer_output.update(printer_output.get() + "\n" + cmd_box.get())
        printer_output.set_vscroll_position(1.0)
        cmd_box.update("")

window.close()