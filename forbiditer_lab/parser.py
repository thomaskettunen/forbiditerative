import re
from lab.parser import Parser

class FIParser(Parser):
    def __init__(self):
        super().__init__()
        self.add_pattern(
            "planner exit",
            r"run-planner exit code: (.+)\n",
            type=int,
            file="driver.log",
        )