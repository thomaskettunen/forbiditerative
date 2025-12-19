import re
from lab.parser import Parser
from enum import Enum

class ExitCode(Enum):
    FOUND_K = 0
    FOUND_ALL = 12
    OUT_OF_MEM = 22
    OUT_OF_TIME = 23
    OTHER_ERROR = 9999999

def error(content, props):
    props["error"] = not content == ''

def exit_code(content, props):
    if not props["error"]:
        matches = re.findall(r"search exit code: (\d+)", content)
        if len(matches) > 0: #. if trannslate sttep aborts, we don't even get one search exit code
            props["exit code"] = int(matches[-1])
        else:
            props["exit code"] = ExitCode.OTHER_ERROR.value #. Fake exit code to indicate this branch


def total_time(content, props):
    if not props["error"]:
        props["total time"] = float(re.search(r"All iterations are done \[(\d+\.\d+)s CPU, \d+\.\d+s wall-clock\]", content).group(1))

def coverage(content, props):
    if not props["error"]:
        match ExitCode(props["exit code"]):
            case ExitCode.FOUND_K | ExitCode.FOUND_ALL:
                props["coverage"] = 1
            case _:
                props["coverage"] = 0


def plans_found(content, props):
    if not props["error"]:
        matches = re.findall(r"found (\d+) plans", content)
        if len(matches) > 0:
            props["plans found"] = int(matches[-1])
        else:
            props["plans found"] = 0


def last_plan_time(content, props):
    if not props["error"]:
        #. Last time it says "Iteration step \d+ is done, found \d+ plans" is the last time it finds plans
        matches = re.findall(r"Iteration step \d+ is done, found \d+ plans, time \[(\d+\.\d+)s CPU, \d+\.\d+s wall-clock\]", content)
        if len(matches) > 0:
            props["last plan time_mean"] = float(matches[-1])
            props["last plan time_min"] = float(matches[-1])
            props["last plan time_max"] = float(matches[-1])
        else:
            props["last plan time_mean"] = None
            props["last plan time_min"] = None
            props["last plan time_max"] = None


def to_str(content, props):
    if not props["error"]:
        props["exit code"] = f'{ExitCode(props["exit code"])}' #. enum name. This will intentionally error on unknown exit codes
    props["error"] = str(props["error"])

class FIParser(Parser):
    def __init__(self):
        super().__init__()
        self.add_function(error, file = 'run.err') #. keep first
        self.add_function(exit_code)
        self.add_function(total_time)
        self.add_function(coverage)
        self.add_function(plans_found)
        self.add_function(last_plan_time)
        self.add_function(to_str) #. keep last, stringyfies thigs that shoulnd't be summed