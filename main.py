import tkinter as tk
from tkinter import ttk, messagebox


class TuringMachine:
    def __init__(self, tape, transitions, start_state, halt_states):
        self.tape = list(tape)
        self.head = 0
        self.state = start_state
        self.transitions = transitions
        self.halt_states = halt_states

    def step(self):
        if self.state in self.halt_states:
            return False

        current_symbol = self.tape[self.head]
        key = (self.state, current_symbol)

        if key not in self.transitions:
            return False

        next_state, write_symbol, direction = self.transitions[key]
        self.tape[self.head] = write_symbol
        self.state = next_state

        if direction == "R":
            self.head += 1
            if self.head >= len(self.tape):
                messagebox.showerror('Error', 'Movement not Possible')
        elif direction == "L":
            self.head -= 1
            if self.head < 0:
                messagebox.showerror('Error', 'Movement not Possible')


        return True


class TuringMachineVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Turing Machine Visualizer")

        # Input for tape
        input_frame = ttk.LabelFrame(root, text="Input Configuration")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Tape (e.g., 101101$):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tape_entry = ttk.Entry(input_frame, width=40)
        self.tape_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Start State:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_state_entry = ttk.Entry(input_frame, width=20)
        self.start_state_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text="Halt States").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.halt_states_entry = ttk.Entry(input_frame, width=40)
        self.halt_states_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Transition", command=self.add_transition).grid(row=3, column=0, pady=10)
        self.transition_listbox = tk.Listbox(input_frame, height=5, width=50)
        self.transition_listbox.grid(row=3, column=1, pady=10)

        ttk.Button(input_frame, text="Set Configuration", command=self.set_configuration).grid(row=4, columnspan=2, pady=10)

        # Tape visualization
        self.tape_display = tk.Canvas(root, height=100, bg="white")
        self.tape_display.pack(fill=tk.BOTH, expand=True)

        # Controls
        controls_frame = ttk.Frame(root)
        controls_frame.pack()

        self.start_button = ttk.Button(controls_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.step_button = ttk.Button(controls_frame, text="Step", command=self.step)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(controls_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Placeholder variables
        self.tape = []
        self.transitions = {}
        self.start_state = "q0"
        self.halt_states = set()
        self.turing_machine = None

    def add_transition(self):
        transition_window = tk.Toplevel(self.root)
        transition_window.title("Add/Update Transition")

        # Labels and entry fields for transition data
        ttk.Label(transition_window, text="Current State:").grid(row=0, column=0, padx=5, pady=5)
        current_state_entry = ttk.Entry(transition_window, width=10)
        current_state_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(transition_window, text="Current Symbol:").grid(row=1, column=0, padx=5, pady=5)
        current_symbol_entry = ttk.Entry(transition_window, width=10)
        current_symbol_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(transition_window, text="Next State:").grid(row=2, column=0, padx=5, pady=5)
        next_state_entry = ttk.Entry(transition_window, width=10)
        next_state_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(transition_window, text="Write Symbol:").grid(row=3, column=0, padx=5, pady=5)
        write_symbol_entry = ttk.Entry(transition_window, width=10)
        write_symbol_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(transition_window, text="Direction (L/R):").grid(row=4, column=0, padx=5, pady=5)
        direction_entry = ttk.Entry(transition_window, width=10)
        direction_entry.grid(row=4, column=1, padx=5, pady=5)

        # Populate entries if updating
        selected_index = self.transition_listbox.curselection()
        if selected_index:
            selected_transition = self.transition_listbox.get(selected_index)
            current, result = selected_transition.split(" -> ")
            state, symbol = current.split(",")
            next_state, write_symbol, direction = result.split(",")

            current_state_entry.insert(0, state)
            current_symbol_entry.insert(0, symbol)
            next_state_entry.insert(0, next_state)
            write_symbol_entry.insert(0, write_symbol)
            direction_entry.insert(0, direction)

        # Save or update the transition
        def save_transition():
            current_state = current_state_entry.get().strip()
            current_symbol = current_symbol_entry.get().strip()
            next_state = next_state_entry.get().strip()
            write_symbol = write_symbol_entry.get().strip()
            direction = direction_entry.get().strip()

            if not current_state or not current_symbol or not next_state or not write_symbol or direction not in {"L", "R"}:
                messagebox.showerror("Error", "Invalid transition format!")
                return

            transition_key = f"{current_state},{current_symbol} -> {next_state},{write_symbol},{direction}"

            if selected_index:  # Update the selected transition
                self.transition_listbox.delete(selected_index)
                self.transition_listbox.insert(selected_index, transition_key)
            else:  # Add a new transition
                self.transition_listbox.insert(tk.END, transition_key)

            transition_window.destroy()

        ttk.Button(transition_window, text="Save", command=save_transition).grid(row=5, columnspan=2, pady=10)

    def update_transition(self):
        if not self.transition_listbox.curselection():
            messagebox.showwarning("Warning", "No transition selected for update!")
            return
        self.add_transition()


    def set_configuration(self):
        tape = self.tape_entry.get().strip()
        start_state = self.start_state_entry.get().strip()
        halt_states = set(self.halt_states_entry.get().strip().split(","))

        if not tape or not start_state or not halt_states or not self.transition_listbox.size():
            messagebox.showerror("Error", "All fields must be filled out, and transitions must be added!")
            return

        try:
            transitions = {}
            for i in range(self.transition_listbox.size()):
                transition = self.transition_listbox.get(i)
                current, result = transition.split(" -> ")
                state, symbol = current.split(",")
                next_state, write_symbol, direction = result.split(",")
                transitions[(state, symbol)] = (next_state, write_symbol, direction)

            self.tape = list(tape)
            self.transitions = transitions
            self.start_state = start_state
            self.halt_states = halt_states
            self.turing_machine = TuringMachine(self.tape, self.transitions, self.start_state, self.halt_states)
            self.update_tape_display()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid configuration: {e}")

    def update_tape_display(self):
        self.tape_display.delete("all")
        x_start = 10
        y_start = 30
        cell_width = 40

        for i, symbol in enumerate(self.turing_machine.tape):
            x = x_start + i * cell_width
            color = "yellow" if i == self.turing_machine.head else "white"
            self.tape_display.create_rectangle(x, y_start, x + cell_width, y_start + 40, fill=color, outline="black")
            self.tape_display.create_text(x + cell_width / 2, y_start + 20, text=symbol, font=("Arial", 16))

    def start(self):
        self.run = True
        self.auto_step()

    def auto_step(self):
        if self.run and self.turing_machine.step():
            self.update_tape_display()
            self.root.after(500, self.auto_step)
        else:
            self.run = False

    def step(self):
        if self.turing_machine.step():
            self.update_tape_display()

    def reset(self):
        if self.turing_machine:
            self.turing_machine = TuringMachine(self.tape, self.transitions, self.start_state, self.halt_states)
            self.update_tape_display()


if __name__ == "__main__":
    root = tk.Tk()
    visualizer = TuringMachineVisualizer(root)
    root.mainloop()