import customtkinter as ctk
import logging

class LogMessageWidget(ctk.CTkFrame):
    def __init__(self, master, message: str, level: int, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        bg_color = self._get_level_color(level)
        text_color = self._get_text_color(level)
        self.configure(fg_color=bg_color)
        
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            anchor="w",
            justify="left",
            wraplength=800,
            text_color=text_color,
            font=ctk.CTkFont(weight=self._get_font_weight(level))
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

    def _get_text_color(self, level: int) -> str:
        if level >= logging.ERROR:
            return "#FF6B6B"  # Bright red
        elif level >= logging.WARNING:
            return "#FFD93D"  # Bright yellow
        elif level >= logging.INFO:
            return None  # Default text color
        return "#6B8E23"  # Olive green for debug

    def _get_font_weight(self, level: int) -> str:
        if level >= logging.ERROR:
            return "bold"
        elif level >= logging.WARNING:
            return "bold"
        return "normal"


class CollapsibleLogMessageWidget(LogMessageWidget):
    def __init__(self, master, message: str, level: int, details: str = "", action_text=None, action_callback=None, **kwargs):
        super().__init__(master, message, level, **kwargs)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Make the header clickable
        self.message_label.configure(cursor="hand2")
        self.message_label.bind("<Button-1>", self._toggle_details)
        
        # Add expand/collapse indicator
        self.expand_label = ctk.CTkLabel(
            self,
            text="▶",  # Right arrow for collapsed state
            width=20,
            anchor="w"
        )
        self.expand_label.grid(row=0, column=0, sticky="w", padx=(5, 0))
        
        # Update message label to take full width and align left
        self.message_label.grid(row=0, column=1, sticky="w", padx=5)
        # self.message_label.configure(anchor="w", justify="left")
        
        # Create details section
        self.details_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.details_text = ctk.CTkTextbox(
            self.details_frame,
            wrap="word",
            height=100,
            activate_scrollbars=True
        )
        self.details_text.insert("1.0", details)
        self.details_text.configure(state="disabled")
        self.details_text.pack(fill="both", expand=True, padx=25, pady=(0, 5))
        
        # Initialize state
        self.expanded = False
        self.details_frame.grid_remove()  # Start collapsed
        
        # Update grid configuration
        self.grid_columnconfigure(1, weight=1)
        
    def _toggle_details(self, event=None):
        self.expanded = not self.expanded
        if self.expanded:
            self.expand_label.configure(text="▼")  # Down arrow for expanded state
            self.details_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        else:
            self.expand_label.configure(text="▶")  # Right arrow for collapsed state
            self.details_frame.grid_remove()