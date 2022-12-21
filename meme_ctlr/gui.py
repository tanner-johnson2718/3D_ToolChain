import customtkinter

###############################################################################
# Globals to share data between the GUI manager and the GUI itself
###############################################################################
Serial_Q = []
CMD_Q = []   # -> Key value list tuple
GUI_killed = 0

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

###############################################################################
# GUI class is inherited from custom tkinter. It holds all GUI elements and 
# also holds the global table encapsulating what is displayed on th GUI. The
# GUI SHALL NOT be accessed, created or modifed directly through this class
# and the GUI_Man class shall be used instead. See GUI_Man for details on this.
###############################################################################
class GUI(customtkinter.CTk):
    def __init__(self, IO_poll_interval):
        super().__init__()

        self.IO_poll_interval = IO_poll_interval

###############################################################################
# Create Base GUI and base layout for selecting the various frames
###############################################################################

        self.title("MEME Controller")
        self.geometry("2000x1500")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

         # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), 
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), 
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), 
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

###############################################################################
# Create the frames
###############################################################################

        self.create_print_frame()

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

###############################################################################
# Call Backs for Selecting frames
###############################################################################

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.printer_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.printer_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

###############################################################################
# Define the global table. Each entry's key is the gcode command that gets
# that data. The second indecies in the table are one of the following)
#    -> prefix      : unique prefix of the response from printer
#    -> description : short text description of command
#    -> regex       : regex to pull relavent data from reponse
#    -> labels      : Text labels of the values returned by command
#    -> values      : numerical values returned by command
#    -> gui         : list of gui elements to be updated 
###############################################################################

    def define_global_table(self):
        self.global_table = {}
        self.global_table["M155 S1"] = {}
        self.global_table["M155 S1"]["prefix"] = "T:"
        self.global_table["M155 S1"]["description"] = "Returns Nozzle and Bed Temp every second."
        self.global_table["M155 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
        self.global_table["M155 S1"]["labels"] = ["Nozzle Current", "Nozzle Target", "Bed Current", "Bed Target"]
        self.global_table["M155 S1"]["values"] = [0,0,0,0]
        self.global_table["M155 S1"]["gui"] = []

        self.global_table["M154 S1"] = {}
        self.global_table["M154 S1"]["prefix"] = "X:"
        self.global_table["M154 S1"]["description"] = "Returns X,Y,Z,E pos every second."
        self.global_table["M154 S1"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
        self.global_table["M154 S1"]["labels"] = ["X Curr", "Y Curr", "Z Curr", "E Curr"]
        self.global_table["M154 S1"]["values"] = [0,0,0,0]
        self.global_table["M154 S1"]["gui"] = []

        self.global_table["M851"] = {}
        self.global_table["M851"]["prefix"] = "M851"
        self.global_table["M851"]["description"] = "Distance from probe to nozzle."
        self.global_table["M851"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
        self.global_table["M851"]["labels"] = ["X Probe Off", "Y Probe Off", "Z Probe Off"]
        self.global_table["M851"]["values"] = [0,0,0]
        self.global_table["M851"]["gui"] = []

        self.global_table["M92"] = {}
        self.global_table["M92"]["prefix"] = "M92"
        self.global_table["M92"]["description"] = "Steps per mm"
        self.global_table["M92"]["regex"] = r"[-+]?(?:\d*\.\d+|\d+)"
        self.global_table["M92"]["labels"] = ["X Steps per mm", "Y  Steps per mm", "Z Steps per mm", "E  Steps per mm"]
        self.global_table["M92"]["values"] = [0,0,0,0]
        self.global_table["M92"]["gui"] = []

###############################################################################
# Printing Frame defintion. The printing frame will have the following)
#    -> Current pos, temps, printing file, print progress bar
#        -> All this will be left justified in a single column
#        -> Target temps will be input boxes
#        -> Current Accels will also be shown
#     -> A terminal with input box will take up most of screen
#     -> Should have raw serial traffic with check boxes to hid traffic
###############################################################################

    def create_print_frame(self):
        padx = 20
        pady = 5

        self.printer_frame = customtkinter.CTkFrame(self)
        self.printer_frame_LHS = customtkinter.CTkFrame(self.printer_frame, fg_color="transparent")
        self.printer_frame_LHS.grid(row=0,column=0,padx=20,pady=20)
        self.printer_frame_RHS = customtkinter.CTkFrame(self.printer_frame, fg_color="transparent")
        self.printer_frame_RHS.grid(row=0,column=1,padx=20,pady=20)

        # LHS info column labels (Temp Block)
        self.nozzle_temp_cur_label = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="Nozzle Temp Current")
        self.nozzle_temp_cur_label.grid(row=0, column=0, padx=padx, pady=pady)
        self.nozzle_temp_target_label = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="Nozzle Temp Target")
        self.nozzle_temp_target_label.grid(row=1, column=0, padx=padx, pady=pady)
        self.bed_temp_cur_label = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="Bed Temp Current",)
        self.bed_temp_cur_label.grid(row=2, column=0,  padx=padx, pady=pady)
        self.bed_temp_target_label = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="Bed Temp Target")
        self.bed_temp_target_label.grid(row=3, column=0,  padx=padx, pady=pady)

        # LHS info column values (Temp Block)
        self.nozzle_temp_cur_value = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="-0.0")
        self.nozzle_temp_cur_value.grid(row=0, column=1, padx=padx, pady=pady)
        self.nozzle_temp_target_value = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="-0.0")
        self.nozzle_temp_target_value.grid(row=1, column=1, padx=padx, pady=pady)
        self.bed_temp_cur_value = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="-0.0")
        self.bed_temp_cur_value.grid(row=2, column=1,  padx=padx, pady=pady)
        self.bed_temp_target_value = customtkinter.CTkLabel(master=self.printer_frame_LHS, text="-0.0")
        self.bed_temp_target_value.grid(row=3, column=1,  padx=padx, pady=pady)

        # Define terminal and input box
        self.terminal = customtkinter.CTkTextbox(master=self.printer_frame_RHS, width=800,height=600)
        self.terminal.grid(row=0, column=0, padx=padx, pady=pady)
        self.terminal.insert("0.0", "Test")
        self.input_gcode = customtkinter.CTkEntry(master=self.printer_frame_RHS,width=800,height=50)
        self.input_gcode.grid(row=1, column=0, padx=padx, pady=pady)

###############################################################################
# IO poll function to pull data from outside of GUI into the GUI
###############################################################################
    def poll(self):
        global Serial_Q
        global GUI_killed

        if GUI_killed == 1:
            self.quit()

        while len(Serial_Q) > 0:
            self.terminal.insert("end", Serial_Q[0])
            Serial_Q.pop(0)

        while len(CMD_Q) > 0:
            self.global_table

        self.after(self.IO_poll_interval, self.poll)

###############################################################################
# Public GUI manager class. This class encapsulates and faciltates data
# transfer between GUI and other threads. All communication is done via shared
# global Qs and a global kill flag.
###############################################################################

class GUI_Man:

    def __init__(self, IO_poll_interval):
        self.IO_poll_interval = IO_poll_interval
        return

    def push_serial_input(self, line):
        global Serial_Q
        Serial_Q.append(line)
        return
    def push_command_response(self):
        return

    def kill(self):
        global GUI_killed
        GUI_killed = 1
    def thread(self):
        self.app = GUI(self.IO_poll_interval)
        self.app.after(self.IO_poll_interval, self.app.poll)
        self.app.mainloop()
