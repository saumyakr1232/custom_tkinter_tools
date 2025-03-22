import customtkinter as ctk
from tkinter import ttk
from output_console_widget import OutputConsole
import logging

class PanedWindowDemo:
    def __init__(self):
        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.root = ctk.CTk()
        self.root.title("Paned Window Demo")
        self.root.geometry("600x400")

        # Create a vertical PanedWindow
        self.paned_window = ttk.PanedWindow(self.root, orient='vertical')
        self.paned_window.pack(fill='both', expand=True)

        # Create top pane with counter
        self.top_frame = ctk.CTkFrame(self.paned_window, fg_color='red')
        
        # Counter variable
        self.counter = 0
        
        # Counter display
        self.counter_label = ctk.CTkLabel(self.top_frame, text=f"Count: {self.counter}")
        self.counter_label.pack(pady=10)
        
        # Increment button
        self.increment_button = ctk.CTkButton(self.top_frame, text="Increment", command=self.increment_counter)
        self.increment_button.pack(pady=10)
        
        # Toggle console button
        self.toggle_console_button = ctk.CTkButton(self.top_frame, text="Toggle Console", command=self.toggle_console)
        self.toggle_console_button.pack(pady=10)

        # Create bottom pane with OutputConsole
        self.output_console = OutputConsole(self.paned_window)
        self.output_console.bind_pop_out_callback(self.handle_console_pop_out)
        
        # Add frames to PanedWindow
        self.paned_window.add(self.top_frame)
        self.paned_window.add(self.output_console)
        
        # Set initial pane sizes (2/3 for top, 1/3 for bottom)
        self.root.update()
        total_height = self.root.winfo_height()
        self.paned_window.sashpos(0, int(total_height * 0.67))
        
        # Track console visibility
        self.console_visible = True

    def toggle_console(self):
        if self.console_visible:
            # Hide console by moving sash to bottom
            self.paned_window.forget(self.output_console)
            self.console_visible = False
        else:
            # Show console and set to 1/3 of space
            self.paned_window.add(self.output_console)
            self.root.update()
            total_height = self.root.winfo_height()
            self.paned_window.sashpos(0, int(total_height * 0.67))
            self.console_visible = True

    def increment_counter(self):
        self.counter += 1
        self.counter_label.configure(text=f"Count: {self.counter}")
        # Use logger instead of direct append_message
        self.logger.info(f"Counter incremented to: {self.counter}")

    def handle_console_pop_out(self, is_popped_out: bool):
        if is_popped_out:
            self.paned_window.forget(self.output_console)
        else:
            self.paned_window.add(self.output_console)
            self.root.update()
            total_height = self.root.winfo_height()
            self.paned_window.sashpos(0, int(total_height * 0.67))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PanedWindowDemo()
    app.run()