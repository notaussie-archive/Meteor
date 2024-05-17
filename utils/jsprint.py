"""
Copyright (c) 2023 NotAussie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""JSPrint - A JavaScript way of printing to the console."""

# Imports
from datetime import datetime

# Version
__version__ = "0.0.4"


# Colour class
class Colour:
    white = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"


# Styles class
class Styles:
    default = "\033[0m"
    bold = "\033[1m"
    underline = "\033[4m"
    reversed = "\033[7m"
    reset = "\033[0m"


# Utils class
class Utils:
    @staticmethod
    def date():
        return f"{Colour.grey}[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]{Styles.reset}"

    default = ["log", "warn", "error", "info", "success", "debug", "trace"]


# JSPrint class
class JSP:
    def __init__(self, log_level: str = "log"):
        # Set log level
        self.log_level = log_level
        self.levels = ["log", "warn", "error", "info", "success", "debug", "trace"]

        # Enable all logging levels below the user input
        if log_level == "warn":
            self.levels = ["warn", "error", "info", "success", "debug", "trace"]
        elif log_level == "error":
            self.levels = ["error", "info", "success", "debug", "trace"]
        elif log_level == "info":
            self.levels = ["info", "success", "debug", "trace"]
        elif log_level == "success":
            self.levels = ["success", "debug", "trace"]
        elif log_level == "debug":
            self.levels = ["debug", "trace"]
        elif log_level == "trace":
            self.levels = ["trace"]

    def set_log_level(self, log_level: str):
        """
        Sets the log level.

        Args:
            log_level (str): The log level to set.
        """
        self.log_level = log_level

        # Enable all logging levels below the user input
        if log_level == "warn":
            self.levels = ["warn", "error", "info", "success", "debug", "trace"]
        elif log_level == "error":
            self.levels = ["error", "info", "success", "debug", "trace"]
        elif log_level == "info":
            self.levels = ["info", "success", "debug", "trace"]
        elif log_level == "success":
            self.levels = ["success", "debug", "trace"]
        elif log_level == "debug":
            self.levels = ["debug", "trace"]
        elif log_level == "trace":
            self.levels = ["trace"]

    def log(self, message: str):
        """
        Logs a message with the [LOG] level.

        Args:
            message (str): The message to be logged.
        """
        if "log" in self.levels and self.levels.index("log") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.blue}[LOG]{Colour.white} {message}{Styles.reset}"
            )

    def warn(self, message: str):
        """
        Logs a message with the [WARN] level.

        Args:
            message (str): The message to be logged.
        """
        if "warn" in self.levels and self.levels.index("warn") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.yellow}[WARN]{Colour.white} {message}{Styles.reset}"
            )

    def error(self, message: str):
        """
        Logs a message with the [ERROR] level.

        Args:
            message (str): The message to be logged.
        """
        if "error" in self.levels and self.levels.index("error") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.red}[ERROR]{Colour.white} {message}{Styles.reset}"
            )

    def info(self, message: str):
        """
        Logs a message with the [INFO] level.

        Args:
            message (str): The message to be logged.
        """
        if "info" in self.levels and self.levels.index("info") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.cyan}[INFO]{Colour.white} {message}{Styles.reset}"
            )

    def success(self, message: str):
        """
        Logs a message with the [SUCCESS] level.

        Args:
            message (str): The message to be logged.
        """
        if "success" in self.levels and self.levels.index(
            "success"
        ) >= self.levels.index(self.log_level):
            print(
                f"{Utils.date()} {Colour.green}[SUCCESS]{Colour.white} {message}{Styles.reset}"
            )

    def debug(self, message: str):
        """
        Logs a message with the [DEBUG] level.

        Args:
            message (str): The message to be logged.
        """
        if "debug" in self.levels and self.levels.index("debug") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.purple}[DEBUG]{Colour.white} {message}{Styles.reset}"
            )

    def trace(self, message: str):
        """
        Logs a message with the [TRACE] level.

        Args:
            message (str): The message to be logged.
        """
        if "trace" in self.levels and self.levels.index("trace") >= self.levels.index(
            self.log_level
        ):
            print(
                f"{Utils.date()} {Colour.grey}[TRACE]{Colour.white} {message}{Styles.reset}"
            )
