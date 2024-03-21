import logging
import discord

from datetime import datetime

# Define ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
LIGHT_PURPLE = "\033[95m"

# Create a custom formatter with color-coded levels
class ColorFormatter(logging.Formatter):

    COLORS = {
        'DEBUG': BLUE,
        'INFO': GREEN,
        'WARNING': YELLOW,
        'ERROR': RED,
        'CRITICAL': RED + BOLD,
    }

    def format(self, record):
        level_name = record.levelname
        filename = record.filename
        
        color = self.COLORS.get(level_name)
        message = record.getMessage()
        
        # Get the asctime in the desired format
        asctime = self.formatTime(record, self.datefmt)
        
        return f"{asctime} - {color}{level_name}{RESET} - {LIGHT_PURPLE}{filename}{RESET} - {BOLD}{message}{RESET}"

# Initialize logger
def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set minimum logging level

    # Console handler with color formatter
    console_handler = logging.StreamHandler()
    formatter = ColorFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    current_datetime = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file_name = f'../logs/{current_datetime}.log'
    file_handler = logging.FileHandler(file_name)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
