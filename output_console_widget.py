import customtkinter as ctk
from tkinter import ttk
from typing import Optional, List, Dict
import logging

class LogMessageWidget(ctk.CTkFrame):
    def __init__(self, master, message: str, level: int, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        bg_color = self._get_level_color(level)
        self.configure(fg_color=bg_color)
        
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            anchor="w",
            justify="left",
            wraplength=800
        )
        self.message_label.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
    
    def _get_level_color(self, level: int) -> str:
        if level >= logging.ERROR:
            return "#3a2a2a"  # Dark red
        elif level >= logging.WARNING:
            return "#3a362a"  # Dark yellow
        elif level >= logging.INFO:
            return "transparent"
        return "#2a2a3a"  # Dark blue for debug

class OutputConsole(ctk.CTkFrame):
    BUFFER_SIZE = 50  # Number of extra widgets to keep in memory
    WIDGET_HEIGHT = 30  # Approximate height of each message widget

    def bind_pop_out_callback(self, callback):
        """Bind a callback function to handle pop-out state changes"""
        self._pop_out_callback = callback
        
    def __init__(self, master, **kwargs):
        self.popped_out = False
        self.popup_window = None
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create content frame for console output
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frame container
        self.scrollable_container = ctk.CTkScrollableFrame(
            self.content_frame,
            label_text="Console Output"
        )
        self.scrollable_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollable_container.grid_columnconfigure(0, weight=1)

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

        # Initialize message counter
        self.message_count = 0
        
        # Set up logging handler
        self.log_handler = LogHandler(self)
        logging.getLogger().addHandler(self.log_handler)
    
    def append_message(self, message: str, level: int = logging.INFO):
        """Append a message to the console"""
        print("Appending message:", message)
        widget = LogMessageWidget(
            self.scrollable_container,
            message,
            level
        )
        widget.grid(row=self.message_count, column=0, sticky="ew", padx=2, pady=1)
        self.message_count += 1
        
        # Auto-scroll to bottom
        self.scrollable_container._parent_canvas.yview_moveto(1.0)

    def toggle_pop_out(self):
        """Toggle between embedded and pop-out states"""
        if not self.popped_out:
            if hasattr(self, '_pop_out_callback'):
                self._pop_out_callback(True)
            # Create pop-out window
            self.popup_window = ctk.CTkToplevel(self)
            self.popup_window.title("Output Console")
            self.popup_window.geometry("600x400")
            self.popup_window.grid_rowconfigure(0, weight=1)
            self.popup_window.grid_columnconfigure(0, weight=1)
            
            # Move the content frame to pop-out window
            self.content_frame.grid_remove()
            self.content_frame.grid(in_=self.popup_window, row=0, column=0)
            
            # Handle window close
            self.popup_window.protocol("WM_DELETE_WINDOW", self.toggle_pop_out)
            self.popped_out = True
        else:
            if hasattr(self, '_pop_out_callback'):
                self._pop_out_callback(False)
            
            # Move content frame back to main window
            self.content_frame.grid_remove()
            self.content_frame.grid(in_=self, row=0, column=0, sticky="nsew")
            
            # Clean up pop-out window
            if self.popup_window:
                self.popup_window.destroy()
                self.popup_window = None
            
            self.popped_out = False

        """Toggle between embedded and pop-out states"""
        if not self.popped_out:
            if hasattr(self, '_pop_out_callback'):
                self._pop_out_callback(True)
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
            
            # Create new scrollable frame for pop-out window
            self.popup_scrollable = ctk.CTkScrollableFrame(popup_frame)
            self.popup_scrollable.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            # Copy all message widgets to pop-out window
            for idx, msg in enumerate(self.messages):
                widget = LogMessageWidget(
                    self.popup_scrollable,
                    msg['message'],
                    msg['level']
                )
                widget.grid(row=idx, column=0, sticky="ew", padx=2, pady=1)
            
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
            
            # Handle window close
            self.popup_window.protocol("WM_DELETE_WINDOW", self.toggle_pop_out)
            self.popped_out = True
        else:
            if hasattr(self, '_pop_out_callback'):
                self._pop_out_callback(False)
            
            # Show the content frame back in main window
            self.content_frame.grid()
            
            # Clean up pop-out window
            if self.popup_window:
                self.popup_window.destroy()
                self.popup_window = None
            
            self.popped_out = False
            self.update_visible_widgets()  # Refresh the main window widgets

class LogHandler(logging.Handler):
    def __init__(self, console):
        super().__init__()
        self.console = console

    def emit(self, record):
        msg = self.format(record)
        self.console.append_message(msg, record.levelno)