import customtkinter as ctk
from tkinter import ttk
from output_console_widget import OutputConsole

class PanedWindowDemo:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Paned Window Demo")
        self.root.geometry("600x400")

        # Create a vertical PanedWindow
        self.paned_window = ttk.PanedWindow(self.root, orient='vertical')
        self.paned_window.pack(fill='both', expand=True)

        # Create top pane with counter
        self.top_frame = ctk.CTkFrame(self.paned_window)
        
        # Counter variable
        self.counter = 0
        
        # Counter display
        self.counter_label = ctk.CTkLabel(self.top_frame, text=f"Count: {self.counter}")
        self.counter_label.pack(pady=10)
        
        # Increment button
        self.increment_button = ctk.CTkButton(self.top_frame, text="Increment", command=self.increment_counter)
        self.increment_button.pack(pady=10)

        # Create bottom pane with OutputConsole
        self.output_console = OutputConsole(self.paned_window)

        # Add frames to PanedWindow
        self.paned_window.add(self.top_frame)
        self.paned_window.add(self.output_console)

    def increment_counter(self):
        self.counter += 1
        self.counter_label.configure(text=f"Count: {self.counter}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PanedWindowDemo()
    app.run()