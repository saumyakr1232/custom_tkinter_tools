import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Optional
import logging

class OutputConsole(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create content frame for console output
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create text widget with scrollbar
        self.text_widget = ctk.CTkTextbox(self.content_frame, wrap="none")
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Create toolbar frame
        self.toolbar = ctk.CTkFrame(self.content_frame)
        self.toolbar.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))

        # Add pop-out button
        self.pop_out_button = ctk.CTkButton(
            self.toolbar,
            text="Pop Out",
            width=80,
            command=self.toggle_pop_out
        )
        self.pop_out_button.pack(side="right", padx=5)

        # Initialize variables
        self.popped_out = False
        self.popup_window: Optional[ctk.CTkToplevel] = None
        self.original_position = None

        # Set up logging handler
        self.log_handler = LogHandler(self)
        logging.getLogger().addHandler(self.log_handler)

    def append_message(self, message: str, level: int = logging.INFO):
        """Append a message to the console with optional log level formatting"""
        tag = self._get_tag_for_level(level)
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", message + "\n", tag)
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")

    def _get_tag_for_level(self, level: int) -> str:
        """Get the appropriate tag for the log level"""
        if level >= logging.ERROR:
            return "error"
        elif level >= logging.WARNING:
            return "warning"
        elif level >= logging.INFO:
            return "info"
        return "debug"

    def toggle_pop_out(self):
        """Toggle between embedded and pop-out states"""
        if not self.popped_out:
            # Create pop-out window
            self.popup_window = ctk.CTkToplevel(self)
            self.popup_window.title("Output Console")
            self.popup_window.geometry("600x400")
            self.popup_window.grid_rowconfigure(0, weight=1)
            self.popup_window.grid_columnconfigure(0, weight=1)
            
            # Hide the content frame in main window
            self.content_frame.grid_remove()
            
            # Create a new frame in the pop-out window
            popup_frame = ctk.CTkFrame(self.popup_window)
            popup_frame.grid(row=0, column=0, sticky="nsew")
            popup_frame.grid_rowconfigure(0, weight=1)
            popup_frame.grid_columnconfigure(0, weight=1)            
            # Create new text widget for pop-out window
            popup_text = ctk.CTkTextbox(popup_frame, wrap="none")
            popup_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            # Copy content from main text widget
            popup_text.insert("1.0", self.text_widget.get("1.0", "end"))
            popup_text.configure(state="disabled")
            
            # Create new toolbar for pop-out window
            popup_toolbar = ctk.CTkFrame(popup_frame)
            popup_toolbar.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
            
            # Create new dock button
            popup_button = ctk.CTkButton(
                popup_toolbar,
                text="Dock",
                width=80,
                command=self.toggle_pop_out
            )
            popup_button.pack(side="right", padx=5)
            
            # Store references to pop-out widgets
            self.popup_text = popup_text
            self.popup_toolbar = popup_toolbar
            
            # Handle window close
            self.popup_window.protocol("WM_DELETE_WINDOW", self.toggle_pop_out)
            self.popped_out = True
        else:
            # Copy content back to main text widget
            self.text_widget.configure(state="normal")
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", self.popup_text.get("1.0", "end"))
            self.text_widget.configure(state="disabled")
            
            # Show the content frame back in main window
            self.content_frame.grid()
            
            # Clean up pop-out window
            if self.popup_window:
                self.popup_window.destroy()
                self.popup_window = None
                self.popup_text = None
                self.popup_toolbar = None
            
            self.popped_out = False

class LogHandler(logging.Handler):
    def __init__(self, console):
        super().__init__()
        self.console = console

    def emit(self, record):
        msg = self.format(record)
        self.console.append_message(msg, record.levelno)