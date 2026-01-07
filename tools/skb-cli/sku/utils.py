"""
Utility functions for SKU CLI
"""

from rich.console import Console
from rich.text import Text
import sys

console = Console()

def success(message):
    """Print success message"""
    text = Text(message)
    text.stylize("green bold")
    console.print(text)

def error(message):
    """Print error message"""
    text = Text(message)
    text.stylize("red bold")
    console.print(text)

def warning(message):
    """Print warning message"""
    text = Text(message)
    text.stylize("yellow bold")
    console.print(text)

def info(message):
    """Print info message"""
    console.print(message)
