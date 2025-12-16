import re
from lab.parser import Parser

def total_time(content, props):
    
    output = re.search(r"All iterations are done \[(.+)s", content)
    
    props["total time"] = float(output.group().split(" ")[4][1:-1])

def coverage(content, props):
    props["coverage"] = int(props["planner exit"] == 0)

def plans_found(content, props):
    output = re.findall(r"found [1234567890]+ plans", content)
    props["plans found"] = int(output[-1].split(" ")[1])

# time for last found plan (time at last reformulation done) case where searched entire state space (run.log returncode 12, driver.log planner exit 0)
def last_plan_time(content, props):

    text_times = re.findall(r"Planner time: .+s", content)[:-1]

    total_time = 0

    for time in text_times:
        total_time += float(time.split(" ")[2][:-1]) # :-1 removes the 's'

    if props["planner exit"] == 0:
        props["Succesful: last plan found time"] = total_time
    elif props["planner exit"] == -15:
        props["Timeout: last plan found time"] = total_time

class FIParser(Parser):
    def __init__(self):
        super().__init__()
        self.add_pattern(
            "planner exit",
            r"run-planner exit code: (.+)\n",
            type=int,
            file="driver.log",
        )
        self.add_function(total_time)
        self.add_function(coverage)
        self.add_function(plans_found)
        self.add_function(last_plan_time)