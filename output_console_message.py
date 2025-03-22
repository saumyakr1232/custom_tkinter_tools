from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class OutputConsoleMessage:
    msg: str
    level: int
    

@dataclass
class TextOutputConsoleMessage(OutputConsoleMessage):
    details: Optional[str] = None
    action_text: Optional[str] = None
    action_callback: Optional[Callable] = None

    def __init__(self, msg: str, level: int, details: str = None, action_text: str = None, action_callback: Callable = None):
        super().__init__(
            msg=msg,
            level=level
        )
        self.details=details
        self.action_text=action_text
        self.action_callback=action_callback
