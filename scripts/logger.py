import logging
from datetime import datetime

# Define ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
LIGHT_PURPLE = "\033[95m"

# Custom formatter with color-coded levels
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
        asctime = self.formatTime(record, self.datefmt)
        return f"{asctime} - {color}{level_name}{RESET} - {LIGHT_PURPLE}{filename}{RESET} - {BOLD}{message}{RESET}"

# Logger class
class CustomLogger:
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        # Check if handlers are already attached before adding new ones
        if not self.logger.handlers:
            # Console handler with color formatter
            console_handler = logging.StreamHandler()
            formatter = ColorFormatter(datefmt="%Y-%m-%d %H:%M:%S")
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler
            current_datetime = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            file_name = f'../logs/{current_datetime}.log'
            file_handler = logging.FileHandler(file_name)
            file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger