import tkinter as tk

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


class StateSelector(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.selected_state_label = tk.Label(self, text="Selected state: ")
        self.selected_state_label.pack()

        self.state_var = tk.StringVar(self)
        self.state_var.set("Select a state")
        self.state_menu = tk.OptionMenu(self, self.state_var, *STATES, command=self.return_selected_state)
        self.state_menu.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack()

        self.selected_state = None

    def return_selected_state(self, selected_state):
        self.selected_state_label.config(text=f"Selected state: {selected_state}")
        self.selected_state = selected_state
